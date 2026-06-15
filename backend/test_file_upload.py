import unittest
import sys
from unittest.mock import MagicMock

# Reuse existing mock logic for FastAPI
from test_middleware import mock_fastapi, mock_responses, MockJSONResponse, identity_decorator_factory

class TestFileUpload(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # We must import main *after* mocking
        import main
        self.main = main

        # Add a dummy tool so find_tool succeeds
        self.dummy_tool = {
            "tool_name": "test_upload_tool",
            "category": "Testing",
            "description": "Dummy tool for upload testing",
            "input_type": "file",
            "output_type": "file"
        }
        if self.dummy_tool not in self.main.TOOLS:
            self.main.TOOLS.append(self.dummy_tool)

    def tearDown(self):
        # Remove dummy tool to avoid side effects
        if self.dummy_tool in self.main.TOOLS:
            self.main.TOOLS.remove(self.dummy_tool)

    async def test_process_tool_none_filename(self):
        # file.filename = None -> raw_filename = "", filename = "" -> fallback to "unnamed"
        file_mock = MagicMock()
        file_mock.filename = None

        result = await self.main.process_tool("test_upload_tool", file=file_mock)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_empty_filename(self):
        file_mock = MagicMock()
        file_mock.filename = ""

        result = await self.main.process_tool("test_upload_tool", file=file_mock)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_whitespace_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "   "

        result = await self.main.process_tool("test_upload_tool", file=file_mock)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_dot_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "."

        result = await self.main.process_tool("test_upload_tool", file=file_mock)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_dotdot_filename(self):
        file_mock = MagicMock()
        file_mock.filename = ".."

        result = await self.main.process_tool("test_upload_tool", file=file_mock)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_path_traversal(self):
        file_mock = MagicMock()
        file_mock.filename = "../../../etc/passwd"

        result = await self.main.process_tool("test_upload_tool", file=file_mock)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "passwd")

    async def test_process_tool_valid_filename(self):
        file_mock = MagicMock()
        file_mock.filename = "my_report.pdf"

        result = await self.main.process_tool("test_upload_tool", file=file_mock)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "my_report.pdf")

if __name__ == "__main__":
    unittest.main()
