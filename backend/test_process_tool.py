import unittest
from unittest.mock import MagicMock
import sys
import json

# Setup mocks identically to test_middleware.py to share sys.modules state cleanly
from test_middleware import mock_fastapi, mock_responses, MockJSONResponse

# Mock HTTPException to actually raise so we can catch it
class MockHTTPException(Exception):
    def __init__(self, status_code, detail=None):
        self.status_code = status_code
        self.detail = detail
mock_fastapi.HTTPException = MockHTTPException

# Mock File, UploadFile, Form, Request for main.py imports
class MockUploadFile:
    def __init__(self, filename):
        self.filename = filename
mock_fastapi.UploadFile = MockUploadFile
mock_fastapi.File = MagicMock(return_value=None)
mock_fastapi.Form = MagicMock(return_value=None)
mock_fastapi.Request = MagicMock()

from main import process_tool, TOOLS

class TestProcessTool(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        TOOLS.append({"tool_name": "TestTool", "output_type": "text"})

    def tearDown(self):
        TOOLS.pop()

    async def test_file_upload_path_traversal(self):
        malicious_file = MockUploadFile(filename="../../../etc/passwd")
        result = await process_tool("TestTool", file=malicious_file)
        self.assertEqual(result["filename"], "passwd")

        malicious_file_2 = MockUploadFile(filename="..\\..\\..\\Windows\\System32\\cmd.exe")
        result_2 = await process_tool("TestTool", file=malicious_file_2)
        self.assertEqual(result_2["filename"], "cmd.exe")

    async def test_file_upload_none_filename(self):
        none_file = MockUploadFile(filename=None)
        result = await process_tool("TestTool", file=none_file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_empty_filename(self):
        empty_file = MockUploadFile(filename="")
        result = await process_tool("TestTool", file=empty_file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_whitespace_filename(self):
        whitespace_file = MockUploadFile(filename="   ")
        result = await process_tool("TestTool", file=whitespace_file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_dot_filename(self):
        dot_file = MockUploadFile(filename=".")
        result = await process_tool("TestTool", file=dot_file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_dot_dot_filename(self):
        dot_dot_file = MockUploadFile(filename="..")
        result = await process_tool("TestTool", file=dot_dot_file)
        self.assertEqual(result["filename"], "unnamed")

if __name__ == '__main__':
    unittest.main()
