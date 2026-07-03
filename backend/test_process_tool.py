import unittest
from unittest.mock import MagicMock
import sys
import asyncio

# Setup mocks identically to test_middleware to ensure consistency
from test_middleware import mock_fastapi, mock_responses, MockJSONResponse
# Re-apply mocks locally just in case
sys.modules["fastapi"] = mock_fastapi
sys.modules["fastapi.middleware"] = MagicMock()
sys.modules["fastapi.middleware.cors"] = MagicMock()
sys.modules["fastapi.responses"] = mock_responses

# Now import main
from main import process_tool, TOOLS

class MockUploadFile:
    def __init__(self, filename):
        self.filename = filename

class TestProcessToolSanitization(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Ensure a dummy tool exists so process_tool doesn't 404
        self.dummy_tool = {"tool_name": "TestSanitizationTool", "category": "Test"}
        if not any(t["tool_name"] == self.dummy_tool["tool_name"] for t in TOOLS):
            TOOLS.append(self.dummy_tool)

    async def test_filename_none(self):
        # Simulate a file with None as filename
        mock_file = MockUploadFile(filename=None)

        # This should not raise an AttributeError
        result = await process_tool("TestSanitizationTool", file=mock_file, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")

    async def test_filename_empty(self):
        mock_file = MockUploadFile(filename="")
        result = await process_tool("TestSanitizationTool", file=mock_file, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")

    async def test_filename_dot(self):
        mock_file = MockUploadFile(filename=".")
        result = await process_tool("TestSanitizationTool", file=mock_file, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")

    async def test_filename_dotdot(self):
        mock_file = MockUploadFile(filename="..")
        result = await process_tool("TestSanitizationTool", file=mock_file, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")

    async def test_filename_whitespace(self):
        mock_file = MockUploadFile(filename="   ")
        result = await process_tool("TestSanitizationTool", file=mock_file, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "unnamed")

    async def test_filename_normal(self):
        mock_file = MockUploadFile(filename="image.png")
        result = await process_tool("TestSanitizationTool", file=mock_file, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "image.png")

    async def test_filename_path_traversal(self):
        mock_file = MockUploadFile(filename="../../etc/passwd")
        result = await process_tool("TestSanitizationTool", file=mock_file, text_input=None)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["filename"], "passwd")

if __name__ == "__main__":
    unittest.main()
