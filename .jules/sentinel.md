## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2024-06-24 - Unhandled DoS via FastAPI `UploadFile.filename`
**Vulnerability:** When handling file uploads, FastAPI's `UploadFile.filename` can be `None` if the client omits the filename parameter. Attempting string operations (like `.replace()`) on `None` causes an `AttributeError` (500 crash), potentially leading to Denial of Service.
**Learning:** Security logic must handle missing or null input parameters robustly, especially attributes that are conventionally expected to be strings but aren't strictly enforced by the framework.
**Prevention:** Always coalesce potentially null string values (e.g., `file.filename or ""`) before processing. Add explicit checks for edge case inputs like `.` and `..` when dealing with file paths.
