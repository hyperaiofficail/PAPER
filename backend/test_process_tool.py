import unittest
from unittest.mock import MagicMock
import sys
import asyncio

# Reuse the mock objects from test_middleware so sys.modules is consistent
from test_middleware import mock_fastapi, mock_responses, MockJSONResponse

# Since main is already imported and decorated we can import process_tool and TOOLS directly
from main import process_tool, TOOLS

class TestProcessToolFileUpload(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Ensure a dummy tool exists so find_tool won't return None
        self.dummy_tool = {
            "tool_name": "DummyTool",
            "category": "Test",
            "output_type": "Unknown"
        }
        if not any(t["tool_name"] == "DummyTool" for t in TOOLS):
            TOOLS.append(self.dummy_tool)

    async def test_process_tool_no_filename(self):
        # file.filename is None
        mock_file = MagicMock()
        mock_file.filename = None

        result = await process_tool(tool_name="DummyTool", file=mock_file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_empty_filename(self):
        # file.filename is empty or just spaces
        mock_file = MagicMock()
        mock_file.filename = "   "

        result = await process_tool(tool_name="DummyTool", file=mock_file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_dot_filename(self):
        # file.filename results in "." after basename extraction
        mock_file = MagicMock()
        mock_file.filename = "foo/."

        result = await process_tool(tool_name="DummyTool", file=mock_file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_dotdot_filename(self):
        # file.filename results in ".." after basename extraction
        mock_file = MagicMock()
        mock_file.filename = "foo/.."

        result = await process_tool(tool_name="DummyTool", file=mock_file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_valid_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "valid.txt"

        result = await process_tool(tool_name="DummyTool", file=mock_file, text_input=None)

        self.assertEqual(result["filename"], "valid.txt")
        self.assertEqual(result["download_url"], "/download/processed_valid.txt")

    async def test_process_tool_windows_path_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "C:\\path\\to\\file.txt"

        result = await process_tool(tool_name="DummyTool", file=mock_file, text_input=None)

        self.assertEqual(result["filename"], "file.txt")
        self.assertEqual(result["download_url"], "/download/processed_file.txt")

if __name__ == "__main__":
    unittest.main()
