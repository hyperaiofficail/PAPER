## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.
## 2026-03-16 - DoS via Resource Exhaustion (Missing Upload Limits)
**Vulnerability:** FastAPI endpoints accepting file uploads (`UploadFile`) default to spooling large payloads directly to disk, allowing unbounded disk/memory usage and Denial of Service (DoS) attacks.
**Learning:** Checking the file size *within* the endpoint logic using `file.file.seek()` or similar is too late because the ASGI framework processes the entire stream beforehand.
**Prevention:** Always implement an ASGI middleware (`BaseHTTPMiddleware`) to intercept requests before they hit endpoint routing. Reject requests with missing/invalid `Content-Length`, oversized `Content-Length`, or `Transfer-Encoding: chunked`.
