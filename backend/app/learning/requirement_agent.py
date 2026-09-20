import json
import logging
import os

from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import get_settings
from app.schemas.learning import TopicRequirements


logger = logging.getLogger(__name__)


class RequirementAgent:

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

    def analyze(self, topic: str) -> TopicRequirements:

        topic = topic.strip()

        if not topic:
            raise ValueError("Topic cannot be empty.")

        prompt = f"""
You are a general-purpose learning prerequisite analyzer.

Your job is to determine what concepts a learner genuinely needs
to understand the requested topic.

TOPIC:
{topic}

IMPORTANT:

This is NOT necessarily a programming or computer-science topic.

The topic may belong to ANY domain, such as:

- Computer Science
- Programming
- Mathematics
- Physics
- Biology
- Chemistry
- Engineering
- Construction
- Economics
- History
- Business
- Finance
- or any other educational domain.

First identify the DOMAIN of the topic internally.

Then identify prerequisites appropriate for THAT DOMAIN.

--------------------------------------------------
CORE RULES
--------------------------------------------------

1. Return ONLY concepts that are genuinely necessary to understand
   the requested topic.

2. Concepts must be semantically relevant to the topic.

3. NEVER add concepts merely because they are common concepts
   from another domain.

4. NEVER assume that the topic is about programming,
   data structures, algorithms, or computer science.

5. Do NOT include unrelated concepts.

6. Do NOT reuse concepts from previous requests.

7. Each requirement must be independently relevant to the
   current topic.

8. Prefer standard, recognizable concept names.

9. Keep the prerequisite list focused.

10. Usually return between 3 and 8 prerequisites.

--------------------------------------------------
DOMAIN-SPECIFIC GUIDANCE
--------------------------------------------------

For programming/computer-science topics, prerequisites may include:

- data structures
- algorithms
- programming concepts
- system concepts
- implementation concepts

Example:

TOPIC: LRU Cache

Possible prerequisites:

HashMap
Doubly Linked List
Cache
Eviction Policy
O(1) Lookup

For a construction/engineering topic, prerequisites may include:

- planning
- structural concepts
- materials
- engineering principles
- construction processes
- safety concepts

Example:

TOPIC: How to build a building

Possible prerequisites:

Building Planning
Structural Analysis
Foundation
Construction Materials
Construction Methods
Building Information Modeling

Do NOT include programming concepts such as:

HashMap
Doubly Linked List
Eviction Policy
O(1) Lookup

unless the requested topic itself genuinely requires them.

For mathematics, prioritize:

- definitions
- mathematical principles
- formulas
- prerequisite mathematical concepts

For science, prioritize:

- fundamental scientific concepts
- laws
- mechanisms
- prerequisite theories

--------------------------------------------------
RELEVANCE CHECK
--------------------------------------------------

Before returning each concept, ask internally:

"Would understanding this concept actually help the learner
understand the requested topic?"

If the answer is NO, remove it.

Also ask:

"Does this concept belong to the same domain as the requested topic?"

If the answer is NO, remove it unless the concept is genuinely
cross-domain and necessary.

--------------------------------------------------
IMPORTANT ANTI-HALLUCINATION RULE
--------------------------------------------------

Do NOT force the examples above into every answer.

The examples are only demonstrations.

Generate requirements specifically for:

{topic}

Do not copy requirements from the examples.

--------------------------------------------------
OUTPUT
--------------------------------------------------

Return ONLY valid JSON.

Do not return markdown.
Do not return explanations outside the JSON.

Required format:

{{
    "topic": "{topic}",
    "requirements": [
        {{
            "concept": "Concept Name",
            "importance": 0.9,
            "reason": "Short explanation of why this concept is needed."
        }}
    ]
}}
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
                "Invalid JSON returned by requirement agent: %s",
                content,
            )

            raise ValueError(
                "Requirement agent returned invalid JSON."
            ) from exc

        return TopicRequirements.model_validate(data)