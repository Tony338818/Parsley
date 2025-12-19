from fastapi import File, UploadFile
import os
from app.pipeline.ingestion import converter as cv
from pathlib import Path


UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        return 'Please provide a file'
    file_ext = Path(file.filename).suffix.lower()
    if not file_ext in ['.docx', '.doc', '.pdf']:
        raise ValueError(f"Unsupported file type: {file_ext}. Only PDF and Word documents are supported.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, 'wb') as f:
        context = await file.read()
        f.write(context)

    text = await cv.converter(file_path)
    # return {
    #     "filename": file.filename,
    #     "saved_to": file_path
    # }
    return text
    