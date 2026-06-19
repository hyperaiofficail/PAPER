import unittest
from unittest.mock import MagicMock
import sys

# Use existing mock definitions from test_middleware to avoid reinventing the wheel
from test_middleware import MockFastAPI, MockJSONResponse, identity_decorator_factory, mock_fastapi, mock_responses

# Setup the system modules like in test_middleware.py
sys.modules["fastapi"] = mock_fastapi
sys.modules["fastapi.middleware"] = MagicMock()
sys.modules["fastapi.middleware.cors"] = MagicMock()
sys.modules["fastapi.responses"] = mock_responses

from main import process_tool, TOOLS

class TestProcessTool(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Ensure a dummy tool exists so process_tool doesn't return 404
        self.dummy_tool = {"tool_name": "TestTool", "category": "Test", "output_type": "TestType"}
        if not any(t["tool_name"] == "TestTool" for t in TOOLS):
            TOOLS.append(self.dummy_tool)

    def tearDown(self):
        if self.dummy_tool in TOOLS:
            TOOLS.remove(self.dummy_tool)

    async def test_process_tool_valid_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "valid_file.txt"

        result = await process_tool("TestTool", file=file_mock, text_input=None)

        self.assertEqual(result["filename"], "valid_file.txt")
        self.assertEqual(result["download_url"], "/download/processed_valid_file.txt")

    async def test_process_tool_none_filename(self):
        file_mock = MagicMock()
        file_mock.filename = None

        result = await process_tool("TestTool", file=file_mock, text_input=None)

        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_empty_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "   "

        result = await process_tool("TestTool", file=file_mock, text_input=None)

        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_path_traversal_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "../../../etc/passwd"

        result = await process_tool("TestTool", file=file_mock, text_input=None)

        self.assertEqual(result["filename"], "passwd")

    async def test_process_tool_dot_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "."

        result = await process_tool("TestTool", file=file_mock, text_input=None)

        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_dot_dot_filename(self):
        file_mock = MagicMock()
        file_mock.filename = ".."

        result = await process_tool("TestTool", file=file_mock, text_input=None)

        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_windows_path_traversal(self):
        file_mock = MagicMock()
        file_mock.filename = "..\\..\\windows\\system32\\cmd.exe"

        result = await process_tool("TestTool", file=file_mock, text_input=None)

        self.assertEqual(result["filename"], "cmd.exe")

if __name__ == "__main__":
    unittest.main()
