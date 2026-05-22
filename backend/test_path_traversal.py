import sys
import unittest
from unittest.mock import MagicMock


# Set up the sys.modules mocks as in test_middleware.py
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


class MockException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail


mock_fastapi = MagicMock()
mock_fastapi.FastAPI = MockFastAPI
mock_fastapi.HTTPException = MockException
mock_fastapi.File = lambda x: x
mock_fastapi.Form = lambda x: x
mock_fastapi.UploadFile = MagicMock
mock_responses = MagicMock()

sys.modules["fastapi"] = mock_fastapi
sys.modules["fastapi.middleware"] = MagicMock()
sys.modules["fastapi.middleware.cors"] = MagicMock()
sys.modules["fastapi.responses"] = mock_responses

from main import process_tool  # noqa: E402


class TestPathTraversal(unittest.IsolatedAsyncioTestCase):
    async def test_empty_filename(self):
        # Create a mock file with an empty filename
        mock_file = MagicMock()
        mock_file.filename = ""

        result = await process_tool("Format-JSON", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_none_filename(self):
        # Create a mock file with None filename
        mock_file = MagicMock()
        mock_file.filename = None

        result = await process_tool("Format-JSON", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_dot_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "."

        result = await process_tool("Format-JSON", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_dotdot_filename(self):
        mock_file = MagicMock()
        mock_file.filename = ".."

        result = await process_tool("Format-JSON", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_whitespace_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "   "

        result = await process_tool("Format-JSON", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_valid_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "test_file.txt"

        result = await process_tool("Format-JSON", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "test_file.txt")
        self.assertEqual(result["download_url"], "/download/processed_test_file.txt")


if __name__ == "__main__":
    unittest.main()
