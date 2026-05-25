import unittest
import sys
from unittest.mock import MagicMock


# Setup mocked FastAPI environment to avoid import errors
def identity_decorator_factory(*args, **kwargs):
    def decorator(func):
        return func

    return decorator


class MockFastAPI:
    def __init__(self, *args, **kwargs):
        pass

    def middleware(self, *args, **kwargs):
        return identity_decorator_factory(*args, **kwargs)

    def get(self, *args, **kwargs):
        return identity_decorator_factory(*args, **kwargs)

    def post(self, *args, **kwargs):
        return identity_decorator_factory(*args, **kwargs)

    def add_middleware(self, *args, **kwargs):
        pass


mock_fastapi = MagicMock()
mock_fastapi.FastAPI = MockFastAPI
sys.modules["fastapi"] = mock_fastapi
sys.modules["fastapi.middleware"] = MagicMock()
sys.modules["fastapi.middleware.cors"] = MagicMock()
sys.modules["fastapi.responses"] = MagicMock()

# Now import the logic
from main import process_tool, TOOLS  # noqa: E402


class TestFileUpload(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Add dummy tool to prevent find_tool from failing
        if not any(t.get("tool_name") == "DummyTool" for t in TOOLS):
            TOOLS.append(
                {"tool_name": "DummyTool", "category": "Test", "output_type": "text"}
            )

    async def test_file_upload_none_filename(self):
        mock_file = MagicMock()
        mock_file.filename = None

        result = await process_tool(
            tool_name="DummyTool", file=mock_file, text_input=None
        )
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_dot_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "."

        result = await process_tool(
            tool_name="DummyTool", file=mock_file, text_input=None
        )
        self.assertEqual(result["filename"], "unnamed")

    async def test_file_upload_dotdot_filename(self):
        mock_file = MagicMock()
        mock_file.filename = "..\\"

        result = await process_tool(
            tool_name="DummyTool", file=mock_file, text_input=None
        )
        self.assertEqual(result["filename"], "unnamed")


if __name__ == "__main__":
    unittest.main()
