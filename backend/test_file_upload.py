import unittest
from unittest.mock import MagicMock
import sys
import asyncio
from typing import Optional

# Reuse the existing mocks from test_middleware to avoid cross-contamination
from test_middleware import mock_fastapi, mock_responses, identity_decorator_factory

# Now import main. The module is already patched.
import main
from main import process_tool

class TestFileUploadSanitization(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        # Append a dummy tool so find_tool doesn't fail
        main.TOOLS.append({
            "tool_name": "TestTool",
            "category": "Test",
            "output_type": "Unknown"
        })

    @classmethod
    def tearDownClass(cls):
        # Remove the dummy tool
        main.TOOLS = [t for t in main.TOOLS if t["tool_name"] != "TestTool"]

    async def _test_filename(self, filename: Optional[str], expected_filename: str):
        mock_file = MagicMock()
        mock_file.filename = filename

        result = await process_tool(tool_name="TestTool", file=mock_file, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["input_type"], "file")
        self.assertEqual(result["filename"], expected_filename)
        self.assertEqual(result["download_url"], f"/download/processed_{expected_filename}")

    async def test_normal_filename(self):
        await self._test_filename("document.pdf", "document.pdf")

    async def test_none_filename(self):
        await self._test_filename(None, "unnamed")

    async def test_empty_filename(self):
        await self._test_filename("", "unnamed")

    async def test_whitespace_filename(self):
        await self._test_filename("   ", "unnamed")

    async def test_dot_filename(self):
        await self._test_filename(".", "unnamed")

    async def test_dotdot_filename(self):
        await self._test_filename("..", "unnamed")

    async def test_path_traversal_filename(self):
        await self._test_filename("../../../etc/passwd", "passwd")

if __name__ == "__main__":
    unittest.main()
