## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-24 - DoS and Path Traversal edge-case in File Uploads
**Vulnerability:** The application attempted to sanitize filenames using `os.path.basename` to prevent path traversals. However, `os.path.basename` evaluates `.` or `..` directly as valid basenames, meaning these payloads could be returned unharmed. Additionally, accessing `file.filename` on an `UploadFile` can raise an `AttributeError` if `filename` is `None`, leading to a DoS vulnerability.
**Learning:** `os.path.basename` is insufficient to protect against literal `.` or `..` filenames, and FastAPI `UploadFile.filename` may be `None` or empty.
**Prevention:** Always provide a default string fallback if the filename is `None` or empty, and implement explicit blocklists to catch `.` or `..` as well as whitespace-only names after sanitization.
