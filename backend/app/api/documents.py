
import logging
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import get_settings
from app.ingestion.document_loader import DocumentLoader
from app.ingestion.ingestion_service import IngestionService
from app.knowledge.knowledge_builder import KnowledgeBuilder
from app.knowledge.learner_store import LearnerStore
from app.retrieval.rag_service import RAGService
from app.schemas.document import (
    DocumentContentResponse,
    DocumentResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

settings = get_settings()

loader = DocumentLoader()
ingestion_service = IngestionService()
knowledge_builder = KnowledgeBuilder()
learner_store = LearnerStore()
rag_service = RAGService()


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    learner_id: int,
    file: UploadFile = File(...),
) -> DocumentResponse:

    # ---------------------------------------------------------
    # Validate learner
    # ---------------------------------------------------------

    if learner_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="learner_id must be a positive integer.",
        )

    # ---------------------------------------------------------
    # Validate file
    # ---------------------------------------------------------

    filename = file.filename or ""

    extension = Path(filename).suffix.lower()

    if extension not in settings.allowed_file_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are currently supported.",
        )

    # ---------------------------------------------------------
    # Create document ID
    # ---------------------------------------------------------

    document_id = str(uuid.uuid4())

    documents_dir = Path(settings.documents_dir)

    documents_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = (
        documents_dir
        / f"{document_id}.pdf"
    )

    max_size = (
        settings.max_upload_size_mb
        * 1024
        * 1024
    )

    try:

        # -----------------------------------------------------
        # Save uploaded file
        # -----------------------------------------------------

        size = 0

        with destination.open("wb") as output:

            while chunk := await file.read(
                1024 * 1024
            ):

                size += len(chunk)

                if size > max_size:

                    destination.unlink(
                        missing_ok=True
                    )

                    raise HTTPException(
                        status_code=(
                            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
                        ),
                        detail=(
                            f"File size exceeds "
                            f"{settings.max_upload_size_mb} MB."
                        ),
                    )

                output.write(chunk)

        # -----------------------------------------------------
        # Parse pages
        # -----------------------------------------------------

        pages = loader.load(
            destination,
            extension,
        )

        logger.info(
            "Uploaded document "
            "learner_id=%s document_id=%s "
            "filename=%s pages=%d",
            learner_id,
            document_id,
            filename,
            len(pages),
        )

        # -----------------------------------------------------
        # Build learner knowledge
        #
        # This:
        # PDF
        #   ↓
        # chunks
        #   ↓
        # concept extraction
        #   ↓
        # KnowledgeStore
        #   ↓
        # LearnerStore
        # -----------------------------------------------------

        knowledge = knowledge_builder.build(
            learner_id=learner_id,
            document_id=document_id,
            file_path=destination,
        )

        logger.info(
            "Knowledge built "
            "learner_id=%s document_id=%s concepts=%d",
            learner_id,
            document_id,
            len(knowledge),
        )
        learner_store.add_history(
            learner_id=learner_id,
            activity_type="DOCUMENT_STUDIED",
            document_id=document_id,
            concepts=[
                item["concept"]
                for item in knowledge
            ],
        )

        # -----------------------------------------------------
        # Ingest chunks for RAG
        # -----------------------------------------------------

        chunks = ingestion_service.process(
            document_id=document_id,
            file_path=destination,
        )

        # -----------------------------------------------------
        # Index chunks in learner-specific Chroma
        # -----------------------------------------------------

        rag_service.index_chunks(
            chunks=chunks,
            learner_id=learner_id,
        )

        logger.info(
            "RAG indexed "
            "learner_id=%s document_id=%s chunks=%d",
            learner_id,
            document_id,
            len(chunks),
        )

        # -----------------------------------------------------
        # Return success
        # -----------------------------------------------------

        return DocumentResponse(
            document_id=document_id,
            filename=filename,
            file_type=extension,
            page_count=len(pages),
            status="processed",
        )

    except HTTPException:
        raise

    except Exception as exc:

        logger.exception(
            "Document processing failed: %s",
            filename,
        )

        destination.unlink(
            missing_ok=True
        )

        raise HTTPException(
            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail="Failed to process document.",
        ) from exc


@router.get(
    "/{document_id}/content",
    response_model=DocumentContentResponse,
)
async def get_document_content(
    document_id: str,
) -> DocumentContentResponse:

    destination = (
        Path(settings.documents_dir)
        / f"{document_id}.pdf"
    )

    # ---------------------------------------------------------
    # Check document exists
    # ---------------------------------------------------------

    if not destination.exists():

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    try:

        pages = loader.load(
            destination,
            ".pdf",
        )

        return DocumentContentResponse(
            document_id=document_id,
            filename=destination.name,
            pages=pages,
        )

    except Exception as exc:

        logger.exception(
            "Failed to read document id=%s",
            document_id,
        )

        raise HTTPException(
            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail="Failed to read document.",
        ) from exc

