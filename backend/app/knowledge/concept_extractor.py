import json
import logging

from ollama import Client

from app.schemas.knowledge import ConceptExtractionResult

logger = logging.getLogger(__name__)


class ConceptExtractor:
    def __init__(
        self,
        model_name: str = "llama3.2:3b",
        host: str = "http://localhost:11434",
    ) -> None:
        self.model_name = model_name
        self.client = Client(host=host)

    def extract(self, text: str) -> ConceptExtractionResult:
        if not text.strip():
            return ConceptExtractionResult(
                concepts=[],
                relationships=[],
            )

        prompt = f"""
You are a knowledge extraction engine for a personalized learning system.

Analyze the educational text below.

Extract:
1. Important technical concepts.
2. Explicit relationships between those concepts.

Rules:

CONCEPTS:
- Extract meaningful technical concepts.
- Do not extract ordinary words.
- Do not invent concepts.
- Keep descriptions grounded in the supplied text.
- Confidence must be between 0 and 1.

RELATIONSHIPS:
- Only extract relationships that are supported by the text.
- Do not infer relationships from general knowledge.
- Use simple relationship types such as:
  - is_a
  - variant_of
  - consists_of
  - uses
  - requires
  - related_to
- source and target must correspond to extracted concepts.
- Confidence must be between 0 and 1.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "concepts": [
        {{
            "name": "Concept Name",
            "description": "Short grounded description",
            "confidence": 0.95
        }}
    ],
    "relationships": [
        {{
            "source": "Concept A",
            "target": "Concept B",
            "relationship_type": "requires",
            "confidence": 0.90
        }}
    ]
}}

TEXT:
{text}
"""

        response = self.client.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            options={
                "temperature": 0,
            },
        )

        content = response["message"]["content"].strip()

        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            logger.error(
                "Invalid JSON returned by model: %s",
                content,
            )
            raise ValueError(
                "Concept extractor returned invalid JSON."
            ) from exc

        return ConceptExtractionResult.model_validate(data)