## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-23 - DoS and Path Traversal edge cases in file uploads
**Vulnerability:** The file upload logic utilized `file.filename` directly for sanitization via `os.path.basename`. However, FastAPI `UploadFile.filename` can be `None` or an empty string, leading to an `AttributeError` (DoS) if string methods like `.replace()` are called. Furthermore, empty or whitespace-only filenames, or filenames resolving to `.` or `..` after `basename`, could lead to subtle path traversal or file system anomalies.
**Learning:** Never assume `UploadFile.filename` is a valid string. Always provide a default fallback (e.g., `'unnamed'`) before performing string operations. Additionally, `os.path.basename` alone is insufficient if the resulting basename is `.` or `..` or empty.
**Prevention:** Handle `None` and empty strings explicitly: `raw_filename = file.filename or "unnamed"`. Sanitize with `os.path.basename`, strip whitespace, and verify the resulting filename is not empty, `.`, or `..`, falling back to a safe default if necessary.
