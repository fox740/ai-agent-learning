import sqlite3
from pathlib import Path

from app.models.document import DocumentResponse


class DocumentService:
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
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    content_type TEXT,
                    size INTEGER NOT NULL,
                    char_count INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def create_document(
        self,
        filename: str,
        file_path: str,
        content_type: str | None,
        size: int,
        char_count: int,
    ) -> DocumentResponse:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO documents (
                    filename,
                    file_path,
                    content_type,
                    size,
                    char_count
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (filename, file_path, content_type, size, char_count),
            )

            document_id = cursor.lastrowid

            cursor = conn.execute(
                """
                SELECT id, filename, file_path, content_type, size, char_count, created_at
                FROM documents
                WHERE id = ?
                """,
                (document_id,),
            )

            row = cursor.fetchone()

        if row is None:
            raise ValueError("Failed to create document")

        return self._row_to_document(row)

    def list_documents(self) -> list[DocumentResponse]:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT id, filename, file_path, content_type, size, char_count, created_at
                FROM documents
                ORDER BY id DESC
                """
            )

            rows = cursor.fetchall()

        return [self._row_to_document(row) for row in rows]

    def get_document(self, document_id: int) -> DocumentResponse | None:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT id, filename, file_path, content_type, size, char_count, created_at
                FROM documents
                WHERE id = ?
                """,
                (document_id,),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_document(row)

    def _row_to_document(self, row: tuple) -> DocumentResponse:
        return DocumentResponse(
            id=row[0],
            filename=row[1],
            file_path=row[2],
            content_type=row[3],
            size=row[4],
            char_count=row[5],
            created_at=str(row[6]),
        )