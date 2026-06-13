## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-24 - DoS via Unhandled UploadFile.filename
**Vulnerability:** When a client uploaded a file without providing a filename (e.g. `filename=None`), `os.path.basename` and `.replace()` calls crashed with `AttributeError`, causing a 500 error and potential DoS. Additionally, whitespace, empty, `.`, or `..` filenames could bypass basic traversal checks.
**Learning:** `UploadFile.filename` from FastAPI (and many other web frameworks) can be null or malformed. Do not trust it directly. Furthermore, after stripping and basic sanitization, explicitly enforce a safe fallback.
**Prevention:** Coalesce null filenames (e.g. `raw = file.filename or ""`), explicitly strip whitespace, and always enforce a safe fallback filename (like "unnamed") if the result is empty or evaluates strictly to directory markers like `.` or `..`.
