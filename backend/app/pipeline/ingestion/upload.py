from fastapi import File, UploadFile, HTTPException
import os
from app.pipeline.ingestion import converter as cv
from pathlib import Path
import magic
import uuid

FILE_TYPES = ['.docx', '.doc', '.pdf']
MAX_FILE_SIZE = 10 * 1024 * 1024
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword",
}


async def upload_file(file: UploadFile = File(...)):
    # check that a file was sent
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail='NO File Found!'
        )
    
    file_name = Path(file.filename).name
    file_ext = Path(file.filename).suffix.lower()
    new_file_name = f'{uuid.uuid4()}{file_ext}'
    file_path = os.path.join(UPLOAD_DIR, new_file_name)
    file_size = 0

    # Check the file type
    if file_ext not in FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f'Invalid file type {file_ext}, only .pdf, .docx and .doc allowed!'
        )  
    
    # Check the file size
    try:
        with open(file_path, 'wb') as f:
            while bits := await file.read(1024 * 1024):
                file_size += len(bits)
                if file_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=400,
                        detail='File too Large. maximum file size is 10mb'
                    )
                f.write(bits)
    
    # Checking the file headers
        file_type = get_mime_type(file_path)
        if file_type not in ALLOWED_MIME_TYPES:
            os.remove(file_path)
            raise HTTPException(
                status_code= 400,
                detail= f'Invalid file type'
            )
        
        file_content = await cv.converter(file_path)
        return file_content
        # return 'file upload successful'
    
    except Exception:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise
    

def get_mime_type(filepath: str) -> str:
    mime = magic.Magic(mime=True)
    return mime.from_file(filepath)