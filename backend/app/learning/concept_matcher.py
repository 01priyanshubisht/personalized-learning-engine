from dataclasses import dataclass


@dataclass
class ConceptMatch:
    required_concept: str
    matched_concept: str | None
    known: bool
    evidence: str | None
    match_type: str


class ConceptMatcher:
    """
    Determines whether a required concept already exists
    in the learner's knowledge base.
    """

    ALIASES = {
        "hash map": "hashmap",
        "hashmap": "hashmap",
        "doubly linked list": "doubly linked list",
        "dll": "doubly linked list",
        "o(1) lookup": "o(1) lookup",
        "constant time lookup": "o(1) lookup",
        "eviction policy": "eviction policy",
        "cache": "cache",
        "least recently used": "lru",
        "lru": "lru",
        "lru cache": "lru cache",
    }

    @staticmethod
    def normalize(concept: str) -> str:
        return " ".join(
            concept.strip().lower().split()
        )

    def canonicalize(self, concept: str) -> str:
        normalized = self.normalize(concept)

        return self.ALIASES.get(
            normalized,
            normalized,
        )

    def match(
        self,
        required_concept: str,
        learner_concepts: list[dict],
    ) -> ConceptMatch:

        required_canonical = self.canonicalize(
            required_concept
        )

        for learner_concept in learner_concepts:

            learner_name = learner_concept[
                "concept_name"
            ]

            learner_canonical = self.canonicalize(
                learner_name
            )

            if learner_canonical != required_canonical:
                continue

            return ConceptMatch(
                required_concept=required_concept,
                matched_concept=learner_name,
                known=True,
                evidence=learner_concept.get(
                    "evidence"
                ),
                match_type="exact_or_alias",
            )

        return ConceptMatch(
            required_concept=required_concept,
            matched_concept=None,
            known=False,
            evidence=None,
            match_type="no_match",
        )