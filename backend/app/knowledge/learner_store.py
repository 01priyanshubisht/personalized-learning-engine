import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


class LearnerStore:
    def __init__(
        self,
        database_path: str = "data/knowledge.db",
    ) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        self._initialize_database()

    def _get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.database_path
        )
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_database(self) -> None:
        with self._get_connection() as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS learners (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS learner_concepts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    learner_id INTEGER NOT NULL,
                    concept_id INTEGER NOT NULL,
                    mastery REAL NOT NULL
                        CHECK (mastery >= 0.0 AND mastery <= 1.0),
                    status TEXT NOT NULL,
                    evidence TEXT,
                    updated_at TEXT NOT NULL,

                    FOREIGN KEY (learner_id)
                        REFERENCES learners(id),

                    FOREIGN KEY (concept_id)
                        REFERENCES concepts(id),

                    UNIQUE (
                        learner_id,
                        concept_id
                    )
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS study_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    learner_id INTEGER NOT NULL,
                    activity_type TEXT NOT NULL,
                    topic TEXT,
                    document_id TEXT,
                    concepts TEXT,
                    created_at TEXT NOT NULL,

                    FOREIGN KEY (learner_id)
                        REFERENCES learners(id)
                )
                """
            )

            connection.commit()

    def create_learner(
        self,
        name: str,
    ) -> int:

        name = name.strip()

        if not name:
            raise ValueError(
                "Learner name cannot be empty."
            )

        created_at = datetime.now(
            timezone.utc
        ).isoformat()

        with self._get_connection() as connection:

            cursor = connection.execute(
                """
                INSERT INTO learners (
                    name,
                    created_at
                )
                VALUES (?, ?)
                """,
                (
                    name,
                    created_at,
                ),
            )

            connection.commit()

            return int(cursor.lastrowid)

    def get_learner(
        self,
        learner_id: int,
    ) -> dict | None:

        with self._get_connection() as connection:

            row = connection.execute(
                """
                SELECT
                    id,
                    name,
                    created_at
                FROM learners
                WHERE id = ?
                """,
                (learner_id,),
            ).fetchone()

            if row is None:
                return None

            return dict(row)

    def set_concept_mastery(
        self,
        learner_id: int,
        concept_id: int,
        mastery: float,
        status: str,
        evidence: str | None = None,
    ) -> None:

        if not 0.0 <= mastery <= 1.0:
            raise ValueError(
                "Mastery must be between 0.0 and 1.0."
            )

        status = status.strip()

        if not status:
            raise ValueError(
                "Status cannot be empty."
            )

        updated_at = datetime.now(
            timezone.utc
        ).isoformat()

        with self._get_connection() as connection:

            connection.execute(
                """
                INSERT INTO learner_concepts (
                    learner_id,
                    concept_id,
                    mastery,
                    status,
                    evidence,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?)

                ON CONFLICT(
                    learner_id,
                    concept_id
                )
                DO UPDATE SET
                    mastery = excluded.mastery,
                    status = excluded.status,
                    evidence = excluded.evidence,
                    updated_at = excluded.updated_at
                """,
                (
                    learner_id,
                    concept_id,
                    mastery,
                    status,
                    evidence,
                    updated_at,
                ),
            )

            connection.commit()

    def add_known_concept(
        self,
        learner_id: int,
        concept_id: int,
        evidence: str | None = None,
    ) -> None:
        """
        Mark a concept as present in the learner's
        previously uploaded material.

        For the MVP, this does NOT mean measured mastery.
        It only means that the learner has material about
        this concept.
        """

        updated_at = datetime.now(
            timezone.utc
        ).isoformat()

        with self._get_connection() as connection:

            connection.execute(
                """
                INSERT INTO learner_concepts (
                    learner_id,
                    concept_id,
                    mastery,
                    status,
                    evidence,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?)

                ON CONFLICT(
                    learner_id,
                    concept_id
                )
                DO UPDATE SET
                    evidence = excluded.evidence,
                    status = excluded.status,
                    updated_at = excluded.updated_at
                """,
                (
                    learner_id,
                    concept_id,
                    0.0,
                    "known",
                    evidence,
                    updated_at,
                ),
            )

            connection.commit()

    def get_learner_concepts(
        self,
        learner_id: int,
    ) -> list[dict]:

        with self._get_connection() as connection:

            rows = connection.execute(
                """
                SELECT
                    lc.learner_id,
                    lc.concept_id,
                    c.name AS concept_name,
                    c.description,
                    lc.mastery,
                    lc.status,
                    lc.evidence,
                    lc.updated_at

                FROM learner_concepts lc

                JOIN concepts c
                    ON c.id = lc.concept_id

                WHERE lc.learner_id = ?

                ORDER BY c.name
                """,
                (learner_id,),
            ).fetchall()

            return [
                dict(row)
                for row in rows
            ]

    # =====================================================
    # STUDY HISTORY
    # =====================================================

    def add_history(
        self,
        learner_id: int,
        activity_type: str,
        topic: str | None = None,
        document_id: str | None = None,
        concepts: list[str] | None = None,
    ) -> int:

        activity_type = activity_type.strip()

        if not activity_type:
            raise ValueError(
                "Activity type cannot be empty."
            )

        created_at = datetime.now(
            timezone.utc
        ).isoformat()

        concepts_json = json.dumps(
            concepts or [],
            ensure_ascii=False,
        )

        with self._get_connection() as connection:

            cursor = connection.execute(
                """
                INSERT INTO study_history (
                    learner_id,
                    activity_type,
                    topic,
                    document_id,
                    concepts,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    learner_id,
                    activity_type,
                    topic,
                    document_id,
                    concepts_json,
                    created_at,
                ),
            )

            connection.commit()

            return int(cursor.lastrowid)

    def get_history(
        self,
        learner_id: int,
        limit: int = 50,
    ) -> list[dict]:

        if limit <= 0:
            raise ValueError(
                "Limit must be greater than 0."
            )

        with self._get_connection() as connection:

            rows = connection.execute(
                """
                SELECT
                    id,
                    learner_id,
                    activity_type,
                    topic,
                    document_id,
                    concepts,
                    created_at
                FROM study_history
                WHERE learner_id = ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (
                    learner_id,
                    limit,
                ),
            ).fetchall()

            history = []

            for row in rows:

                item = dict(row)

                item["concepts"] = json.loads(
                    item["concepts"] or "[]"
                )

                history.append(item)

            return history