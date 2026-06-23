import unittest
from unittest.mock import AsyncMock, MagicMock
import sys
import asyncio

# Setup mocks by importing from test_middleware
import test_middleware
from test_middleware import mock_fastapi

# Make sure HTTPException is a proper Exception subclass
class MockHTTPException(Exception):
    def __init__(self, status_code, detail=None):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

mock_fastapi.HTTPException = MockHTTPException

# Now we can import main
import main

class MockUploadFile:
    def __init__(self, filename):
        self.filename = filename

class TestProcessTool(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.dummy_tool = {
            "tool_name": "dummy_tool",
            "category": "Test",
            "description": "A dummy tool",
            "output_type": "text",
        }
        main.TOOLS.append(self.dummy_tool)

    def tearDown(self):
        main.TOOLS.remove(self.dummy_tool)

    async def test_valid_file(self):
        file = MockUploadFile("valid_file.txt")
        result = await main.process_tool("dummy_tool", file=file, text_input=None)
        self.assertEqual(result["filename"], "valid_file.txt")

    async def test_none_filename(self):
        file = MockUploadFile(None)
        # This will fail with the current code, but let's see
        try:
            result = await main.process_tool("dummy_tool", file=file, text_input=None)
            self.assertEqual(result["filename"], "unnamed")
        except AttributeError as e:
            self.fail(f"Failed with AttributeError: {e}")

    async def test_path_traversal(self):
        file = MockUploadFile("../../../etc/passwd")
        result = await main.process_tool("dummy_tool", file=file, text_input=None)
        self.assertEqual(result["filename"], "passwd")

if __name__ == "__main__":
    unittest.main()
