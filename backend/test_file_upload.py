import unittest
from unittest.mock import MagicMock
import sys

# We need to test the file upload behavior and its edge cases.
# We will reuse the mock objects from test_middleware if they are available.
try:
    from test_middleware import mock_fastapi
except ImportError:
    mock_fastapi = MagicMock()
    mock_responses = MagicMock()
    sys.modules["fastapi"] = mock_fastapi
    sys.modules["fastapi.middleware"] = MagicMock()
    sys.modules["fastapi.middleware.cors"] = MagicMock()
    sys.modules["fastapi.responses"] = mock_responses

from main import process_tool, TOOLS

class TestProcessToolFileUpload(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # We need a dummy tool to be present in TOOLS to test process_tool
        self.dummy_tool_name = "DummyTool"
        self.dummy_tool = {
            "tool_name": self.dummy_tool_name,
            "category": "Test",
            "output_type": "string"
        }
        TOOLS.append(self.dummy_tool)

    def tearDown(self):
        # Clean up the dummy tool
        if self.dummy_tool in TOOLS:
            TOOLS.remove(self.dummy_tool)

    async def test_process_tool_valid_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "test_image.png"
        result = await process_tool(tool_name=self.dummy_tool_name, file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "test_image.png")
        self.assertEqual(result["download_url"], "/download/processed_test_image.png")

    async def test_process_tool_none_filename(self):
        mock_file = MagicMock()
        mock_file.filename = None
        result = await process_tool(tool_name=self.dummy_tool_name, file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_empty_filename(self):
        mock_file = MagicMock()
        mock_file.filename = ""
        result = await process_tool(tool_name=self.dummy_tool_name, file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_dot_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "."
        result = await process_tool(tool_name=self.dummy_tool_name, file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_dot_dot_filename(self):
        mock_file = MagicMock()
        mock_file.filename = ".."
        result = await process_tool(tool_name=self.dummy_tool_name, file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_whitespace_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "   "
        result = await process_tool(tool_name=self.dummy_tool_name, file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_path_traversal_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "../../etc/passwd"
        result = await process_tool(tool_name=self.dummy_tool_name, file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "passwd")
        self.assertEqual(result["download_url"], "/download/processed_passwd")

    async def test_process_tool_backslash_traversal_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "..\\..\\Windows\\System32\\cmd.exe"
        result = await process_tool(tool_name=self.dummy_tool_name, file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "cmd.exe")
        self.assertEqual(result["download_url"], "/download/processed_cmd.exe")

if __name__ == '__main__':
    unittest.main()
