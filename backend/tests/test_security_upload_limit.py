import pytest
from fastapi.testclient import TestClient
import os
import sys

# Ensure backend is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app, MAX_UPLOAD_SIZE

client = TestClient(app)

def test_large_file_upload():
    # Create content slightly larger than limit
    large_content = b"a" * (MAX_UPLOAD_SIZE + 1)

    # "PDF Merge" is a valid tool name
    response = client.post(
        "/process/PDF%20Merge",
        files={"file": ("large_file.pdf", large_content, "application/pdf")}
    )

    # Expectation: middleware should reject with 413
    assert response.status_code == 413
    assert "too large" in response.text.lower()

def test_small_file_upload():
    # Verify small files still work
    small_content = b"test content"
    response = client.post(
        "/process/PDF%20Merge",
        files={"file": ("small.pdf", small_content, "application/pdf")}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
