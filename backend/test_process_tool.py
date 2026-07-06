import unittest
from unittest.mock import MagicMock
import test_middleware  # sets up sys.modules["fastapi"]
from main import process_tool, TOOLS
import sys

# HTTPException from FastAPI mock must be a proper exception
class MockHTTPException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail

sys.modules["fastapi"].HTTPException = MockHTTPException

import asyncio

class TestProcessTool(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        if not any(t["tool_name"] == "dummy_tool" for t in TOOLS):
            TOOLS.append({"tool_name": "dummy_tool", "category": "dummy"})

    async def test_file_filename_none(self):
        file_mock = MagicMock()
        file_mock.filename = None

        result = await process_tool("dummy_tool", file=file_mock)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_filename_dotdot(self):
        file_mock = MagicMock()
        file_mock.filename = "../../"

        result = await process_tool("dummy_tool", file=file_mock)
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_filename_whitespace(self):
        file_mock = MagicMock()
        file_mock.filename = "  "

        result = await process_tool("dummy_tool", file=file_mock)
        self.assertEqual(result["filename"], "unnamed")

if __name__ == "__main__":
    unittest.main()
