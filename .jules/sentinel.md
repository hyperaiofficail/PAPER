## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-24 - DoS and Path Traversal via UploadFile.filename
**Vulnerability:** The application was not safely handling edge cases for `UploadFile.filename` during file uploads. Because `file.filename` can be `None` (if the client doesn't provide it), applying string operations like `.replace()` resulted in `AttributeError` DoS crashes. Furthermore, `os.path.basename` could evaluate to an empty string, `.`, or `..`, leading to subtle path traversal or bad state vulnerabilities when resolving file paths.
**Learning:** `UploadFile.filename` must not be trusted. Not only can it be a malicious path, but it can also be legitimately `None` or evaluate to edge case components when sanitized by functions like `os.path.basename`.
**Prevention:** Always coalesce potentially `None` string values (e.g., `file.filename or ""`) before string operations. After stripping whitespace and using `os.path.basename`, explicitly check that the resulting filename is truthy and not equal to '.' or '..', and provide a safe fallback like "unnamed".
