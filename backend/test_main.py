from fastapi.testclient import TestClient
from backend.main import app
import os

client = TestClient(app)

def test_chunked_upload_rejected():
    response = client.post("/process/Tool1", headers={"transfer-encoding": "chunked"})
    assert response.status_code == 400
    assert "Chunked transfer encoding is not allowed" in response.json()["detail"]

def test_large_upload_rejected():
    # 11MB
    response = client.post("/process/Tool1", headers={"content-length": str(11 * 1024 * 1024)})
    assert response.status_code == 413
    assert "File too large" in response.json()["detail"]

def test_invalid_content_length_rejected():
    response = client.post("/process/Tool1", headers={"content-length": "invalid"})
    assert response.status_code == 400
    assert "Invalid Content-Length" in response.json()["detail"]

def test_valid_upload_size_accepted():
    response = client.post("/process/Tool1", headers={"content-length": "1024"})
    # It should pass the middleware and hit the endpoint logic (which might return 404/422 but not 400/413 from middleware)
    assert response.status_code not in [400, 413]
