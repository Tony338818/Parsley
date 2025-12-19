from fastapi.testclient import TestClient
from app.main import app
import os 
from app.pipeline.ingestion import converter


client = TestClient(app)

def testHomePage():
    """Test that the homepage loads successfully"""
    response = client.get("/")
    
    assert response.status_code == 200
    # assert "text/html" in response.headers["content-type"]
    assert "upload" in response.text.lower()

def test_file_size_limit_rejected():
    """Test that files larger than limit are rejected"""
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    # Create an in-memory file slightly larger than limit
    large_content = b"A" * (MAX_FILE_SIZE + 1)  # 10MB + 1 byte
    file_name = "large_cover.txt"

    response = client.post(
        "/upload",
        files={"file": (file_name, large_content, "text/plain")}
    )

    assert response.status_code == 413  # Payload Too Large
    assert "too large" in response.text.lower() or "exceeds" in response.text.lower()



def test_upload_file_success():
    """Test uploading a supported file successfully"""
    
    file_content = b"%PDF-1.4 dummy pdf content"  # Minimal valid PDF header
    file_name = "cover.pdf"  # Must be .pdf or .docx based on your validation
    
    response = client.post(
        "/upload",
        files={"file": (file_name, file_content, "application/pdf")}
    )
    
    assert response.status_code == 200
    # assert "success" in response.text.lower() or "uploaded" in response.text.lower()

    # Check file was saved
    uploaded_file_path = os.path.join("uploads", file_name)
    assert os.path.exists(uploaded_file_path)

    # Verify content
    with open(uploaded_file_path, "rb") as f:
        saved_content = f.read()
    assert saved_content == file_content

    # Cleanup
    if os.path.exists(uploaded_file_path):
        os.remove(uploaded_file_path)