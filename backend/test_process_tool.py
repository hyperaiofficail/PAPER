import unittest
from unittest.mock import MagicMock

# Reuse existing mock environment to avoid cross-contamination
import test_middleware

from main import process_tool, TOOLS

class TestProcessTool(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Ensure a dummy tool exists
        if not any(t["tool_name"] == "DummyTool" for t in TOOLS):
            TOOLS.append({"tool_name": "DummyTool", "category": "Test", "output_type": "text"})

    async def test_process_tool_none_filename(self):
        mock_file = MagicMock()
        mock_file.filename = None

        result = await process_tool("DummyTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_whitespace_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "   "

        result = await process_tool("DummyTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_dot_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "."

        result = await process_tool("DummyTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_dotdot_filename(self):
        mock_file = MagicMock()
        mock_file.filename = ".."

        result = await process_tool("DummyTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_valid_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "valid.txt"

        result = await process_tool("DummyTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "valid.txt")

if __name__ == "__main__":
    unittest.main()
