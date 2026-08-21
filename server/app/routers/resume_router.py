from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.services.parser_service import ParserService
from app.database.db import get_db
from app.schemas.resume import ResumeResponse
from app.services.resume_service import ResumeService
from app.services.file_service import FileService

router = APIRouter()

@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
    content = await file.read()

    # Save the uploaded file
    file_path = FileService.save_file(file.filename, content)

    # Extract text from the PDF
    extracted_text = ParserService.extract_resume(file_path=file_path)

    # Create a new resume entry in the database
    resume = ResumeService.create(db, filename=file.filename, file_path=file_path, extracted_text=extracted_text)

    return resume
