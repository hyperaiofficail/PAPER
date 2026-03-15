## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.
## 2026-03-15 - Framework-Level Payload Limits for DoS Prevention
**Vulnerability:** The backend lacked a global file upload size limit, making it susceptible to Denial of Service (DoS) attacks via resource exhaustion (oversized payloads). Additionally, relying purely on `Content-Length` without handling `Transfer-Encoding: chunked` left a bypass open.
**Learning:** Checking the payload size within the FastAPI endpoint is too late, as the framework may spool the entire large payload into memory or temp files before the endpoint handler is reached. We must intercept requests at the ASGI middleware level, inspecting `Content-Length` and explicitly rejecting `Transfer-Encoding: chunked` to safely block excessive uploads.
**Prevention:** Implement and globally register an ASGI middleware (`ContentLengthLimitMiddleware`) that enforces a strict maximum size (e.g., 10MB) by checking `scope["headers"]` before passing the request to `self.app(scope, receive, send)`.
