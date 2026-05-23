import unittest
import sys
from unittest.mock import MagicMock


# Standard mock for MockJSONResponse for testing
class MockJSONResponse:
    def __init__(self, status_code, content):
        self.status_code = status_code
        import json

        self.body = json.dumps(content).encode()


class MockHTTPException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail


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


def mock_form(default=None, **kwargs):
    return default


def mock_file(default=None, **kwargs):
    return default


class TestFileUploadSanitization(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # We need to setup sys.modules temporarily
        self.original_modules = dict(sys.modules)

        mock_fastapi = MagicMock()
        mock_fastapi.FastAPI = MockFastAPI
        mock_fastapi.HTTPException = MockHTTPException
        mock_fastapi.Form = mock_form
        mock_fastapi.File = mock_file
        mock_fastapi.UploadFile = MagicMock

        mock_responses = MagicMock()
        mock_responses.JSONResponse = MockJSONResponse

        sys.modules["fastapi"] = mock_fastapi
        sys.modules["fastapi.middleware"] = MagicMock()
        sys.modules["fastapi.middleware.cors"] = MagicMock()
        sys.modules["fastapi.responses"] = mock_responses

        # Ensure 'main' is imported cleanly with our mocks
        if "main" in sys.modules:
            del sys.modules["main"]

        import main

        self.main_module = main
        self.process_tool = main.process_tool

        if not main.TOOLS:
            main.TOOLS.append(
                {
                    "tool_name": "TestTool",
                    "category": "Test",
                    "description": "Test tool",
                    "use_case": "Testing",
                    "input_type": "Any",
                    "output_type": "Any",
                }
            )
        self.tool_name = main.TOOLS[0]["tool_name"]

    def tearDown(self):
        # Restore sys.modules to prevent cross-contamination
        sys.modules.clear()
        sys.modules.update(self.original_modules)

    async def _test_filename(self, input_name, expected_name):
        mock_file_obj = MagicMock()
        mock_file_obj.filename = input_name

        result = await self.process_tool(
            tool_name=self.tool_name, file=mock_file_obj, text_input=None
        )

        self.assertEqual(result.get("filename"), expected_name)
        self.assertEqual(
            result.get("download_url"), f"/download/processed_{expected_name}"
        )

    async def test_normal_filename(self):
        await self._test_filename("document.pdf", "document.pdf")

    async def test_none_filename(self):
        await self._test_filename(None, "unnamed")

    async def test_empty_filename(self):
        await self._test_filename("", "unnamed")
        await self._test_filename("   ", "unnamed")

    async def test_path_traversal_linux(self):
        await self._test_filename("../../../etc/passwd", "passwd")
        await self._test_filename("/var/www/html/index.php", "index.php")

    async def test_path_traversal_windows(self):
        await self._test_filename("C:\\Windows\\System32\\cmd.exe", "cmd.exe")
        await self._test_filename("..\\..\\..\\boot.ini", "boot.ini")

    async def test_path_traversal_mixed(self):
        await self._test_filename("foo\\bar/baz.txt", "baz.txt")

    async def test_dot_filename(self):
        await self._test_filename(".", "unnamed")
        await self._test_filename("..", "unnamed")

    async def test_spaces_in_filename(self):
        await self._test_filename("  my secret file.txt  ", "my secret file.txt")


if __name__ == "__main__":
    unittest.main()
