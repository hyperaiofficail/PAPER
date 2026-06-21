## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-23 - DoS and Path Traversal in File Upload Filename Handling
**Vulnerability:** The application used `file.filename` directly in `.replace()` calls without checking for `None`, leading to an `AttributeError` DoS if a client uploads a file without a filename. Furthermore, after extracting the basename, it didn't verify if the resulting filename was just `.` or `..` or entirely empty/whitespace, allowing subtle path traversal or bad URLs.
**Learning:** FastAPI's `UploadFile.filename` can be `None`. When performing any string operations like replacement or basename extraction, the input must be safely coerced to a string. Post-extraction, the filename must be stripped and validated against edge cases like empty strings or directory navigation primitives.
**Prevention:** Always coalesce `UploadFile.filename` with `or ""` before any string manipulation. After extracting the basename, strip whitespace and explicitly check if it's `.` or `..` or empty. If so, revert to a safe default like `"unnamed"`.
