import unittest
from unittest.mock import AsyncMock, MagicMock
import sys

# Import test_middleware to reuse the FastAPI mock setup
import test_middleware

from main import process_tool, TOOLS

class TestProcessTool(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Add a dummy tool so that process_tool can find it
        self.dummy_tool = {
            "tool_name": "DummyTool",
            "category": "Dummy",
            "description": "Dummy description",
            "output_type": "DummyOutput"
        }
        TOOLS.append(self.dummy_tool)

    def tearDown(self):
        TOOLS.remove(self.dummy_tool)

    async def test_process_tool_with_valid_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "valid_file.txt"

        result = await process_tool("DummyTool", file=mock_file)
        self.assertEqual(result["filename"], "valid_file.txt")
        self.assertEqual(result["download_url"], "/download/processed_valid_file.txt")

    async def test_process_tool_with_none_filename(self):
        # Tests DoS vulnerability when filename is None
        mock_file = MagicMock()
        mock_file.filename = None

        result = await process_tool("DummyTool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_with_empty_filename(self):
        mock_file = MagicMock()
        mock_file.filename = ""

        result = await process_tool("DummyTool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_with_whitespace_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "   "

        result = await process_tool("DummyTool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_with_dot_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "."

        result = await process_tool("DummyTool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_with_dotdot_filename(self):
        mock_file = MagicMock()
        mock_file.filename = ".."

        result = await process_tool("DummyTool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_with_path_traversal(self):
        mock_file = MagicMock()
        mock_file.filename = "../../etc/passwd"

        result = await process_tool("DummyTool", file=mock_file)
        self.assertEqual(result["filename"], "passwd")
        self.assertEqual(result["download_url"], "/download/processed_passwd")

    async def test_process_tool_with_backslash_traversal(self):
        mock_file = MagicMock()
        mock_file.filename = "..\\..\\Windows\\System32\\cmd.exe"

        result = await process_tool("DummyTool", file=mock_file)
        self.assertEqual(result["filename"], "cmd.exe")
        self.assertEqual(result["download_url"], "/download/processed_cmd.exe")


if __name__ == "__main__":
    unittest.main()
