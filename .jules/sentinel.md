## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-03-01 - DoS Risk via Unrestricted File Uploads in FastAPI
**Vulnerability:** The `/process/{tool_name}` endpoint allowed unrestricted file uploads. Because FastAPI handles file streaming framework-side, an attacker could stream extremely large files or use chunked encoding to exhaust server resources (memory/disk) before the endpoint logic even executes.
**Learning:** Checking file sizes inside the endpoint using `seek()` and `tell()` is ineffective against resource exhaustion because the framework has already spooled the payload.
**Prevention:** Always implement a file size limit early in the request lifecycle via ASGI middleware. Enforce a maximum `Content-Length`, explicitly reject `Transfer-Encoding: chunked` (which bypasses length checks), and gracefully handle malformed headers.
