import json

import ollama

from app.learning.learning_plan import LearningStep
from app.schemas.teaching import (
    TeachingResponse,
    TeachingSection,
    TeachingSource,
)


class TeachingAgent:
    """
    Generates a personalized lesson.

    Known concepts:
        Use learner's retrieved material.

    Unknown concepts:
        Explain using the LLM's general knowledge.

    Target topic:
        Connect all required concepts into one lesson.
    """

    def __init__(
        self,
        model: str = "llama3.2:3b",
    ) -> None:
        self.model = model

    def teach(
        self,
        topic: str,
        learning_plan: list[LearningStep],
        retrieved_material: list[dict] | None = None,
    ) -> TeachingResponse:

        retrieved_material = (
            retrieved_material or []
        )

        # -----------------------------------------
        # Build learner material context
        # -----------------------------------------

        learner_material_context = ""

        if retrieved_material:

            learner_material_context = (
                "\n\nLEARNER'S PREVIOUS MATERIAL:\n"
            )

            for index, material in enumerate(
                retrieved_material,
                start=1,
            ):

                learner_material_context += (
                    f"\n[{index}] "
                    f"Concept: "
                    f"{material.get('retrieved_for')}\n"
                )

                learner_material_context += (
                    f"Document: "
                    f"{material.get('document_id')}\n"
                )

                learner_material_context += (
                    f"Page: "
                    f"{material.get('page_number')}\n"
                )

                learner_material_context += (
                    f"Content:\n"
                    f"{material.get('text', '')}\n"
                )

        # -----------------------------------------
        # Build learning plan context
        # -----------------------------------------

        learning_plan_context = ""

        for step in learning_plan:

            learning_plan_context += (
                f"\n- Concept: {step.concept}\n"
                f"  Action: {step.action}\n"
                f"  Importance: {step.importance}\n"
                f"  Reason: {step.reason}\n"
            )

            if step.evidence:
                learning_plan_context += (
                    f"  Learner evidence: "
                    f"{step.evidence}\n"
                )

        # -----------------------------------------
        # Prompt
        # -----------------------------------------

        prompt = f"""
You are a personalized teaching agent.

The learner asked:

"{topic}"

Your job is to teach the target topic by connecting
the required concepts.

IMPORTANT PERSONALIZATION RULE:

There are two types of concepts.

1. KNOWN CONCEPTS
Their learning plan action is:
"use_learner_material"

For these concepts:
- Use the learner's retrieved material provided below.
- Use the learner's terminology or definitions when useful.
- Do not unnecessarily teach the concept from scratch.
- Use it as a familiar building block.

2. UNKNOWN CONCEPTS
Their learning plan action is:
"teach_new"

For these concepts:
- The learner has no known material for the concept.
- Explain the concept using your general knowledge.
- Teach it clearly as a new concept.
- Do NOT claim that it came from the learner's material.

3. TARGET TOPIC
The target topic is:
"{topic}"

After explaining any necessary new concepts,
connect them with the concepts the learner already knows.

Do not assume that a concept is known merely because
it is related to another known concept.

IMPORTANT ACCURACY RULE:

For LRU Cache:
- LRU means Least Recently Used.
- Eviction is based on RECENCY, not frequency.
- A standard O(1) LRU Cache commonly combines a HashMap
  with a Doubly Linked List.
- HashMap provides fast lookup.
- Doubly Linked List maintains recency order.
- When capacity is exceeded, the least recently used
  item is removed.

Use the learner material only as supporting context.
Do not invent learner knowledge.

LEARNING PLAN:
{learning_plan_context}

{learner_material_context}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "topic": "{topic}",
    "introduction": "short personalized introduction",
    "sections": [
        {{
            "title": "section title",
            "content": "section explanation"
        }}
    ],
    "summary": "short summary",
    "sources": [
        {{
            "document_id": "document id or null",
            "page_number": 1
        }}
    ]
}}

Rules:
- Do not use markdown code fences.
- Do not include programming code.
- Keep the explanation technically accurate.
- Mention when a concept is being introduced as new.
- Use learner material for known concepts when available.
- Include sources only when learner material was actually used.
"""

        # -----------------------------------------
        # Call Ollama
        # -----------------------------------------

        response = ollama.chat(
            model=self.model,
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

        raw_content = response["message"][
            "content"
        ].strip()

        # -----------------------------------------
        # Clean possible markdown fences
        # -----------------------------------------

        if raw_content.startswith(
            "```json"
        ):
            raw_content = raw_content[
                7:
            ].strip()

        elif raw_content.startswith("```"):
            raw_content = raw_content[
                3:
            ].strip()

        if raw_content.endswith("```"):
            raw_content = raw_content[
                :-3
            ].strip()

        # -----------------------------------------
        # Extract JSON
        # -----------------------------------------

        start = raw_content.find("{")
        end = raw_content.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(
                "Teaching Agent did not return valid JSON."
            )

        raw_content = raw_content[
            start:end + 1
        ]

        data = json.loads(raw_content)

        # -----------------------------------------
        # Validate response
        # -----------------------------------------

        sections = [
            TeachingSection(**section)
            for section in data.get(
                "sections",
                [],
            )
        ]

        sources = [
            TeachingSource(**source)
            for source in data.get(
                "sources",
                [],
            )
        ]

        return TeachingResponse(
            topic=data["topic"],
            introduction=data["introduction"],
            sections=sections,
            summary=data["summary"],
            sources=sources,
        )