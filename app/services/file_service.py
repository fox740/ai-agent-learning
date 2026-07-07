from pathlib import Path

from fastapi import UploadFile

from app.models.upload import UploadResponse


class FileService:
    def __init__(self, upload_dir: str = "uploads") -> None:
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_text_file(self, file: UploadFile) -> UploadResponse:
        content = await file.read()
        size = len(content)

        text = content.decode("utf-8")

        file_path = self.upload_dir / file.filename

        file_path.write_text(text, encoding="utf-8")

        preview = text[:500]

        return UploadResponse(
            filename=file.filename or "unknown",
            content_type=file.content_type,
            size=size,
            preview=preview,
        )