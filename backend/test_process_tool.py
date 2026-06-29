import unittest
import asyncio
from unittest.mock import MagicMock
import sys

from test_middleware import mock_fastapi
class MockHTTPException(Exception): pass
mock_fastapi.HTTPException = MockHTTPException

from main import process_tool, TOOLS

class TestProcessTool(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Ensure dummy tool exists
        if not any(t.get("tool_name") == "DummyTool" for t in TOOLS):
            TOOLS.append({"tool_name": "DummyTool", "category": "Test", "output_type": "Text"})

    async def test_file_upload_none_filename(self):
        file_mock = MagicMock()
        file_mock.filename = None

        try:
            res = await process_tool("DummyTool", file=file_mock, text_input=None)
            self.assertEqual(res["filename"], "unnamed")
            self.assertEqual(res["download_url"], "/download/processed_unnamed")
        except Exception as e:
            self.fail(f"process_tool raised an exception: {e}")

    async def test_file_upload_path_traversal_empty(self):
        file_mock = MagicMock()
        file_mock.filename = "../../"

        try:
            res = await process_tool("DummyTool", file=file_mock, text_input=None)
            self.assertEqual(res["filename"], "unnamed")
            self.assertEqual(res["download_url"], "/download/processed_unnamed")
        except Exception as e:
            self.fail(f"process_tool raised an exception: {e}")

    async def test_file_upload_path_traversal_whitespace(self):
        file_mock = MagicMock()
        file_mock.filename = "../../  \t  \n "

        try:
            res = await process_tool("DummyTool", file=file_mock, text_input=None)
            self.assertEqual(res["filename"], "unnamed")
            self.assertEqual(res["download_url"], "/download/processed_unnamed")
        except Exception as e:
            self.fail(f"process_tool raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
