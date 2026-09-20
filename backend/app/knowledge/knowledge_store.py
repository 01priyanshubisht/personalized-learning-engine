import sqlite3
from pathlib import Path


class KnowledgeStore:
    def __init__(self, database_path: str = "data/knowledge.db") -> None:
        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize_database()

    def _get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)

        connection.row_factory = sqlite3.Row

        return connection

    def _initialize_database(self) -> None:
        with self._get_connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS concepts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS concept_sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    concept_id INTEGER NOT NULL,
                    document_id TEXT NOT NULL,
                    page_number INTEGER NOT NULL,

                    FOREIGN KEY (concept_id)
                        REFERENCES concepts(id),

                    UNIQUE (
                        concept_id,
                        document_id,
                        page_number
                    )
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_concept_id INTEGER NOT NULL,
                    target_concept_id INTEGER NOT NULL,
                    relationship_type TEXT NOT NULL,

                    FOREIGN KEY (source_concept_id)
                        REFERENCES concepts(id),

                    FOREIGN KEY (target_concept_id)
                        REFERENCES concepts(id),

                    UNIQUE (
                        source_concept_id,
                        target_concept_id,
                        relationship_type
                    )
                )
                """
            )

            connection.commit()

    def add_concept(
        self,
        name: str,
        description: str | None = None,
    ) -> int:
        name = name.strip()

        if not name:
            raise ValueError("Concept name cannot be empty.")

        with self._get_connection() as connection:
            connection.execute(
                """
                INSERT INTO concepts (name, description)
                VALUES (?, ?)
                ON CONFLICT(name)
                DO UPDATE SET
                    description = COALESCE(
                        excluded.description,
                        concepts.description
                    )
                """,
                (name, description),
            )

            row = connection.execute(
                """
                SELECT id
                FROM concepts
                WHERE name = ?
                """,
                (name,),
            ).fetchone()

            connection.commit()

            if row is None:
                raise RuntimeError(
                    f"Failed to create concept: {name}"
                )

            return int(row["id"])

    def add_source(
        self,
        concept_id: int,
        document_id: str,
        page_number: int,
    ) -> None:
        with self._get_connection() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO concept_sources (
                    concept_id,
                    document_id,
                    page_number
                )
                VALUES (?, ?, ?)
                """,
                (
                    concept_id,
                    document_id,
                    page_number,
                ),
            )

            connection.commit()

    def add_relationship(
        self,
        source_concept_id: int,
        target_concept_id: int,
        relationship_type: str,
    ) -> None:
        relationship_type = relationship_type.strip()

        if not relationship_type:
            raise ValueError(
                "Relationship type cannot be empty."
            )

        with self._get_connection() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO relationships (
                    source_concept_id,
                    target_concept_id,
                    relationship_type
                )
                VALUES (?, ?, ?)
                """,
                (
                    source_concept_id,
                    target_concept_id,
                    relationship_type,
                ),
            )

            connection.commit()

    def list_concepts(self) -> list[dict]:
        with self._get_connection() as connection:
            rows = connection.execute(
                """
                SELECT id, name, description
                FROM concepts
                ORDER BY name
                """
            ).fetchall()

            return [dict(row) for row in rows]