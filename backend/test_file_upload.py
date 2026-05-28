import unittest
from unittest.mock import MagicMock
import sys

# Reuse mocks from test_middleware to avoid cross-contamination in sys.modules
import test_middleware
from test_middleware import MockJSONResponse, identity_decorator_factory

# Import main after mocks are set up
import main
from main import process_tool

class TestProcessTool(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Add a dummy tool to TOOLS for testing
        self.dummy_tool = {
            "tool_name": "TestTool",
            "category": "Test",
            "description": "A test tool",
            "output_type": "text"
        }
        main.TOOLS.append(self.dummy_tool)

    def tearDown(self):
        # Remove the dummy tool
        if self.dummy_tool in main.TOOLS:
            main.TOOLS.remove(self.dummy_tool)

    async def test_normal_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "test.txt"

        result = await process_tool("TestTool", file=mock_file)
        self.assertEqual(result["filename"], "test.txt")
        self.assertEqual(result["download_url"], "/download/processed_test.txt")

    async def test_path_traversal_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "../../../etc/passwd"

        result = await process_tool("TestTool", file=mock_file)
        self.assertEqual(result["filename"], "passwd")
        self.assertEqual(result["download_url"], "/download/processed_passwd")

    async def test_path_traversal_windows_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "..\\..\\..\\windows\\system32\\cmd.exe"

        result = await process_tool("TestTool", file=mock_file)
        self.assertEqual(result["filename"], "cmd.exe")
        self.assertEqual(result["download_url"], "/download/processed_cmd.exe")

    async def test_none_filename(self):
        mock_file = MagicMock()
        mock_file.filename = None

        result = await process_tool("TestTool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_empty_filename(self):
        mock_file = MagicMock()
        mock_file.filename = ""

        result = await process_tool("TestTool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_whitespace_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "   "

        result = await process_tool("TestTool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_dot_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "."

        result = await process_tool("TestTool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_dotdot_filename(self):
        mock_file = MagicMock()
        mock_file.filename = ".."

        result = await process_tool("TestTool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

if __name__ == "__main__":
    unittest.main()
