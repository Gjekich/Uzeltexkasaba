import os
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/upload",
    tags=["Uploads"]
)

UPLOAD_DIR = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".png", ".jpg", ".jpeg", ".webp"}


@router.post("/")
def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Validate file extension
    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Noto'g'ri fayl turi. Ruxsat berilgan turlar: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Create a unique file name
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Faylni yuklashda xatolik yuz berdi: {str(e)}")

    # Return relative URL
    file_url = f"/static/uploads/{unique_filename}"
    return {
        "filename": file.filename,
        "url": file_url
    }
