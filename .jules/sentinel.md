## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-23 - Edge Cases in Filename Sanitization
**Vulnerability:** Filename sanitization lacked robustness; it did not handle `None` values (which FastAPI's `UploadFile.filename` can be), nor did it explicitly strip whitespace or reject edge cases like `.` or `..` after standard sanitization. This could lead to 500 errors or logic bypassing.
**Learning:** `os.path.basename` combined with string replacement is not always sufficient; inputs might be empty, `None`, or resolve to special directory markers after stripping.
**Prevention:** Always provide a fallback (e.g., `'unnamed'`) for `None` or empty strings, explicitly strip whitespace, and verify that the resulting string is not a directory marker like `.` or `..` before use.
