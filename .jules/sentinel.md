## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-28 - Unrestricted File Upload Size DoS
**Vulnerability:** The FastAPI application processed file uploads without checking `Content-Length` or enforcing a maximum file size limits. A malicious user could exhaust server memory and disk space by uploading gigabytes of data.
**Learning:** Default configurations in FastAPI do not impose a limit on payload sizes. Any public-facing upload endpoint must be explicitly protected with middleware checking the size of incoming requests.
**Prevention:** Implement an HTTP middleware verifying the `content-length` header on `POST` requests, returning HTTP `413 Payload Too Large` for requests exceeding safe thresholds (e.g., 10MB) before payload bodies are processed.
