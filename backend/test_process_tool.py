import unittest
from unittest.mock import AsyncMock, MagicMock
import sys
import os

# Reuse mocks from test_middleware to avoid module conflicts
from test_middleware import mock_fastapi, MockJSONResponse

# Since we're directly testing the endpoint, we need `HTTPException` mock that acts like an Exception
class MockHTTPException(Exception):
    def __init__(self, status_code, detail=None):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

sys.modules["fastapi"].HTTPException = MockHTTPException

# Now import the function to test
from main import process_tool, TOOLS

class TestProcessTool(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Ensure there's a dummy tool to find
        if not any(t["tool_name"] == "DummyTool" for t in TOOLS):
            TOOLS.append({"tool_name": "DummyTool", "category": "Test", "output_type": "text"})

    async def test_process_tool_filename_none_dos(self):
        file_mock = MagicMock()
        file_mock.filename = None

        result = await process_tool("DummyTool", file=file_mock, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_filename_empty(self):
        file_mock = MagicMock()
        file_mock.filename = "   "

        result = await process_tool("DummyTool", file=file_mock, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_filename_dot(self):
        file_mock = MagicMock()
        file_mock.filename = "."

        result = await process_tool("DummyTool", file=file_mock, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_filename_dot_dot(self):
        file_mock = MagicMock()
        file_mock.filename = ".."

        result = await process_tool("DummyTool", file=file_mock, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_filename_traversal_backslash(self):
        file_mock = MagicMock()
        file_mock.filename = "..\\..\\etc\\passwd"

        result = await process_tool("DummyTool", file=file_mock, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "passwd")
        self.assertEqual(result["download_url"], "/download/processed_passwd")

    async def test_process_tool_filename_traversal_forwardslash(self):
        file_mock = MagicMock()
        file_mock.filename = "../../etc/passwd"

        result = await process_tool("DummyTool", file=file_mock, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "passwd")
        self.assertEqual(result["download_url"], "/download/processed_passwd")

if __name__ == "__main__":
    unittest.main()
