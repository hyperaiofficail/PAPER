import unittest
from unittest.mock import AsyncMock, MagicMock
import sys

# Reuse the mock environment already set up in test_middleware
import test_middleware

# Import the logic to test
from main import process_tool, TOOLS

class TestFileUpload(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        # We need a dummy tool to exist so find_tool doesn't return None
        cls.dummy_tool = {"tool_name": "TestTool", "output_type": "text"}
        if cls.dummy_tool not in TOOLS:
            TOOLS.append(cls.dummy_tool)

    @classmethod
    def tearDownClass(cls):
        if cls.dummy_tool in TOOLS:
            TOOLS.remove(cls.dummy_tool)

    async def test_process_tool_no_filename(self):
        # UploadFile mock where filename is None
        mock_file = MagicMock()
        mock_file.filename = None

        result = await process_tool("TestTool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_empty_filename(self):
        # UploadFile mock where filename is empty
        mock_file = MagicMock()
        mock_file.filename = "   "

        result = await process_tool("TestTool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_dot_filename(self):
        # UploadFile mock where filename results in '.'
        mock_file = MagicMock()
        mock_file.filename = "."

        result = await process_tool("TestTool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_dotdot_filename(self):
        # UploadFile mock where filename results in '..'
        mock_file = MagicMock()
        mock_file.filename = ".."

        result = await process_tool("TestTool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_path_traversal_filename(self):
        # UploadFile mock where filename attempts path traversal
        mock_file = MagicMock()
        mock_file.filename = "../../etc/passwd"

        result = await process_tool("TestTool", file=mock_file)
        self.assertEqual(result["filename"], "passwd")
        self.assertEqual(result["download_url"], "/download/processed_passwd")

    async def test_process_tool_valid_filename(self):
        # UploadFile mock with a valid filename
        mock_file = MagicMock()
        mock_file.filename = "valid.txt"

        result = await process_tool("TestTool", file=mock_file)
        self.assertEqual(result["filename"], "valid.txt")
        self.assertEqual(result["download_url"], "/download/processed_valid.txt")


if __name__ == "__main__":
    unittest.main()
