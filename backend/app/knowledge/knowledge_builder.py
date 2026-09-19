from pathlib import Path

from app.ingestion.ingestion_service import IngestionService
from app.knowledge.concept_extractor import ConceptExtractor
from app.knowledge.knowledge_store import KnowledgeStore
from app.knowledge.learner_store import LearnerStore


class KnowledgeBuilder:
    """
    Builds conceptual knowledge from a learner's document.

    Concepts are stored globally in the knowledge base,
    but are also explicitly associated with the learner
    who uploaded the document.
    """

    def __init__(
        self,
        ingestion_service: IngestionService | None = None,
        concept_extractor: ConceptExtractor | None = None,
        knowledge_store: KnowledgeStore | None = None,
        learner_store: LearnerStore | None = None,
    ) -> None:

        self.ingestion_service = (
            ingestion_service or IngestionService()
        )

        self.concept_extractor = (
            concept_extractor or ConceptExtractor()
        )

        self.knowledge_store = (
            knowledge_store or KnowledgeStore()
        )

        self.learner_store = (
            learner_store or LearnerStore()
        )

    def build(
        self,
        learner_id: int,
        document_id: str,
        file_path: Path,
    ) -> list[dict]:

        chunks = self.ingestion_service.process(
            document_id=document_id,
            file_path=file_path,
        )

        extracted_concepts: dict[str, int] = {}

        for chunk in chunks:

            extraction = (
                self.concept_extractor.extract(
                    chunk.text
                )
            )

            for concept in extraction.concepts:

                concept_id = (
                    self.knowledge_store.add_concept(
                        name=concept.name,
                        description=concept.description,
                    )
                )

                extracted_concepts[
                    concept.name
                ] = concept_id

                self.knowledge_store.add_source(
                    concept_id=concept_id,
                    document_id=document_id,
                    page_number=chunk.page_number,
                )

                # ----------------------------------
                # Associate concept with THIS learner
                # ----------------------------------

                self.learner_store.add_known_concept(
                    learner_id=learner_id,
                    concept_id=concept_id,
                    evidence=(
                        f"{document_id} "
                        f"page {chunk.page_number}"
                    ),
                )

            # --------------------------------------
            # Relationships
            # --------------------------------------

            for relationship in (
                extraction.relationships
            ):

                source_id = extracted_concepts.get(
                    relationship.source
                )

                target_id = extracted_concepts.get(
                    relationship.target
                )

                if (
                    source_id is None
                    or target_id is None
                ):
                    continue

                self.knowledge_store.add_relationship(
                    source_concept_id=source_id,
                    target_concept_id=target_id,
                    relationship_type=(
                        relationship.relationship_type
                    ),
                )

        return [
            {
                "concept": name,
                "concept_id": concept_id,
            }
            for name, concept_id
            in extracted_concepts.items()
        ]