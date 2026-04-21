import unittest
from unittest.mock import AsyncMock, MagicMock
import sys


class MockJSONResponse:
    def __init__(self, status_code, content):
        self.status_code = status_code
        import json

        self.body = json.dumps(content).encode()


# Mocking FastAPI to avoid actual import errors in restricted environments if any
# We need `app.middleware` to return the original function so it is not replaced by a MagicMock
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
mock_responses = MagicMock()
mock_responses.JSONResponse = MockJSONResponse
sys.modules["fastapi"] = mock_fastapi
sys.modules["fastapi.middleware"] = MagicMock()
sys.modules["fastapi.middleware.cors"] = MagicMock()
sys.modules["fastapi.responses"] = mock_responses

# Now import main, and `content_length_limit_middleware` will be the actual function.
from main import content_length_limit_middleware, MAX_FILE_SIZE  # noqa: E402


class TestContentLengthLimitMiddleware(unittest.IsolatedAsyncioTestCase):
    async def test_get_request_allowed(self):
        request = MagicMock()
        request.method = "GET"
        request.headers = {"Content-Length": str(MAX_FILE_SIZE + 1)}
        call_next = AsyncMock(return_value="OK")

        response = await content_length_limit_middleware(request, call_next)
        self.assertEqual(response, "OK")
        call_next.assert_called_once_with(request)

    async def test_post_request_allowed_size(self):
        request = MagicMock()
        request.method = "POST"
        request.headers = {"Content-Length": str(MAX_FILE_SIZE)}
        call_next = AsyncMock(return_value="OK")

        response = await content_length_limit_middleware(request, call_next)
        self.assertEqual(response, "OK")
        call_next.assert_called_once_with(request)

    async def test_post_request_too_large(self):
        request = MagicMock()
        request.method = "POST"
        request.headers = {"Content-Length": str(MAX_FILE_SIZE + 1)}
        call_next = AsyncMock()

        response = await content_length_limit_middleware(request, call_next)
        self.assertIsInstance(response, MockJSONResponse)
        self.assertEqual(response.status_code, 413)
        self.assertIn("Payload too large", response.body.decode())
        call_next.assert_not_called()

    async def test_post_request_chunked(self):
        request = MagicMock()
        request.method = "POST"
        request.headers = {"Transfer-Encoding": "chunked"}
        call_next = AsyncMock()

        response = await content_length_limit_middleware(request, call_next)
        self.assertIsInstance(response, MockJSONResponse)
        self.assertEqual(response.status_code, 411)
        self.assertIn(
            "Chunked transfer encoding is not allowed", response.body.decode()
        )
        call_next.assert_not_called()

    async def test_post_request_missing_content_length(self):
        request = MagicMock()
        request.method = "POST"
        request.headers = {}
        call_next = AsyncMock()

        response = await content_length_limit_middleware(request, call_next)
        self.assertIsInstance(response, MockJSONResponse)
        self.assertEqual(response.status_code, 411)
        self.assertIn("Content-Length header is missing", response.body.decode())
        call_next.assert_not_called()

    async def test_post_request_invalid_content_length(self):
        request = MagicMock()
        request.method = "POST"
        request.headers = {"Content-Length": "invalid"}
        call_next = AsyncMock()

        response = await content_length_limit_middleware(request, call_next)
        self.assertIsInstance(response, MockJSONResponse)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid Content-Length header", response.body.decode())
        call_next.assert_not_called()


if __name__ == "__main__":
    unittest.main()
