import sys
import os
from fastapi.testclient import TestClient

# Add backend directory to path so we can import main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app

client = TestClient(app)

def test_large_file_upload():
    print("\n--- Testing Large File Upload (11MB) ---")
    large_content = b"a" * (11 * 1024 * 1024)
    tool_name = "PDF Merge"
    files = {"file": ("large.pdf", large_content, "application/pdf")}

    response = client.post(f"/process/{tool_name}", files=files)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 413:
        print("✅ SUCCESS: Large file rejected (413).")
    elif response.status_code == 200:
        print("❌ FAILURE: Large file accepted (200). expected 413.")
    else:
        print(f"❌ FAILURE: Unexpected status code {response.status_code}.")

def test_small_file_upload():
    print("\n--- Testing Small File Upload (1KB) ---")
    small_content = b"a" * 1024
    tool_name = "PDF Merge"
    files = {"file": ("small.pdf", small_content, "application/pdf")}

    response = client.post(f"/process/{tool_name}", files=files)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        print("✅ SUCCESS: Small file accepted (200).")
    else:
        print(f"❌ FAILURE: Small file rejected ({response.status_code}). expected 200.")

if __name__ == "__main__":
    test_large_file_upload()
    test_small_file_upload()
