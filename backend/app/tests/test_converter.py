import os
from app.pipeline.ingestion.converter import converter
from reportlab.pdfgen import canvas
import pytest

@pytest.mark.asyncio
async def test_conversion_success(tmp_path):
    file_path = tmp_path / "test.pdf"
    c = canvas.Canvas(str(file_path))
    c.drawString(100, 750, "Hello PDF World")
    c.save()
     # 2. Get the full path as a string
    file_name = str(file_path)

    # 3. Run your converter
    result = await converter(file_name)

    # 4. Assertions
    assert result is not None
    assert isinstance(result, str)