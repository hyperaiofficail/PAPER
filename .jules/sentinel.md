## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-24 - DoS and Path Traversal Bypass in File Uploads
**Vulnerability:** The application was vulnerable to an `AttributeError` DoS if a client uploaded a file without a filename, as FastAPI's `UploadFile.filename` can be `None`. Furthermore, if the sanitized filename resulted in an empty string, `.`, or `..` (e.g. `file.filename = "  "`), it could bypass intended path traversal protections and lead to unintended behavior.
**Learning:** Always coalesce external properties that might be `None` (like `file.filename or ""`) before performing string operations, and explicitly validate the result of sanitization functions (like `os.path.basename`) against empty or self-referential dot-segments.
**Prevention:** Use a safe default (like "unnamed") when a sanitized user-controlled filename evaluates to an invalid or dangerous value.
