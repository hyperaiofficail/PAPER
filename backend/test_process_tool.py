import unittest
from unittest.mock import MagicMock
import sys

# Ensure sys.modules is patched before importing main
import test_middleware

from main import process_tool, TOOLS

class TestProcessTool(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Add a dummy tool to prevent 404
        self.dummy_tool = {"tool_name": "TestTool", "category": "Test"}
        TOOLS.append(self.dummy_tool)

    def tearDown(self):
        TOOLS.remove(self.dummy_tool)

    async def test_process_tool_none_filename(self):
        file_mock = MagicMock()
        file_mock.filename = None

        result = await process_tool(tool_name="TestTool", file=file_mock, text_input=None)

        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_empty_filename(self):
        file_mock = MagicMock()
        file_mock.filename = ""

        result = await process_tool(tool_name="TestTool", file=file_mock, text_input=None)

        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_whitespace_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "   "

        result = await process_tool(tool_name="TestTool", file=file_mock, text_input=None)

        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_dot_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "."

        result = await process_tool(tool_name="TestTool", file=file_mock, text_input=None)

        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_dotdot_filename(self):
        file_mock = MagicMock()
        file_mock.filename = ".."

        result = await process_tool(tool_name="TestTool", file=file_mock, text_input=None)

        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_path_traversal(self):
        file_mock = MagicMock()
        file_mock.filename = "../../../etc/passwd"

        result = await process_tool(tool_name="TestTool", file=file_mock, text_input=None)

        self.assertEqual(result["filename"], "passwd")

    async def test_process_tool_windows_path_traversal(self):
        file_mock = MagicMock()
        file_mock.filename = "..\\..\\windows\\system32\\cmd.exe"

        result = await process_tool(tool_name="TestTool", file=file_mock, text_input=None)

        self.assertEqual(result["filename"], "cmd.exe")

if __name__ == "__main__":
    unittest.main()
