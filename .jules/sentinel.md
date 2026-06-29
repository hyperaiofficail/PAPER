## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-24 - Unhandled DoS and Path Traversal Bypass via file.filename
**Vulnerability:** FastAPI's `UploadFile.filename` can be `None` if the client doesn't provide a filename. Directly calling string operations like `.replace()` on it causes an unhandled `AttributeError`, resulting in an Internal Server Error (DoS). Additionally, users uploading files named with only spaces or traversal strings (like `../../ \t`) could bypass `os.path.basename` resulting in empty strings or strings containing whitespace in URLs.
**Learning:** Never assume attributes provided by the client (like `filename`) are strings. Input could be `None` or completely empty after sanitization.
**Prevention:** Always coalesce potentially `None` strings (e.g. `file.filename or ""`) before processing. Strip sanitized filenames and fallback to a safe default like `"unnamed"` if they become empty or evaluate to `.` or `..`.
