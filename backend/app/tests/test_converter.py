import os
from app.pipeline.ingestion.converter import converter


BASE_DIR = ''
def test_conversion_success():
    file_name = 'cover.pdf'
    file_path = os.path.join(BASE_DIR, file_name)

    # Check file was actually saved
    uploaded_file_path = os.path.join("uploads", file_name)
    assert os.path.exists(uploaded_file_path)

    result = converter(file_path)
    assert result is not None
    assert isinstance(result, str) 