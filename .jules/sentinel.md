## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-06-26 - Unhandled Optional UploadFile.filename DoS and Path Traversal Bypass
**Vulnerability:** FastAPI's `UploadFile.filename` can be `None` if the client omits the filename. Calling string operations like `.replace()` on it directly caused an `AttributeError`, leading to a Denial of Service. Additionally, relying solely on `os.path.basename` without verifying the result could leave empty strings or `.`/`..` which are invalid/unsafe filenames.
**Learning:** Framework objects representing user input can sometimes be `None` or result in edge-case values (like empty strings) after sanitization. Always account for `None` values and validate the output of sanitization functions.
**Prevention:** Always coalesce potentially `None` string inputs (e.g., `file.filename or ""`) before applying string operations. Furthermore, after applying functions like `os.path.basename`, explicitly check that the resulting filename is non-empty and not a path traversal artifact like `.` or `..`, falling back to a safe default if necessary.
