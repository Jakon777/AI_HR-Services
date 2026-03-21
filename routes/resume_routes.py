import os
import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from core.resume_parser import parse_resume

router = APIRouter(prefix="/resume")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/parse")
async def parse(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix or ".pdf"
    safe_name = f"{uuid.uuid4().hex}{suffix}"
    path = os.path.join(UPLOAD_FOLDER, safe_name)

    try:
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        data = parse_resume(path)
        return data
    finally:
        if os.path.isfile(path):
            try:
                os.remove(path)
            except OSError:
                pass
