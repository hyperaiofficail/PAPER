import json
import os
import time
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load tools
TOOLS_FILE = os.path.join(os.path.dirname(__file__), "..", "tools.json")

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

class ToolResponse(BaseModel):
    tool_name: str
    status: str
    input_received: str
    output_type: str
    output_data: Optional[Any] = None
    message: str
    processing_time_ms: int
    settings_used: Optional[Dict[str, Any]] = None

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

@app.post("/process/{tool_name}", response_model=ToolResponse)
async def process_tool(
    tool_name: str,
    file: Optional[UploadFile] = File(None),
    text_input: Optional[str] = Form(None),
    settings: Optional[str] = Form(None) # JSON string of settings
):
    start_time = time.time()

    tool = find_tool(tool_name)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    parsed_settings = {}
    if settings:
        try:
            parsed_settings = json.loads(settings)
        except:
            pass

    # Simulate processing time
    time.sleep(0.5)

    response = {
        "tool_name": tool_name,
        "status": "success",
        "input_received": "",
        "output_type": tool.get("output_type", "Unknown"),
        "output_data": None,
        "message": "",
        "processing_time_ms": 0,
        "settings_used": parsed_settings if parsed_settings else None
    }

    try:
        if file:
            response["input_received"] = f"File: {file.filename} ({file.content_type})"
            # In a real app, we would process the file here
            # For now, return a dummy download URL or base64
            response["output_data"] = f"https://hyper-tools.com/output/processed_{file.filename}"
            response["message"] = f"Successfully processed {file.filename}"

        elif text_input:
            response["input_received"] = f"Text input (length: {len(text_input)})"

            # Simple dummy logic for demonstration
            if "Case" in tool_name:
                response["output_data"] = text_input.upper()
                response["message"] = "Text converted to uppercase"
            elif "Reverse" in tool_name:
                 response["output_data"] = text_input[::-1]
                 response["message"] = "Text reversed"
            elif "Count" in tool_name:
                 response["output_data"] = f"Word count: {len(text_input.split())}"
                 response["message"] = "Words counted"
            elif "QR" in tool_name:
                 response["output_type"] = "QR Code"
                 response["output_data"] = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==" # 1x1 pixel dummy QR
                 response["message"] = "QR Code generated"
            else:
                 response["output_data"] = f"Processed: {text_input}"
                 response["message"] = "Input processed successfully"

        else:
            response["status"] = "error"
            response["message"] = "No input provided"
            response["input_received"] = "None"

    except Exception as e:
        response["status"] = "error"
        response["message"] = str(e)

    end_time = time.time()
    response["processing_time_ms"] = int((end_time - start_time) * 1000)

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
