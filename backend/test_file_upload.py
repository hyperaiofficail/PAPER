import unittest
from unittest.mock import MagicMock
import sys
import os

# Reuse mocks from test_middleware setup
from test_middleware import mock_fastapi, MockJSONResponse, MockFastAPI # noqa: E402

# Need to mock Form, File, UploadFile
sys.modules["fastapi"].File = MagicMock()
sys.modules["fastapi"].Form = MagicMock()

class MockUploadFile:
    def __init__(self, filename):
        self.filename = filename

sys.modules["fastapi"].UploadFile = MockUploadFile

class MockHTTPException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail

sys.modules["fastapi"].HTTPException = MockHTTPException

# Import main after mocks
from main import process_tool, TOOLS # noqa: E402

class TestFileUpload(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Ensure a dummy tool exists for process_tool to find
        if not any(t["tool_name"] == "DummyTool" for t in TOOLS):
            TOOLS.append({
                "tool_name": "DummyTool",
                "category": "Test",
                "output_type": "TestOutput"
            })

    async def test_file_upload_none_filename(self):
        file = MockUploadFile(filename=None)
        result = await process_tool(tool_name="DummyTool", file=file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_empty_filename(self):
        file = MockUploadFile(filename="")
        result = await process_tool(tool_name="DummyTool", file=file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_whitespace_filename(self):
        file = MockUploadFile(filename="   ")
        result = await process_tool(tool_name="DummyTool", file=file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_dot_filename(self):
        file = MockUploadFile(filename=".")
        result = await process_tool(tool_name="DummyTool", file=file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_dot_dot_filename(self):
        file = MockUploadFile(filename="..")
        result = await process_tool(tool_name="DummyTool", file=file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_valid_filename(self):
        file = MockUploadFile(filename="test.txt")
        result = await process_tool(tool_name="DummyTool", file=file, text_input=None)
        self.assertEqual(result["filename"], "test.txt")

    async def test_file_upload_path_traversal(self):
        file = MockUploadFile(filename="../../../etc/passwd")
        result = await process_tool(tool_name="DummyTool", file=file, text_input=None)
        self.assertEqual(result["filename"], "passwd")

if __name__ == "__main__":
    unittest.main()
