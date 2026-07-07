from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.models.upload import UploadResponse
from app.services.document_service import DocumentService


class FileService:
    def __init__(self, upload_dir: str = "uploads") -> None:
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.max_file_size = 1 * 1024 * 1024
        self.document_service = DocumentService()

    async def save_text_file(self, file: UploadFile) -> UploadResponse:
        filename = file.filename or "unknown"

        if not filename.endswith(".txt"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .txt files are supported",
            )

        content = await file.read()
        size = len(content)

        if size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty",
            )

        if size > self.max_file_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds 1MB limit",
            )

        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be a valid UTF-8 text file",
            ) from exc

        file_path = self.upload_dir / filename
        file_path.write_text(text, encoding="utf-8")

        document = self.document_service.create_document(
            filename=filename,
            file_path=str(file_path),
            content_type=file.content_type,
            size=size,
            char_count=len(text),
        )

        preview = text[:500]

        return UploadResponse(
            document_id=document.id,
            filename=filename,
            content_type=file.content_type,
            size=size,
            char_count=len(text),
            preview=preview,
        )