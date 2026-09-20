from app.learning.requirement_agent import RequirementAgent


def main() -> None:
    agent = RequirementAgent()

    topic = "LRU Cache"

    print(f"Analyzing topic: {topic}\n")

    result = agent.analyze(topic)

    print("Required concepts:")

    for requirement in result.requirements:
        print(
            f"- {requirement.concept} | "
            f"importance={requirement.importance} | "
            f"reason={requirement.reason}"
        )


if __name__ == "__main__":
    main()