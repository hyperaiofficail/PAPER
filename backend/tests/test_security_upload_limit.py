import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_upload_within_limit():
    # Simulate a file upload within the 10MB limit
    # We don't actually need 10MB of data to test the middleware if it relies on Content-Length,
    # but TestClient might recalculate it. Let's send a small payload and ensure it passes.
    # To properly test the limit, we will mock a large Content-Length header.

    # Test valid request passes the middleware
    response = client.post(
        "/process/PDF to Text", # Use a valid tool name
        headers={"Content-Length": "1000"},
        data={"text_input": "Small payload"}
    )
    # The endpoint might return 200 or 400 (if no file is provided but expected),
    # but it shouldn't return 413.
    assert response.status_code != 413

def test_upload_exceeds_limit():
    # Simulate a request exceeding the 10MB limit
    MAX_SIZE = 10 * 1024 * 1024

    # Send a request with Content-Length larger than MAX_UPLOAD_SIZE
    response = client.post(
        "/process/PDF to Text",
        headers={"Content-Length": str(MAX_SIZE + 1)},
        data={"text_input": "Test data"}
    )

    # The middleware should catch this and return a 413 Payload Too Large
    assert response.status_code == 413
    assert "Payload Too Large" in response.json()["detail"]
