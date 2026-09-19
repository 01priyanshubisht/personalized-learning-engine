from dataclasses import dataclass

from app.learning.gap_detector import ConceptGap


@dataclass
class LearningStep:
    concept: str
    action: str
    importance: float
    reason: str
    evidence: str | None


class LearningPlanBuilder:

    def build(
        self,
        topic: str,
        gaps: list[ConceptGap],
    ) -> list[LearningStep]:

        steps: list[LearningStep] = []

        for gap in gaps:

            if gap.known:
                action = "use_learner_material"
            else:
                action = "teach_new"

            steps.append(
                LearningStep(
                    concept=gap.concept,
                    action=action,
                    importance=gap.importance,
                    reason=gap.reason,
                    evidence=gap.evidence,
                )
            )

        steps.append(
            LearningStep(
                concept=topic,
                action="teach_topic",
                importance=1.0,
                reason=(
                    "Target topic requested "
                    "by the learner."
                ),
                evidence=None,
            )
        )

        return steps