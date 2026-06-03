import unittest
from unittest.mock import AsyncMock, MagicMock
import sys

# We reuse the mocks from test_middleware so we don't contaminate sys.modules differently
from test_middleware import mock_fastapi, mock_responses, MockFastAPI, MockJSONResponse

# Now import the process_tool function and TOOLS list
from main import process_tool, TOOLS

class TestFileUpload(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Ensure a dummy tool exists so we can test the endpoint logic
        self.dummy_tool = {
            "tool_name": "DummyTool",
            "category": "Test",
            "output_type": "text"
        }
        if self.dummy_tool not in TOOLS:
            TOOLS.append(self.dummy_tool)

    def tearDown(self):
        # Remove dummy tool to keep state clean
        if self.dummy_tool in TOOLS:
            TOOLS.remove(self.dummy_tool)

    async def test_file_upload_none_filename(self):
        # Simulate an upload without a filename (which causes AttributeError if not handled)
        file_mock = MagicMock()
        file_mock.filename = None

        result = await process_tool("DummyTool", file=file_mock, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_file_upload_empty_filename(self):
        file_mock = MagicMock()
        file_mock.filename = ""

        result = await process_tool("DummyTool", file=file_mock, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_whitespace_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "   "

        result = await process_tool("DummyTool", file=file_mock, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_dot_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "."

        result = await process_tool("DummyTool", file=file_mock, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_dot_dot_filename(self):
        file_mock = MagicMock()
        file_mock.filename = ".."

        result = await process_tool("DummyTool", file=file_mock, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_normal_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "test_file.txt"

        result = await process_tool("DummyTool", file=file_mock, text_input=None)
        self.assertEqual(result["filename"], "test_file.txt")

    async def test_file_upload_traversal_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "../../../etc/passwd"

        result = await process_tool("DummyTool", file=file_mock, text_input=None)
        self.assertEqual(result["filename"], "passwd")

if __name__ == "__main__":
    unittest.main()
