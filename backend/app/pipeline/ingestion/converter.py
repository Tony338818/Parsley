import PyPDF2
import docx2txt
from pathlib import Path

async def converter(file_path: str) -> str:
    with open(file_path, 'rb') as f:
        # get file extension
        file_ext = Path(file_path).suffix.lower()
        text = ''

        if file_ext == '.pdf':
            reader = PyPDF2.PdfReader(f)
            for word in reader.pages:
                text += word.extract_text()
            return text
        
        elif file_ext in ['.docx', '.doc']:
            reader = docx2txt.process(f)
            return reader
        
        else: 
            raise ValueError(f"Unsupported file type: {file_ext}. Only PDF and Word documents are supported.")