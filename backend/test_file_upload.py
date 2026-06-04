import unittest
from unittest.mock import MagicMock
import os
import sys

# We need to import the mocked fastapi before main is imported
# The easiest way is to import from test_middleware, which sets up sys.modules
from test_middleware import mock_fastapi

# Now we can safely import from main
from main import process_tool, TOOLS

class TestFileUpload(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Ensure a test tool exists
        self.test_tool = {
            "tool_name": "TestTool",
            "category": "Test",
            "output_type": "string"
        }
        if self.test_tool not in TOOLS:
            TOOLS.append(self.test_tool)

    async def test_process_tool_filename_none(self):
        # Test case: file.filename is None
        mock_file = MagicMock()
        mock_file.filename = None

        result = await process_tool("TestTool", file=mock_file, text_input=None)

        self.assertEqual(result["input_type"], "file")
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_path_traversal(self):
        # Test case: file.filename attempts path traversal
        mock_file = MagicMock()
        mock_file.filename = "../../../etc/passwd"

        result = await process_tool("TestTool", file=mock_file, text_input=None)

        self.assertEqual(result["input_type"], "file")
        self.assertEqual(result["filename"], "passwd")
        self.assertEqual(result["download_url"], "/download/processed_passwd")

    async def test_process_tool_empty_filename(self):
        # Test case: file.filename resolves to empty after sanitization
        mock_file = MagicMock()
        mock_file.filename = "   "

        result = await process_tool("TestTool", file=mock_file, text_input=None)

        self.assertEqual(result["input_type"], "file")
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

if __name__ == "__main__":
    unittest.main()
