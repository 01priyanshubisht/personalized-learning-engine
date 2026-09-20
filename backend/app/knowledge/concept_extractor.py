import json
import logging
import os

from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import get_settings
from app.schemas.knowledge import ConceptExtractionResult

logger = logging.getLogger(__name__)


class ConceptExtractor:
    def __init__(
        self,
        model_name: str | None = None,
        api_key: str | None = None,
    ) -> None:
        settings = get_settings()
        self.model_name = (
            model_name
            or os.getenv("GEMINI_MODEL")
            or getattr(settings, "gemini_model", "gemini-2.5-flash")
            or "gemini-2.5-flash"
        )
        self.api_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
            or getattr(settings, "gemini_api_key", None)
        )
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = genai.Client()

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

        @retry(
            stop=stop_after_attempt(5),
            wait=wait_exponential(multiplier=1, min=2, max=10),
            reraise=True,
        )
        def _generate_with_retry():
            return self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.0,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                ),
            )

        response = _generate_with_retry()

        content = response.text.strip()


        if content.startswith("```json"):
            content = content[7:].strip()
        elif content.startswith("```"):
            content = content[3:].strip()
        if content.endswith("```"):
            content = content[:-3].strip()

        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1:
            content = content[start : end + 1]

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