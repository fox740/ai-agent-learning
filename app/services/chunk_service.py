import sqlite3
from pathlib import Path

from app.models.chunk import ChunkResponse
from app.models.document import DocumentResponse


class ChunkService:
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
                CREATE TABLE IF NOT EXISTS document_chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_id INTEGER NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    char_count INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def create_chunks(
        self,
        document: DocumentResponse,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ) -> list[ChunkResponse]:
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        file_path = Path(document.file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Document file not found: {document.file_path}")

        text = file_path.read_text(encoding="utf-8")

        chunks = self._split_text(
            text=text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        with self._connect() as conn:
            conn.execute(
                """
                DELETE FROM document_chunks
                WHERE document_id = ?
                """,
                (document.id,),
            )

            for chunk_index, chunk_content in enumerate(chunks):
                conn.execute(
                    """
                    INSERT INTO document_chunks (
                        document_id,
                        chunk_index,
                        content,
                        char_count
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        document.id,
                        chunk_index,
                        chunk_content,
                        len(chunk_content),
                    ),
                )

        return self.get_chunks(document.id)

    def get_chunks(self, document_id: int) -> list[ChunkResponse]:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT id, document_id, chunk_index, content, char_count, created_at
                FROM document_chunks
                WHERE document_id = ?
                ORDER BY chunk_index ASC
                """,
                (document_id,),
            )

            rows = cursor.fetchall()

        return [self._row_to_chunk(row) for row in rows]

    def _split_text(
        self,
        text: str,
        chunk_size: int,
        chunk_overlap: int,
    ) -> list[str]:
        chunks: list[str] = []

        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start = end - chunk_overlap

        return chunks

    def _row_to_chunk(self, row: tuple) -> ChunkResponse:
        return ChunkResponse(
            id=row[0],
            document_id=row[1],
            chunk_index=row[2],
            content=row[3],
            char_count=row[4],
            created_at=str(row[5]),
        )