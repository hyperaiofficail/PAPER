import unittest
from unittest.mock import AsyncMock, MagicMock
import sys

# Reuse mocks from test_middleware if we need them, or set them up directly
from test_middleware import mock_fastapi

# Set TOOLS variable in main so it has at least one tool
import main
main.TOOLS.append({"tool_name": "TestTool", "category": "Test"})

class TestFileUploadSecurity(unittest.IsolatedAsyncioTestCase):
    async def test_process_tool_no_filename(self):
        file = MagicMock()
        file.filename = None

        result = await main.process_tool("TestTool", file=file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_empty_filename(self):
        file = MagicMock()
        file.filename = ""

        result = await main.process_tool("TestTool", file=file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_whitespace_filename(self):
        file = MagicMock()
        file.filename = "   "

        result = await main.process_tool("TestTool", file=file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_dot_filename(self):
        file = MagicMock()
        file.filename = "."

        result = await main.process_tool("TestTool", file=file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_dotdot_filename(self):
        file = MagicMock()
        file.filename = ".."

        result = await main.process_tool("TestTool", file=file, text_input=None)

        self.assertEqual(result["filename"], "unnamed")

    async def test_process_tool_path_traversal(self):
        file = MagicMock()
        file.filename = "../../../etc/passwd"

        result = await main.process_tool("TestTool", file=file, text_input=None)

        self.assertEqual(result["filename"], "passwd")

    async def test_process_tool_windows_path_traversal(self):
        file = MagicMock()
        file.filename = "..\\..\\..\\Windows\\System32\\cmd.exe"

        result = await main.process_tool("TestTool", file=file, text_input=None)

        self.assertEqual(result["filename"], "cmd.exe")

    async def test_process_tool_valid_filename(self):
        file = MagicMock()
        file.filename = "safe_image.png"

        result = await main.process_tool("TestTool", file=file, text_input=None)

        self.assertEqual(result["filename"], "safe_image.png")

if __name__ == '__main__':
    unittest.main()
