import sqlite3

from app.knowledge.learner_store import LearnerStore


def main() -> None:
    store = LearnerStore()

    with store._get_connection() as connection:
        connection.execute(
            """
            DELETE FROM learner_concepts
            WHERE learner_id = ?
            """,
            (1,),
        )
        connection.commit()

    print("✅ Learner 1 knowledge cleared.")


if __name__ == "__main__":
    main()