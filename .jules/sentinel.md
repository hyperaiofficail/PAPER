## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - Unrestricted File Upload Size
**Vulnerability:** The application accepted unlimited file uploads, allowing attackers to exhaust server disk space or memory (DoS).
**Learning:** FastAPI `UploadFile` handles uploads without size limits by default. Explicit size validation is required to prevent resource exhaustion.
**Prevention:** Check file size using `seek(0, 2)` and `tell()` before processing.
