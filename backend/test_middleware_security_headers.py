import unittest
from unittest.mock import AsyncMock, MagicMock
import sys


# Mocking FastAPI to avoid actual import errors in restricted environments if any
def identity_decorator_factory(*args, **kwargs):
    def decorator(func):
        return func

    return decorator


class MockJSONResponse:
    def __init__(self, status_code, content):
        self.status_code = status_code
        import json

        self.body = json.dumps(content).encode()


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

from main import security_headers_middleware  # noqa: E402


class MockResponse:
    def __init__(self):
        self.headers = {}


class TestSecurityHeadersMiddleware(unittest.IsolatedAsyncioTestCase):
    async def test_security_headers_added(self):
        request = MagicMock()
        mock_response = MockResponse()
        call_next = AsyncMock(return_value=mock_response)

        response = await security_headers_middleware(request, call_next)
        self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(response.headers.get("X-Frame-Options"), "DENY")
        self.assertEqual(
            response.headers.get("Strict-Transport-Security"),
            "max-age=31536000; includeSubDomains",
        )
        self.assertEqual(
            response.headers.get("Content-Security-Policy"),
            "default-src 'self'; script-src 'self'; object-src 'none';",
        )


if __name__ == "__main__":
    unittest.main()
