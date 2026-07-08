import json
import sqlite3
from pathlib import Path

from app.models.vector import ChunkEmbeddingResponse

import math
from app.models.rag import RAGSource


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
    def search_similar_chunks(
        self,
        query_embedding: list[float],
        top_k: int = 3,
        document_id: int | None = None,
        min_score: float = 0.0,
    ) -> list[RAGSource]:
        sql = """
            SELECT
                ce.chunk_id,
                ce.document_id,
                ce.embedding,
                dc.chunk_index,
                dc.content,
                d.filename
            FROM chunk_embeddings ce
            JOIN document_chunks dc
                ON ce.chunk_id = dc.id
            JOIN documents d
                ON ce.document_id = d.id
        """

        params: tuple = ()

        if document_id is not None:
            sql += """
            WHERE ce.document_id = ?
            """
            params = (document_id,)

        with self._connect() as conn:
            cursor = conn.execute(sql, params)
            rows = cursor.fetchall()

        scored_sources: list[RAGSource] = []
        seen_contents: set[str] = set()

        for row in rows:
            chunk_id = row[0]
            source_document_id = row[1]
            chunk_embedding = json.loads(row[2])
            chunk_index = row[3]
            content = row[4]
            filename = row[5]

            normalized_content = content.strip()

            if normalized_content in seen_contents:
                continue

            score = self._cosine_similarity(
                query_embedding,
                chunk_embedding,
            )

            if score < min_score:
                continue

            seen_contents.add(normalized_content)

            scored_sources.append(
                RAGSource(
                    source_index=0,
                    chunk_id=chunk_id,
                    document_id=source_document_id,
                    filename=filename,
                    chunk_index=chunk_index,
                    score=score,
                    content=content,
                )
            )

        scored_sources.sort(key=lambda source: source.score, reverse=True)

        top_sources = scored_sources[:top_k]

        return [
            source.model_copy(update={"source_index": index})
            for index, source in enumerate(top_sources, start=1)
        ]

    def _cosine_similarity(
        self,
        vector_a: list[float],
        vector_b: list[float],
    ) -> float:
        if len(vector_a) != len(vector_b):
            raise ValueError("Embedding dimensions do not match")

        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
        norm_a = math.sqrt(sum(a * a for a in vector_a))
        norm_b = math.sqrt(sum(b * b for b in vector_b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)