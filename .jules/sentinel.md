## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - Denial of Service via Resource Exhaustion in File Uploads
**Vulnerability:** File upload endpoints allowed arbitrarily large payloads, which could exhaust server memory and disk space, leading to a Denial of Service (DoS). The framework-level FastAPI/Starlette handles the payload spooling before endpoint execution.
**Learning:** Checking file sizes inside the route endpoint using `file.file.seek()` or `file.size` is too late, as the payload has already been received and partially or fully processed by the framework.
**Prevention:** Always implement an ASGI middleware to intercept requests and check the `Content-Length` header on POST, PUT, and PATCH methods, returning a 413 Payload Too Large error before the payload is processed.
