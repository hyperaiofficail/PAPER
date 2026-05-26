import unittest
from unittest.mock import AsyncMock, MagicMock
import sys

class MockJSONResponse:
    def __init__(self, status_code, content):
        self.status_code = status_code
        import json
        self.body = json.dumps(content).encode()

def identity_decorator_factory(*args, **kwargs):
    def decorator(func):
        return func
    return decorator

class MockFastAPI:
    def __init__(self, *args, **kwargs):
        pass

    def middleware(self, *args, **kwargs):
        return identity_decorator_factory(*args, **kwargs)

    def get(self, *args, **kwargs):
        return identity_decorator_factory(*args, **kwargs)

    def post(self, *args, **kwargs):
        return identity_decorator_factory(*args, **kwargs)

    def add_middleware(self, *args, **kwargs):
        pass

# Mock fastapi dependencies
mock_fastapi = MagicMock()
mock_fastapi.FastAPI = MockFastAPI
mock_fastapi.HTTPException = Exception
mock_fastapi.File = MagicMock()
mock_fastapi.Form = MagicMock()

class MockUploadFile:
    def __init__(self, filename):
        self.filename = filename

mock_fastapi.UploadFile = MockUploadFile

mock_responses = MagicMock()
mock_responses.JSONResponse = MockJSONResponse
sys.modules["fastapi"] = mock_fastapi
sys.modules["fastapi.middleware"] = MagicMock()
sys.modules["fastapi.middleware.cors"] = MagicMock()
sys.modules["fastapi.responses"] = mock_responses

from main import process_tool, TOOLS  # noqa: E402

class TestFileUploadSanitization(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Add a dummy tool so we don't get 404
        if not any(t["tool_name"] == "dummy_tool" for t in TOOLS):
            TOOLS.append({"tool_name": "dummy_tool", "output_type": "text"})

    async def test_valid_filename(self):
        file = MockUploadFile("valid.txt")
        res = await process_tool("dummy_tool", file=file, text_input=None)
        self.assertEqual(res["filename"], "valid.txt")
        self.assertEqual(res["download_url"], "/download/processed_valid.txt")

    async def test_filename_with_path_traversal(self):
        file = MockUploadFile("../../etc/passwd")
        res = await process_tool("dummy_tool", file=file, text_input=None)
        self.assertEqual(res["filename"], "passwd")
        self.assertEqual(res["download_url"], "/download/processed_passwd")

    async def test_filename_with_windows_path_traversal(self):
        file = MockUploadFile("..\\..\\windows\\system32\\cmd.exe")
        res = await process_tool("dummy_tool", file=file, text_input=None)
        self.assertEqual(res["filename"], "cmd.exe")
        self.assertEqual(res["download_url"], "/download/processed_cmd.exe")

    async def test_none_filename(self):
        file = MockUploadFile(None)
        res = await process_tool("dummy_tool", file=file, text_input=None)
        self.assertEqual(res["filename"], "unnamed")
        self.assertEqual(res["download_url"], "/download/processed_unnamed")

    async def test_empty_filename(self):
        file = MockUploadFile("")
        res = await process_tool("dummy_tool", file=file, text_input=None)
        self.assertEqual(res["filename"], "unnamed")
        self.assertEqual(res["download_url"], "/download/processed_unnamed")

    async def test_whitespace_filename(self):
        file = MockUploadFile("   ")
        res = await process_tool("dummy_tool", file=file, text_input=None)
        self.assertEqual(res["filename"], "unnamed")
        self.assertEqual(res["download_url"], "/download/processed_unnamed")

    async def test_dot_filename(self):
        file = MockUploadFile(".")
        res = await process_tool("dummy_tool", file=file, text_input=None)
        self.assertEqual(res["filename"], "unnamed")
        self.assertEqual(res["download_url"], "/download/processed_unnamed")

    async def test_dotdot_filename(self):
        file = MockUploadFile("..")
        res = await process_tool("dummy_tool", file=file, text_input=None)
        self.assertEqual(res["filename"], "unnamed")
        self.assertEqual(res["download_url"], "/download/processed_unnamed")

if __name__ == "__main__":
    unittest.main()
