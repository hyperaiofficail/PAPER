import unittest
from unittest.mock import MagicMock
import sys

# Reuse mocks from test_middleware to avoid sys.modules conflicts
try:
    from test_middleware import mock_fastapi, mock_responses
except ImportError:
    # If run individually, setup basic mocks
    def identity_decorator_factory(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

    class MockFastAPI:
        def __init__(self, *args, **kwargs): pass
        def middleware(self, *args, **kwargs): return identity_decorator_factory(*args, **kwargs)
        def get(self, *args, **kwargs): return identity_decorator_factory(*args, **kwargs)
        def post(self, *args, **kwargs): return identity_decorator_factory(*args, **kwargs)
        def add_middleware(self, *args, **kwargs): pass

    class MockJSONResponse:
        def __init__(self, status_code, content):
            self.status_code = status_code
            import json
            self.body = json.dumps(content).encode()

    mock_fastapi = MagicMock()
    mock_fastapi.FastAPI = MockFastAPI
    mock_responses = MagicMock()
    mock_responses.JSONResponse = MockJSONResponse
    sys.modules["fastapi"] = mock_fastapi
    sys.modules["fastapi.middleware"] = MagicMock()
    sys.modules["fastapi.middleware.cors"] = MagicMock()
    sys.modules["fastapi.responses"] = mock_responses


# Mock FastAPI classes used in function signature
class MockUploadFile:
    def __init__(self, filename):
        self.filename = filename

class MockHTTPException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail

mock_fastapi.UploadFile = MockUploadFile
mock_fastapi.HTTPException = MockHTTPException

# Import after mocks
from main import process_tool, TOOLS

class TestFileUploadSecurity(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Add a dummy tool to TOOLS list to allow process_tool to proceed
        self.dummy_tool = {"tool_name": "DummyTool", "category": "Test", "output_type": "json"}
        TOOLS.append(self.dummy_tool)

    def tearDown(self):
        if self.dummy_tool in TOOLS:
            TOOLS.remove(self.dummy_tool)

    async def test_process_tool_none_filename(self):
        file_mock = MockUploadFile(filename=None)
        result = await process_tool("DummyTool", file=file_mock)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_empty_filename(self):
        file_mock = MockUploadFile(filename="")
        result = await process_tool("DummyTool", file=file_mock)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_whitespace_filename(self):
        file_mock = MockUploadFile(filename="   ")
        result = await process_tool("DummyTool", file=file_mock)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_dot_filename(self):
        file_mock = MockUploadFile(filename=".")
        result = await process_tool("DummyTool", file=file_mock)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_dotdot_filename(self):
        file_mock = MockUploadFile(filename="..")
        result = await process_tool("DummyTool", file=file_mock)
        self.assertEqual(result["filename"], "unnamed")
        self.assertEqual(result["download_url"], "/download/processed_unnamed")

    async def test_process_tool_path_traversal(self):
        file_mock = MockUploadFile(filename="../../../etc/passwd")
        result = await process_tool("DummyTool", file=file_mock)
        self.assertEqual(result["filename"], "passwd")
        self.assertEqual(result["download_url"], "/download/processed_passwd")

    async def test_process_tool_windows_path_traversal(self):
        file_mock = MockUploadFile(filename="..\\..\\windows\\system32\\cmd.exe")
        result = await process_tool("DummyTool", file=file_mock)
        self.assertEqual(result["filename"], "cmd.exe")
        self.assertEqual(result["download_url"], "/download/processed_cmd.exe")

if __name__ == '__main__':
    unittest.main()
