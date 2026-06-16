import unittest
from unittest.mock import MagicMock
import asyncio

# Reuse the existing mocks from test_middleware so sys.modules is consistently patched
from test_middleware import mock_fastapi, mock_responses, MockJSONResponse
import sys

# Now we can safely import from main
from main import process_tool, TOOLS

# Add a dummy tool to TOOLS so find_tool doesn't fail
TOOLS.append({
    "tool_name": "dummy_tool",
    "category": "Test",
    "description": "Dummy tool for testing",
    "use_case": "Testing",
    "capabilities": [],
    "limitations": [],
    "input_type": "Any",
    "output_type": "Any"
})


class TestFileUpload(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # We don't need a full TestClient, we can just test the function directly
        pass

    async def test_file_upload_none_filename(self):
        # file.filename is None
        mock_file = MagicMock()
        mock_file.filename = None

        result = await process_tool(tool_name="dummy_tool", file=mock_file, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_file_upload_empty_filename(self):
        # file.filename is empty
        mock_file = MagicMock()
        mock_file.filename = "   "

        result = await process_tool(tool_name="dummy_tool", file=mock_file, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_dot_filename(self):
        # file.filename is "."
        mock_file = MagicMock()
        mock_file.filename = "."

        result = await process_tool(tool_name="dummy_tool", file=mock_file, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_dot_dot_filename(self):
        # file.filename is ".."
        mock_file = MagicMock()
        mock_file.filename = ".."

        result = await process_tool(tool_name="dummy_tool", file=mock_file, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_normal_filename(self):
        # file.filename is "test.txt"
        mock_file = MagicMock()
        mock_file.filename = "test.txt"

        result = await process_tool(tool_name="dummy_tool", file=mock_file, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "test.txt")

    async def test_file_upload_path_traversal(self):
        # file.filename with path traversal characters
        mock_file = MagicMock()
        mock_file.filename = "../../test.txt"

        result = await process_tool(tool_name="dummy_tool", file=mock_file, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "test.txt")

    async def test_file_upload_backslash_path_traversal(self):
        # file.filename with backslash path traversal
        mock_file = MagicMock()
        mock_file.filename = "..\\..\\test.txt"

        result = await process_tool(tool_name="dummy_tool", file=mock_file, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "test.txt")


if __name__ == "__main__":
    unittest.main()
