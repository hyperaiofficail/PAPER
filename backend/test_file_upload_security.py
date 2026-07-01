import unittest
import asyncio
from unittest.mock import AsyncMock, MagicMock
import sys

# Crucial: reuse test_middleware's mocks to prevent cross-contamination errors in unittest discovery
from test_middleware import mock_fastapi, mock_responses, MockJSONResponse

from main import process_tool, TOOLS

# Add a test tool
TOOLS.append({"tool_name": "test_security_tool", "output_type": "text"})

class MockUploadFile:
    def __init__(self, filename):
        self.filename = filename

class TestFileUploadSecurity(unittest.IsolatedAsyncioTestCase):
    async def test_none_filename(self):
        f = MockUploadFile(None)
        res = await process_tool("test_security_tool", file=f)
        self.assertEqual(res["input_type"], "file")
        self.assertEqual(res["filename"], "unnamed")
        self.assertEqual(res["download_url"], "/download/processed_unnamed")

    async def test_whitespace_filename(self):
        f = MockUploadFile("   ")
        res = await process_tool("test_security_tool", file=f)
        self.assertEqual(res["input_type"], "file")
        self.assertEqual(res["filename"], "unnamed")

    async def test_path_traversal_filename(self):
        f = MockUploadFile("../../../etc/passwd")
        res = await process_tool("test_security_tool", file=f)
        self.assertEqual(res["input_type"], "file")
        self.assertEqual(res["filename"], "passwd")

    async def test_empty_filename(self):
        f = MockUploadFile("")
        res = await process_tool("test_security_tool", file=f)
        self.assertEqual(res["input_type"], "file")
        self.assertEqual(res["filename"], "unnamed")

    async def test_windows_path_traversal(self):
        f = MockUploadFile("..\\..\\windows\\system32\\cmd.exe")
        res = await process_tool("test_security_tool", file=f)
        self.assertEqual(res["input_type"], "file")
        self.assertEqual(res["filename"], "cmd.exe")

    async def test_dot_dot_filename(self):
        f = MockUploadFile("..")
        res = await process_tool("test_security_tool", file=f)
        self.assertEqual(res["input_type"], "file")
        self.assertEqual(res["filename"], "unnamed")

    async def test_normal_filename(self):
        f = MockUploadFile("normal_file.txt")
        res = await process_tool("test_security_tool", file=f)
        self.assertEqual(res["input_type"], "file")
        self.assertEqual(res["filename"], "normal_file.txt")

if __name__ == "__main__":
    unittest.main()
