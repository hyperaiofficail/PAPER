from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_upload_file_too_large():
    # 10MB + 1 byte
    large_size = 10 * 1024 * 1024 + 1

    # We don't actually need to send that much data if we fake the header,
    # but some servers/frameworks might wait for the body.
    # However, a middleware checking Content-Length should reject it immediately.
    headers = {"Content-Length": str(large_size)}

    # We use a tool name that exists, e.g., "PDF Merge"
    response = client.post(
        "/process/PDF%20Merge",
        headers=headers,
        # We provide a small body, but the header claims it's huge.
        # If the server respects Content-Length check, it should 413.
        # If it tries to read the body, it might fail differently or succeed if we didn't send enough data.
        # But for this specific test of the security control (Content-Length check), this is sufficient.
        content=b"small content"
    )

    assert response.status_code == 413
    assert response.json() == {"detail": "File too large"}
