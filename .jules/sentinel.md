## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-23 - DoS and Path Traversal via Edge-case Filenames
**Vulnerability:** In file upload handling, FastAPI's `UploadFile.filename` can be `None`, leading to an `AttributeError` DoS when string operations are applied. Furthermore, even when using `os.path.basename` to sanitize filenames, passing exact strings like `.` or `..` results in those same exact values bypassing the sanitization and causing potential path traversals.
**Learning:** `os.path.basename` is insufficient to protect against exact `.` or `..` filenames. In addition, unvalidated attributes on uploaded files can lead to DoS if they default to `None`.
**Prevention:** Always coalesce potentially `None` filename inputs to empty strings before processing (e.g., `file.filename or ""`). Additionally, explicitly verify the sanitized filename is not empty, `.`, or `..`, and revert to a safe default if it is.
