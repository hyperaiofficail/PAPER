import unittest
from unittest.mock import MagicMock
import sys

from test_middleware import mock_fastapi, mock_responses
sys.modules["fastapi"] = mock_fastapi
sys.modules["fastapi.responses"] = mock_responses

from main import process_tool, TOOLS

class TestFileUpload(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Ensure we have a dummy tool to find
        self.dummy_tool = {"tool_name": "TestTool", "category": "Test", "output_type": "text"}
        if not any(t["tool_name"] == "TestTool" for t in TOOLS):
            TOOLS.append(self.dummy_tool)

    async def test_file_upload_none_filename(self):
        file_mock = MagicMock()
        file_mock.filename = None
        result = await process_tool("TestTool", file=file_mock)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_empty_filename(self):
        file_mock = MagicMock()
        file_mock.filename = ""
        result = await process_tool("TestTool", file=file_mock)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_dot_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "."
        result = await process_tool("TestTool", file=file_mock)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_valid_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "valid_file.txt"
        result = await process_tool("TestTool", file=file_mock)
        self.assertEqual(result["filename"], "valid_file.txt")

    async def test_file_upload_path_traversal(self):
        file_mock = MagicMock()
        file_mock.filename = "../../etc/passwd"
        result = await process_tool("TestTool", file=file_mock)
        self.assertEqual(result["filename"], "passwd")

if __name__ == "__main__":
    unittest.main()
