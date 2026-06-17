import unittest
from unittest.mock import MagicMock, AsyncMock
import sys
import os

# Reuse mocks from test_middleware to avoid sys.modules conflict
from test_middleware import mock_fastapi, MockJSONResponse

# Ensure fastapi modules are properly mocked in sys.modules
sys.modules["fastapi"] = mock_fastapi
sys.modules["fastapi.middleware"] = MagicMock()
sys.modules["fastapi.middleware.cors"] = MagicMock()
sys.modules["fastapi.responses"] = MagicMock(JSONResponse=MockJSONResponse)

# Import the necessary components from main
from main import process_tool, TOOLS, HTTPException

class TestFileUploadSanitization(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Add a dummy tool to TOOLS list to pass the find_tool check
        self.dummy_tool = {
            "tool_name": "TestTool",
            "category": "TestCategory",
            "output_type": "TestOutput"
        }
        TOOLS.append(self.dummy_tool)

    def tearDown(self):
        # Clean up the dummy tool
        TOOLS.remove(self.dummy_tool)

    async def test_filename_none(self):
        # Test case where file.filename is None
        mock_file = MagicMock()
        mock_file.filename = None

        result = await process_tool(tool_name="TestTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_filename_empty_string(self):
        # Test case where file.filename is an empty string
        mock_file = MagicMock()
        mock_file.filename = ""

        result = await process_tool(tool_name="TestTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_filename_whitespace(self):
        # Test case where file.filename contains only whitespace
        mock_file = MagicMock()
        mock_file.filename = "   \t\n  "

        result = await process_tool(tool_name="TestTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_filename_dot(self):
        # Test case where file.filename evaluates to '.'
        mock_file = MagicMock()
        mock_file.filename = "."

        result = await process_tool(tool_name="TestTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_filename_dot_dot(self):
        # Test case where file.filename evaluates to '..'
        mock_file = MagicMock()
        mock_file.filename = ".."

        result = await process_tool(tool_name="TestTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_filename_path_traversal(self):
        # Test case with path traversal attempt
        mock_file = MagicMock()
        mock_file.filename = "../../../etc/passwd"

        result = await process_tool(tool_name="TestTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "passwd")

    async def test_filename_valid(self):
        # Test case with a valid filename
        mock_file = MagicMock()
        mock_file.filename = "valid_file.txt"

        result = await process_tool(tool_name="TestTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "valid_file.txt")

    async def test_filename_windows_path(self):
        # Test case with Windows path separators
        mock_file = MagicMock()
        mock_file.filename = "C:\\Windows\\System32\\cmd.exe"

        result = await process_tool(tool_name="TestTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "cmd.exe")

if __name__ == "__main__":
    unittest.main()
