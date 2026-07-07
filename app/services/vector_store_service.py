import json
import sqlite3
from pathlib import Path

from app.models.vector import ChunkEmbeddingResponse


class VectorStoreService:
    def __init__(self, db_path: str = "data/chat_history.db") -> None:
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chunk_embeddings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chunk_id INTEGER NOT NULL,
                    document_id INTEGER NOT NULL,
                    embedding TEXT NOT NULL,
                    dimension INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def save_embedding(
        self,
        chunk_id: int,
        document_id: int,
        embedding: list[float],
    ) -> ChunkEmbeddingResponse:
        embedding_json = json.dumps(embedding)

        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO chunk_embeddings (
                    chunk_id,
                    document_id,
                    embedding,
                    dimension
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    chunk_id,
                    document_id,
                    embedding_json,
                    len(embedding),
                ),
            )

            embedding_id = cursor.lastrowid

            cursor = conn.execute(
                """
                SELECT id, chunk_id, document_id, embedding, dimension, created_at
                FROM chunk_embeddings
                WHERE id = ?
                """,
                (embedding_id,),
            )

            row = cursor.fetchone()

        if row is None:
            raise ValueError("Failed to save chunk embedding")

        return self._row_to_embedding(row)

    def delete_embeddings_by_document(self, document_id: int) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                DELETE FROM chunk_embeddings
                WHERE document_id = ?
                """,
                (document_id,),
            )

    def get_embeddings_by_document(
        self,
        document_id: int,
    ) -> list[ChunkEmbeddingResponse]:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT id, chunk_id, document_id, embedding, dimension, created_at
                FROM chunk_embeddings
                WHERE document_id = ?
                ORDER BY id ASC
                """,
                (document_id,),
            )

            rows = cursor.fetchall()

        return [self._row_to_embedding(row) for row in rows]

    def _row_to_embedding(self, row: tuple) -> ChunkEmbeddingResponse:
        embedding = json.loads(row[3])

        return ChunkEmbeddingResponse(
            id=row[0],
            chunk_id=row[1],
            document_id=row[2],
            embedding=embedding,
            dimension=row[4],
            created_at=str(row[5]),
        )