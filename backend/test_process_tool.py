import unittest
from unittest.mock import AsyncMock, MagicMock
import sys

# Reuse mocks from test_middleware to prevent sys.modules cross-contamination
from test_middleware import mock_fastapi, mock_responses, MockJSONResponse

class MockHTTPException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail

mock_fastapi.HTTPException = MockHTTPException

# Import main after mocks are set up
from main import process_tool, TOOLS

class TestProcessTool(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure there's at least one tool to test with
        cls.test_tool_name = "DummyTool"
        if not any(t["tool_name"] == cls.test_tool_name for t in TOOLS):
            TOOLS.append({
                "tool_name": cls.test_tool_name,
                "category": "Test",
                "description": "Dummy tool for testing",
                "output_type": "text"
            })

    async def test_process_tool_valid_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "test_image.png"

        result = await process_tool(tool_name=self.test_tool_name, file=file_mock, text_input=None)

        self.assertEqual(result["input_type"], "file")
        self.assertEqual(result["filename"], "test_image.png")
        self.assertEqual(result["download_url"], "/download/processed_test_image.png")

    async def test_process_tool_none_filename(self):
        file_mock = MagicMock()
        file_mock.filename = None

        result = await process_tool(tool_name=self.test_tool_name, file=file_mock, text_input=None)

        self.assertEqual(result["input_type"], "file")
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_empty_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "   "

        result = await process_tool(tool_name=self.test_tool_name, file=file_mock, text_input=None)

        self.assertEqual(result["input_type"], "file")
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_dot_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "."

        result = await process_tool(tool_name=self.test_tool_name, file=file_mock, text_input=None)

        self.assertEqual(result["input_type"], "file")
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_dot_dot_filename(self):
        file_mock = MagicMock()
        file_mock.filename = ".."

        result = await process_tool(tool_name=self.test_tool_name, file=file_mock, text_input=None)

        self.assertEqual(result["input_type"], "file")
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_path_traversal(self):
        file_mock = MagicMock()
        file_mock.filename = "../../../etc/passwd"

        result = await process_tool(tool_name=self.test_tool_name, file=file_mock, text_input=None)

        self.assertEqual(result["input_type"], "file")
        self.assertEqual(result["filename"], "passwd")
        self.assertEqual(result["download_url"], "/download/processed_passwd")

    async def test_process_tool_windows_path_traversal(self):
        file_mock = MagicMock()
        file_mock.filename = "..\\..\\..\\Windows\\System32\\cmd.exe"

        result = await process_tool(tool_name=self.test_tool_name, file=file_mock, text_input=None)

        self.assertEqual(result["input_type"], "file")
        self.assertEqual(result["filename"], "cmd.exe")
        self.assertEqual(result["download_url"], "/download/processed_cmd.exe")

if __name__ == "__main__":
    unittest.main()
