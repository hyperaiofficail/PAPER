import unittest
from unittest.mock import AsyncMock, MagicMock
import sys

# Import the mock setup from test_middleware
import test_middleware

from main import process_tool, TOOLS

class TestProcessTool(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Add a dummy tool
        if not any(t.get("tool_name") == "dummy" for t in TOOLS):
            TOOLS.append({"tool_name": "dummy", "category": "test"})

    async def test_process_tool_none_filename(self):
        mock_file = MagicMock()
        mock_file.filename = None

        result = await process_tool("dummy", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_empty_filename(self):
        mock_file = MagicMock()
        mock_file.filename = ""

        result = await process_tool("dummy", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_whitespace_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "   "

        result = await process_tool("dummy", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_dot_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "."

        result = await process_tool("dummy", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_dotdot_filename(self):
        mock_file = MagicMock()
        mock_file.filename = ".."

        result = await process_tool("dummy", file=mock_file)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_valid_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "test.txt"

        result = await process_tool("dummy", file=mock_file)
        self.assertEqual(result["filename"], "test.txt")

if __name__ == "__main__":
    unittest.main()
