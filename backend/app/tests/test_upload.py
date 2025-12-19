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

def test_upload_file_success():
    """Test uploading a file successfully"""
    
    # Create a fake file in memory
    file_content = b"This is test file content"
    file_name = "cover.pdf"
    
    # Upload the file
    response = client.post(
        "/upload",
        files={"file": (file_name, file_content, "text/plain")}
    )
    
    # Check response
    assert "writing" in response.text.lower()
    assert response.status_code == 200
    
    # Check file was actually saved
    uploaded_file_path = os.path.join("uploads", file_name)
    assert os.path.exists(uploaded_file_path)
    
    # Verify content is correct
    with open(uploaded_file_path, "rb") as f:
        saved_content = f.read()
    assert saved_content == file_content
    
    # Cleanup
    os.remove(uploaded_file_path)
