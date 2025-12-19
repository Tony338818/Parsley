import pypdf
import pymupdf
import docx2txt
from pathlib import Path

async def converter(filePath: str) -> str:
    # get the file extension
    file_ext = Path(filePath).suffix.lower()

    if file_ext == '.pdf':
        text = []
        with open(filePath, 'rb') as f:
            # reader = pypdf.PdfReader(f)
            reader = pymupdf.open(f)
            for pages in reader:
                text.append(pages.get_text())
        return "".join(text)
    
    elif file_ext in ['.docx', '.doc']:
        return docx2txt.process(filePath)
    
    else: 
        raise ValueError(f"Unsupported file type: {file_ext}")
