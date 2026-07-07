from fastapi import APIRouter, File, UploadFile

from app.models.upload import UploadResponse
from app.services.file_service import FileService

router = APIRouter(prefix="/upload", tags=["upload"])

file_service = FileService()


@router.post("", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)) -> UploadResponse:
    return await file_service.save_text_file(file)