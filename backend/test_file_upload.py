import unittest
from unittest.mock import MagicMock
import sys

# Reuse the existing mocks from test_middleware to avoid clobbering sys.modules
import test_middleware
from test_middleware import mock_fastapi

# Ensure HTTPException is properly mocked as an Exception
class MockHTTPException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
mock_fastapi.HTTPException = MockHTTPException

from main import process_tool, TOOLS # noqa: E402

class TestFileUpload(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Ensure a tool exists so process_tool doesn't 404 immediately
        if not any(t.get("tool_name") == "TestTool" for t in TOOLS):
            TOOLS.append({"tool_name": "TestTool", "category": "Test"})

    async def test_none_filename(self):
        file_mock = MagicMock()
        file_mock.filename = None

        result = await process_tool("TestTool", file=file_mock, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_dot_dot_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "../../../etc/passwd"

        result = await process_tool("TestTool", file=file_mock, text_input=None)
        self.assertEqual(result["filename"], "passwd")

    async def test_dot_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "."

        result = await process_tool("TestTool", file=file_mock, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_empty_filename(self):
        file_mock = MagicMock()
        file_mock.filename = ""

        result = await process_tool("TestTool", file=file_mock, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_whitespace_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "   "

        result = await process_tool("TestTool", file=file_mock, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_backslash_traversal(self):
        file_mock = MagicMock()
        file_mock.filename = "..\\..\\windows\\system32\\cmd.exe"

        result = await process_tool("TestTool", file=file_mock, text_input=None)
        self.assertEqual(result["filename"], "cmd.exe")

if __name__ == "__main__":
    unittest.main()
