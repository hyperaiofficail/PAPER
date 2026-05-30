import unittest
from unittest.mock import AsyncMock, MagicMock
import sys

# Reuse mocked dependencies from test_middleware to prevent sys.modules conflicts
from test_middleware import mock_fastapi, mock_responses

# Now import main, it will use the mocked FastAPI
import main  # noqa: E402


class TestFileUploadSanitization(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Append a dummy tool to TOOLS so find_tool doesn't fail
        self.dummy_tool = {"tool_name": "test_tool", "category": "test"}
        if self.dummy_tool not in main.TOOLS:
            main.TOOLS.append(self.dummy_tool)

    async def test_file_upload_valid_filename(self):
        file = MagicMock()
        file.filename = "test_file.txt"

        result = await main.process_tool("test_tool", file=file, text_input=None)

        self.assertEqual(result["filename"], "test_file.txt")
        self.assertEqual(result["download_url"], "/download/processed_test_file.txt")

    async def test_file_upload_none_filename(self):
        file = MagicMock()
        file.filename = None

        result = await main.process_tool("test_tool", file=file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_file_upload_empty_filename(self):
        file = MagicMock()
        file.filename = ""

        result = await main.process_tool("test_tool", file=file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_file_upload_whitespace_filename(self):
        file = MagicMock()
        file.filename = "   "

        result = await main.process_tool("test_tool", file=file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_file_upload_dot_filename(self):
        file = MagicMock()
        file.filename = "."

        result = await main.process_tool("test_tool", file=file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_file_upload_dot_dot_filename(self):
        file = MagicMock()
        file.filename = ".."

        result = await main.process_tool("test_tool", file=file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_file_upload_path_traversal_filename(self):
        file = MagicMock()
        file.filename = "../../../etc/passwd"

        result = await main.process_tool("test_tool", file=file, text_input=None)

        self.assertEqual(result["filename"], "passwd")
        self.assertEqual(result["download_url"], "/download/processed_passwd")

    async def test_file_upload_windows_path_traversal_filename(self):
        file = MagicMock()
        file.filename = "..\\..\\..\\Windows\\System32\\cmd.exe"

        result = await main.process_tool("test_tool", file=file, text_input=None)

        self.assertEqual(result["filename"], "cmd.exe")
        self.assertEqual(result["download_url"], "/download/processed_cmd.exe")


if __name__ == "__main__":
    unittest.main()
