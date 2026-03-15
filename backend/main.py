import json
import os
from typing import Optional
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.responses import JSONResponse

app = FastAPI()

# Security configuration
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB limit


class ContentLengthLimitMiddleware:
    """
    Middleware to limit the maximum size of incoming requests to prevent DoS attacks
    via resource exhaustion. This intercepts requests early before parsing.
    """

    def __init__(self, app: ASGIApp, max_upload_size: int = MAX_UPLOAD_SIZE):
        self.app = app
        self.max_upload_size = max_upload_size

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Only check POST, PUT, PATCH where payloads are expected
        if scope["method"] in ["POST", "PUT", "PATCH"]:
            headers = dict(scope.get("headers", []))

            # Reject chunked transfer encoding as it bypasses content-length checks
            if (
                b"transfer-encoding" in headers
                and b"chunked" in headers[b"transfer-encoding"]
            ):
                response = JSONResponse(
                    {"detail": "Chunked transfer encoding is not allowed."},
                    status_code=411,
                )
                await response(scope, receive, send)
                return

            if b"content-length" in headers:
                try:
                    content_length = int(headers[b"content-length"])
                    if content_length > self.max_upload_size:
                        response = JSONResponse(
                            {
                                "detail": f"Request body too large. Maximum size is {self.max_upload_size} bytes."
                            },
                            status_code=413,
                        )
                        await response(scope, receive, send)
                        return
                except ValueError:
                    response = JSONResponse(
                        {"detail": "Invalid Content-Length header."},
                        status_code=400,
                    )
                    await response(scope, receive, send)
                    return

        await self.app(scope, receive, send)


app.add_middleware(ContentLengthLimitMiddleware)

# Enable CORS
allowed_origins_env = os.environ.get("ALLOWED_ORIGINS")
if allowed_origins_env:
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",")]
else:
    allowed_origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load tools
TOOLS_FILE = os.path.join(os.path.dirname(__file__), "..", "tools.json")

# Security configuration
MAX_TEXT_INPUT_LENGTH = 10000

try:
    with open(TOOLS_FILE, "r") as f:
        TOOLS = json.load(f)
except FileNotFoundError:
    # Fallback if running from a different directory context or file moved
    if os.path.exists("tools.json"):
        with open("tools.json", "r") as f:
            TOOLS = json.load(f)
    else:
        TOOLS = []
        print("Warning: tools.json not found")


# Helper to find tool
def find_tool(tool_name: str):
    # Case insensitive search might be better, but exact match for now
    for tool in TOOLS:
        if tool["tool_name"] == tool_name:
            return tool
    return None


@app.get("/tools")
def get_tools(category: Optional[str] = None):
    if category:
        return [t for t in TOOLS if t["category"] == category]
    return TOOLS


@app.get("/tool/{tool_name}")
def get_tool(tool_name: str):
    tool = find_tool(tool_name)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool


@app.post("/process/{tool_name}")
async def process_tool(
    tool_name: str,
    file: Optional[UploadFile] = File(None),
    text_input: Optional[str] = Form(None),
):
    tool = find_tool(tool_name)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    # Placeholder logic
    result = {
        "tool": tool_name,
        "status": "success",
        "message": f"Successfully processed input for {tool_name}",
        "output_type": tool.get("output_type", "Unknown"),
    }

    if file:
        result["input_type"] = "file"
        # Sanitize filename to prevent path traversal
        # We handle both / and \ as separators
        filename = os.path.basename(file.filename.replace("\\", "/"))
        result["filename"] = filename
        # Simulate processing file
        result["download_url"] = f"/download/processed_{filename}"
    elif text_input:
        if len(text_input) > MAX_TEXT_INPUT_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Text input too long. Max length is {MAX_TEXT_INPUT_LENGTH} characters.",
            )

        result["input_type"] = "text"
        result["text_length"] = len(text_input)

        # Simple dummy logic for demonstration
        if "Case" in tool_name:
            result["output"] = text_input.upper()
        elif "Reverse" in tool_name:
            result["output"] = text_input[::-1]
        elif "Count" in tool_name:
            result["output"] = f"Word count: {len(text_input.split())}"
        else:
            result["output"] = f"Processed: {text_input}"

    else:
        result["message"] = "No input provided"

    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
