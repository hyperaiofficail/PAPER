import unittest
from unittest.mock import MagicMock
import sys

# We need to ensure fastapi is mocked identically as in test_middleware.py
# since sys.modules is global to the python process when we run both tests.
from test_middleware import mock_fastapi, MockFastAPI

# Mock HTTPException to be a real exception
class MockHTTPException(Exception):
    def __init__(self, status_code, detail=None):
        self.status_code = status_code
        self.detail = detail

mock_fastapi.HTTPException = MockHTTPException

sys.modules["fastapi"] = mock_fastapi
sys.modules["fastapi.middleware"] = MagicMock()
sys.modules["fastapi.middleware.cors"] = MagicMock()
sys.modules["fastapi.responses"] = MagicMock()

# Import main after mocking
import main
from main import process_tool

# Ensure TOOLS has a dummy tool so find_tool doesn't return None
main.TOOLS = [{"tool_name": "DummyTool", "category": "Test"}]

class TestFileUpload(unittest.IsolatedAsyncioTestCase):
    async def test_process_tool_file_filename_none(self):
        file_mock = MagicMock()
        file_mock.filename = None

        result = await process_tool(tool_name="DummyTool", file=file_mock)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_file_filename_empty(self):
        file_mock = MagicMock()
        file_mock.filename = ""

        result = await process_tool(tool_name="DummyTool", file=file_mock)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_file_filename_spaces(self):
        file_mock = MagicMock()
        file_mock.filename = "   "

        result = await process_tool(tool_name="DummyTool", file=file_mock)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_file_filename_dot(self):
        file_mock = MagicMock()
        file_mock.filename = "."

        result = await process_tool(tool_name="DummyTool", file=file_mock)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_file_filename_dotdot(self):
        file_mock = MagicMock()
        file_mock.filename = ".."

        result = await process_tool(tool_name="DummyTool", file=file_mock)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_file_filename_normal(self):
        file_mock = MagicMock()
        file_mock.filename = "test.txt"

        result = await process_tool(tool_name="DummyTool", file=file_mock)
        self.assertEqual(result["filename"], "test.txt")
        self.assertEqual(result["download_url"], "/download/processed_test.txt")

    async def test_process_tool_file_filename_path_traversal(self):
        file_mock = MagicMock()
        file_mock.filename = "../../etc/passwd"

        result = await process_tool(tool_name="DummyTool", file=file_mock)
        self.assertEqual(result["filename"], "passwd")

if __name__ == "__main__":
    unittest.main()
