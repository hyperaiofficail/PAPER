import unittest
import sys
from unittest.mock import AsyncMock, MagicMock
from test_middleware import mock_fastapi, mock_responses, MockJSONResponse, identity_decorator_factory

# Import test_middleware to reuse sys.modules mocks before importing main
import test_middleware

from main import process_tool, TOOLS, find_tool

class TestProcessToolSanitization(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Add a dummy tool to TOOLS for testing so find_tool doesn't fail
        if not find_tool("test_tool"):
            TOOLS.append({"tool_name": "test_tool", "category": "test", "output_type": "text"})

    async def test_process_tool_no_filename(self):
        # Simulate a file without a filename
        mock_file = MagicMock()
        mock_file.filename = None

        result = await process_tool("test_tool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_empty_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "   "

        result = await process_tool("test_tool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_dot_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "."

        result = await process_tool("test_tool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_dotdot_filename(self):
        mock_file = MagicMock()
        mock_file.filename = ".."

        result = await process_tool("test_tool", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_path_traversal(self):
        mock_file = MagicMock()
        mock_file.filename = "../../../etc/passwd"

        result = await process_tool("test_tool", file=mock_file)
        self.assertEqual(result["filename"], "passwd")

if __name__ == '__main__':
    unittest.main()
