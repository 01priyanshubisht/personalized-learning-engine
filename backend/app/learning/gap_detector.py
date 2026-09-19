from dataclasses import dataclass

from app.knowledge.learner_store import LearnerStore
from app.learning.concept_matcher import ConceptMatcher
from app.schemas.learning import TopicRequirements


@dataclass
class ConceptGap:
    concept: str
    importance: float
    reason: str
    known: bool
    evidence: str | None


class GapDetector:

    def __init__(
        self,
        learner_store: LearnerStore | None = None,
        concept_matcher: ConceptMatcher | None = None,
    ) -> None:

        self.learner_store = (
            learner_store or LearnerStore()
        )

        self.concept_matcher = (
            concept_matcher or ConceptMatcher()
        )

    def detect(
        self,
        learner_id: int,
        topic_requirements: TopicRequirements,
    ) -> list[ConceptGap]:

        learner_concepts = (
            self.learner_store.get_learner_concepts(
                learner_id
            )
        )

        gaps: list[ConceptGap] = []

        for requirement in (
            topic_requirements.requirements
        ):

            match = self.concept_matcher.match(
                required_concept=requirement.concept,
                learner_concepts=learner_concepts,
            )

            gaps.append(
                ConceptGap(
                    concept=requirement.concept,
                    importance=requirement.importance,
                    reason=requirement.reason,
                    known=match.known,
                    evidence=match.evidence,
                )
            )

        return gaps