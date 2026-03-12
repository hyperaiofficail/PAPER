## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS via Resource Exhaustion (FastAPI Payload Spooling)
**Vulnerability:** Missing strict payload size limits allowed arbitrarily large file uploads or text payloads, which could lead to Denial of Service (DoS) attacks by exhausting server memory or disk space.
**Learning:** In FastAPI, relying on `seek()` or `tell()` inside the endpoint handler or form data validation is ineffective for large payloads because the framework (via Starlette) has already spooled the incoming payload into memory or a temporary file on disk *before* the handler logic runs.
**Prevention:** Always enforce a maximum payload size limit via ASGI middleware that checks the `Content-Length` header on `POST`, `PUT`, and `PATCH` requests and rejects payloads early (e.g., HTTP 413 Payload Too Large) before framework-level processing.
