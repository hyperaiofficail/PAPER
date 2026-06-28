import unittest
from unittest.mock import MagicMock
import os
import sys
import json

# Reuse existing mocks
import test_middleware
from main import process_tool, TOOLS

class TestProcessTool(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.dummy_tool = {"tool_name": "DummyTool", "category": "Test", "output_type": "text"}
        if self.dummy_tool not in TOOLS:
            TOOLS.append(self.dummy_tool)

    async def test_process_tool_filename_none(self):
        mock_file = MagicMock()
        mock_file.filename = None

        result = await process_tool("DummyTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_filename_empty(self):
        mock_file = MagicMock()
        mock_file.filename = "   "

        result = await process_tool("DummyTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_filename_dot(self):
        mock_file = MagicMock()
        mock_file.filename = "."

        result = await process_tool("DummyTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_filename_dotdot(self):
        mock_file = MagicMock()
        mock_file.filename = ".."

        result = await process_tool("DummyTool", file=mock_file, text_input=None)
        self.assertEqual(result["filename"], "unnamed")

if __name__ == "__main__":
    unittest.main()
