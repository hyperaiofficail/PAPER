## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Mitigation via Content-Length Limit
**Vulnerability:** Attackers could upload massive payloads to bypass handler-level size validations, potentially exhausting server disk space or memory because FastAPI spools files before executing route handlers.
**Learning:** Enforcing file size checks *inside* endpoints via `seek`/`tell` is ineffective for preventing payload-driven DoS attacks because the framework has already processed and spooled the large payload.
**Prevention:** Reject excessively large requests before framework processing by using an ASGI middleware that checks the incoming `Content-Length` header against a strict limit (e.g., `MAX_FILE_SIZE`).
