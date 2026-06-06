import unittest
from unittest.mock import AsyncMock, MagicMock
import sys

# Import the existing mocks from test_middleware
# This ensures we don't clobber the sys.modules setup and cause isinstance failures
import test_middleware

from main import process_tool, TOOLS

class TestFileUploadSecurity(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Ensure there is a dummy tool so find_tool succeeds
        self.dummy_tool_name = "DummyTool"
        TOOLS.append({
            "tool_name": self.dummy_tool_name,
            "category": "Test",
            "output_type": "text"
        })

    def tearDown(self):
        # Remove the dummy tool
        TOOLS[:] = [t for t in TOOLS if t["tool_name"] != self.dummy_tool_name]

    async def test_file_upload_filename_none(self):
        """Test that a file with filename=None doesn't crash the server (DoS)"""
        mock_file = MagicMock()
        mock_file.filename = None

        result = await process_tool(self.dummy_tool_name, file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_file_upload_filename_empty(self):
        """Test that an empty filename correctly falls back to 'unnamed'"""
        mock_file = MagicMock()
        mock_file.filename = ""

        result = await process_tool(self.dummy_tool_name, file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_filename_dot(self):
        """Test that a filename of '.' correctly falls back to 'unnamed'"""
        mock_file = MagicMock()
        mock_file.filename = "."

        result = await process_tool(self.dummy_tool_name, file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_filename_dot_dot(self):
        """Test that a filename of '..' correctly falls back to 'unnamed'"""
        mock_file = MagicMock()
        mock_file.filename = ".."

        result = await process_tool(self.dummy_tool_name, file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_filename_path_traversal(self):
        """Test that path traversal sequences are correctly sanitized"""
        mock_file = MagicMock()
        mock_file.filename = "../../etc/passwd"

        result = await process_tool(self.dummy_tool_name, file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "passwd")

    async def test_file_upload_filename_windows_path_traversal(self):
        """Test that Windows path traversal sequences are correctly sanitized"""
        mock_file = MagicMock()
        mock_file.filename = "..\\..\\Windows\\System32\\cmd.exe"

        result = await process_tool(self.dummy_tool_name, file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "cmd.exe")


if __name__ == "__main__":
    unittest.main()
