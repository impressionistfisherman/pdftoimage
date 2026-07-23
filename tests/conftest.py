from pathlib import Path

import fitz
import pytest


@pytest.fixture()
def sample_pdf(tmp_path: Path) -> Path:
    """A 3-page PDF built with PyMuPDF, for use in tests."""
    path = tmp_path / "sample.pdf"
    doc = fitz.open()
    for i in range(3):
        page = doc.new_page()
        page.insert_text((72, 72), f"Page {i + 1}")
    doc.save(path)
    doc.close()
    return path
