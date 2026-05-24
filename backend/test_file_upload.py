import unittest
import sys
from unittest.mock import MagicMock
import json


class MockJSONResponse:
    def __init__(self, status_code, content):
        self.status_code = status_code
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


mock_fastapi = MagicMock()
mock_fastapi.FastAPI = MockFastAPI
mock_fastapi.File = MagicMock()
mock_fastapi.Form = MagicMock()
mock_fastapi.UploadFile = MagicMock()
mock_fastapi.Request = MagicMock()


class MockHTTPException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail


mock_fastapi.HTTPException = MockHTTPException

mock_responses = MagicMock()
mock_responses.JSONResponse = MockJSONResponse

sys.modules["fastapi"] = mock_fastapi
sys.modules["fastapi.middleware"] = MagicMock()
sys.modules["fastapi.middleware.cors"] = MagicMock()
sys.modules["fastapi.responses"] = mock_responses


# Now import main
from main import process_tool, TOOLS  # noqa: E402

# Add a dummy tool to TOOLS so find_tool succeeds
TOOLS.append(
    {
        "tool_name": "test_tool",
        "category": "Test",
        "description": "Test tool",
        "use_case": "Testing",
        "capabilities": [],
        "limitations": [],
        "input_type": "file",
        "output_type": "text",
    }
)


class TestFileUploadSanitization(unittest.IsolatedAsyncioTestCase):
    async def test_normal_filename(self):
        file = MagicMock()
        file.filename = "image.png"

        result = await process_tool(tool_name="test_tool", file=file, text_input=None)
        self.assertEqual(result["filename"], "image.png")
        self.assertEqual(result["download_url"], "/download/processed_image.png")

    async def test_none_filename(self):
        file = MagicMock()
        file.filename = None

        result = await process_tool(tool_name="test_tool", file=file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_empty_filename(self):
        file = MagicMock()
        file.filename = ""

        result = await process_tool(tool_name="test_tool", file=file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_path_traversal_filename(self):
        file = MagicMock()
        file.filename = "../../../etc/passwd"

        result = await process_tool(tool_name="test_tool", file=file, text_input=None)
        self.assertEqual(result["filename"], "passwd")

    async def test_path_traversal_backslash(self):
        file = MagicMock()
        file.filename = "..\\..\\..\\windows\\system32\\cmd.exe"

        result = await process_tool(tool_name="test_tool", file=file, text_input=None)
        self.assertEqual(result["filename"], "cmd.exe")

    async def test_dot_filename(self):
        file = MagicMock()
        file.filename = "."

        result = await process_tool(tool_name="test_tool", file=file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_dot_dot_filename(self):
        file = MagicMock()
        file.filename = ".."

        result = await process_tool(tool_name="test_tool", file=file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_whitespace_filename(self):
        file = MagicMock()
        file.filename = "   "

        result = await process_tool(tool_name="test_tool", file=file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")


if __name__ == "__main__":
    unittest.main()
