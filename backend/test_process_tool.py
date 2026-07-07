import unittest
from unittest.mock import MagicMock
import sys
import os

# Import the mock setup from test_middleware to ensure sys.modules is properly patched
from test_middleware import mock_fastapi

# Mock HTTPException as a real exception so it can be raised and caught
class MockHTTPException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

mock_fastapi.HTTPException = MockHTTPException

# Now import the components from main
from main import process_tool, TOOLS

class TestProcessToolFileUpload(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        # Add a dummy tool to TOOLS list to prevent 404 errors during testing
        cls.dummy_tool_name = "DummyUploadTool"
        TOOLS.append({
            "tool_name": cls.dummy_tool_name,
            "category": "Test",
            "description": "Dummy tool for testing",
            "output_type": "string"
        })

    @classmethod
    def tearDownClass(cls):
        # Remove the dummy tool
        TOOLS[:] = [t for t in TOOLS if t["tool_name"] != cls.dummy_tool_name]

    async def test_file_upload_none_filename(self):
        # file.filename is None
        mock_file = MagicMock()
        mock_file.filename = None

        result = await process_tool(tool_name=self.dummy_tool_name, file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_file_upload_empty_filename(self):
        # file.filename is empty string
        mock_file = MagicMock()
        mock_file.filename = "   "

        result = await process_tool(tool_name=self.dummy_tool_name, file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_file_upload_path_traversal_dot_dot(self):
        # file.filename resolves to '..'
        mock_file = MagicMock()
        mock_file.filename = "../.."

        result = await process_tool(tool_name=self.dummy_tool_name, file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_file_upload_path_traversal_dot(self):
        # file.filename resolves to '.'
        mock_file = MagicMock()
        mock_file.filename = "./."

        result = await process_tool(tool_name=self.dummy_tool_name, file=mock_file)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_file_upload_path_traversal_complex(self):
        # file.filename resolves to a dangerous file name
        mock_file = MagicMock()
        mock_file.filename = "../../../etc/passwd"

        result = await process_tool(tool_name=self.dummy_tool_name, file=mock_file)
        self.assertEqual(result["filename"], "passwd")
        self.assertEqual(result["download_url"], "/download/processed_passwd")

    async def test_file_upload_windows_path_traversal(self):
        # file.filename uses windows backslashes
        mock_file = MagicMock()
        mock_file.filename = "..\\..\\windows\\system32\\cmd.exe"

        result = await process_tool(tool_name=self.dummy_tool_name, file=mock_file)
        self.assertEqual(result["filename"], "cmd.exe")
        self.assertEqual(result["download_url"], "/download/processed_cmd.exe")

    async def test_file_upload_valid_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "my_document.pdf"

        result = await process_tool(tool_name=self.dummy_tool_name, file=mock_file)
        self.assertEqual(result["filename"], "my_document.pdf")
        self.assertEqual(result["download_url"], "/download/processed_my_document.pdf")

if __name__ == "__main__":
    unittest.main()
