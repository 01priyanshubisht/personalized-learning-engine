from app.learning.gap_detector import GapDetector
from app.learning.learning_plan import LearningPlanBuilder
from app.learning.requirement_agent import RequirementAgent
from app.learning.teaching_agent import TeachingAgent
from app.retrieval.learning_retriever import LearningRetriever
from app.knowledge.learner_store import LearnerStore


class LearningService:

    def __init__(
        self,
        requirement_agent: RequirementAgent | None = None,
        gap_detector: GapDetector | None = None,
        plan_builder: LearningPlanBuilder | None = None,
        teaching_agent: TeachingAgent | None = None,
        learning_retriever: LearningRetriever | None = None,
        learner_store: LearnerStore | None = None,
    ) -> None:

        self.requirement_agent = (
            requirement_agent or RequirementAgent()
        )

        self.gap_detector = (
            gap_detector or GapDetector()
        )

        self.plan_builder = (
            plan_builder or LearningPlanBuilder()
        )

        self.teaching_agent = (
            teaching_agent or TeachingAgent()
        )

        self.learning_retriever = (
            learning_retriever or LearningRetriever()
        )

        self.learner_store = (
            learner_store or LearnerStore()
        )

    def teach(
        self,
        learner_id: int,
        topic: str,
        use_previous_material: bool = True,
    ) -> dict:

        topic = topic.strip()

        if not topic:
            raise ValueError("Topic cannot be empty.")

        # -------------------------------------------------
        # 1. Understand what is required to learn the topic
        # -------------------------------------------------

        requirements = self.requirement_agent.analyze(topic)

        # -------------------------------------------------
        # 2. Compare requirements with learner knowledge
        # -------------------------------------------------

        gaps = self.gap_detector.detect(
            learner_id=learner_id,
            topic_requirements=requirements,
        )

        # -------------------------------------------------
        # 3. Build learning sequence
        # -------------------------------------------------

        learning_plan = self.plan_builder.build(
            topic=topic,
            gaps=gaps,
        )

        # -------------------------------------------------
        # 4. Retrieve only learner's previous material
        # -------------------------------------------------

        retrieved_material = []

        if use_previous_material:

            queries = [
                gap.concept
                for gap in gaps
                if gap.known
            ]
            if topic not in queries:
                queries.append(topic)

            retrieved_material = (
                self.learning_retriever.retrieve_for_concepts(
                    learner_id=learner_id,
                    concepts=queries,
                    top_k_per_concept=2,
                )
            )

        # -------------------------------------------------
        # 5. Generate personalized teaching
        # -------------------------------------------------

        lesson = self.teaching_agent.teach(
            topic=topic,
            learning_plan=learning_plan,
            retrieved_material=retrieved_material,
        )

        self.learner_store.add_history(
            learner_id=learner_id,
            activity_type="TOPIC_STUDIED",
            topic=topic,
            concepts=[
                gap.concept
                for gap in gaps
            ],
        )

        # -------------------------------------------------
        # 6. Return complete learning result
        # -------------------------------------------------

        return {
            "learner_id": learner_id,
            "topic": topic,
            "requirements": requirements,
            "gaps": gaps,
            "learning_plan": learning_plan,
            "retrieved_material": retrieved_material,
            "lesson": lesson,
        }