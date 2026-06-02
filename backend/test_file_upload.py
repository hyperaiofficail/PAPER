import unittest
from unittest.mock import MagicMock
import sys

# Setup sys.modules for FastAPI using existing mocks from test_middleware
from test_middleware import mock_fastapi, mock_responses, MockJSONResponse

sys.modules["fastapi"] = mock_fastapi
sys.modules["fastapi.responses"] = mock_responses
sys.modules["fastapi.middleware"] = MagicMock()
sys.modules["fastapi.middleware.cors"] = MagicMock()

# Import the logic to test
from main import process_tool, TOOLS  # noqa: E402

# Append a dummy tool so `find_tool` passes
DUMMY_TOOL = {"tool_name": "TestTool", "output_type": "text"}
if DUMMY_TOOL not in TOOLS:
    TOOLS.append(DUMMY_TOOL)


class TestFileUpload(unittest.IsolatedAsyncioTestCase):
    async def test_file_upload_none_filename(self):
        file = MagicMock()
        file.filename = None
        result = await process_tool("TestTool", file=file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_dot_filename(self):
        file = MagicMock()
        file.filename = "."
        result = await process_tool("TestTool", file=file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_dot_dot_filename(self):
        file = MagicMock()
        file.filename = ".."
        result = await process_tool("TestTool", file=file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_empty_filename(self):
        file = MagicMock()
        file.filename = ""
        result = await process_tool("TestTool", file=file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_whitespace_filename(self):
        file = MagicMock()
        file.filename = "   "
        result = await process_tool("TestTool", file=file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_valid_filename(self):
        file = MagicMock()
        file.filename = "valid.txt"
        result = await process_tool("TestTool", file=file)
        self.assertEqual(result["filename"], "valid.txt")


if __name__ == "__main__":
    unittest.main()
