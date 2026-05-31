import unittest

# Ensure sys.modules is patched by reusing test_middleware's mocks
import test_middleware  # noqa: F401

from main import process_tool, TOOLS  # noqa: E402


class TestFileUpload(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        if not any(t.get("tool_name") == "TestTool" for t in TOOLS):
            TOOLS.append(
                {"tool_name": "TestTool", "category": "Test", "output_type": "text"}
            )

    async def test_filename_sanitization_none(self):
        class MockFile:
            filename = None

        result = await process_tool("TestTool", file=MockFile(), text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_filename_sanitization_dot(self):
        class MockFile:
            filename = "."

        result = await process_tool("TestTool", file=MockFile(), text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_filename_sanitization_dotdot(self):
        class MockFile:
            filename = ".."

        result = await process_tool("TestTool", file=MockFile(), text_input=None)
        self.assertEqual(result["filename"], "unnamed")

    async def test_filename_sanitization_empty(self):
        class MockFile:
            filename = "   "

        result = await process_tool("TestTool", file=MockFile(), text_input=None)
        self.assertEqual(result["filename"], "unnamed")


if __name__ == "__main__":
    unittest.main()
