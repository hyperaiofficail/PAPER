import unittest
from unittest.mock import MagicMock
import sys
import os

from test_middleware import mock_fastapi

# Create a mock for HTTPException that inherits from Exception
class MockHTTPException(Exception):
    def __init__(self, status_code, detail=None):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"{status_code}: {detail}")

mock_fastapi.HTTPException = MockHTTPException

# We also need to mock File, UploadFile, Form, Request
mock_fastapi.File = MagicMock()
mock_fastapi.UploadFile = MagicMock
mock_fastapi.Form = MagicMock()
mock_fastapi.Request = MagicMock

# Now import main and the process_tool function (sys.modules is already populated by test_middleware)
import main
from main import process_tool

class TestProcessToolSecurity(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # We need to make sure tools exist so find_tool doesn't raise 404
        self.dummy_tool = {"tool_name": "DummyTool", "category": "Test", "output_type": "text"}
        if "DummyTool" not in [t.get("tool_name") for t in main.TOOLS]:
            main.TOOLS.append(self.dummy_tool)

    async def test_process_tool_filename_none(self):
        # Test file.filename being None
        mock_file = MagicMock()
        mock_file.filename = None

        result = await process_tool(tool_name="DummyTool", file=mock_file, text_input=None)

        self.assertEqual(result["input_type"], "file")
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_filename_empty_after_strip(self):
        # Test file.filename being spaces
        mock_file = MagicMock()
        mock_file.filename = "   "

        result = await process_tool(tool_name="DummyTool", file=mock_file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_filename_dot(self):
        # Test file.filename being "."
        mock_file = MagicMock()
        mock_file.filename = "."

        result = await process_tool(tool_name="DummyTool", file=mock_file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_filename_dotdot(self):
        # Test file.filename being ".."
        mock_file = MagicMock()
        mock_file.filename = ".."

        result = await process_tool(tool_name="DummyTool", file=mock_file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_filename_normal(self):
        # Test a normal filename
        mock_file = MagicMock()
        mock_file.filename = "test_image.png"

        result = await process_tool(tool_name="DummyTool", file=mock_file, text_input=None)

        self.assertEqual(result["filename"], "test_image.png")

    async def test_process_tool_filename_traversal(self):
        # Test path traversal payloads
        mock_file = MagicMock()
        mock_file.filename = "../../etc/passwd"

        result = await process_tool(tool_name="DummyTool", file=mock_file, text_input=None)

        self.assertEqual(result["filename"], "passwd")

if __name__ == "__main__":
    unittest.main()
