## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-23 - DoS and Path Traversal via Unhandled UploadFile.filename
**Vulnerability:** The application used `file.filename` in `os.path.basename(file.filename.replace("\\", "/"))` without checking if it was `None`. This could cause an unhandled `AttributeError` DoS if a client uploaded a file without a filename. Furthermore, it did not check for entirely empty or purely whitespace filenames after `os.path.basename`, which could bypass intended sanitization.
**Learning:** `UploadFile.filename` from FastAPI can be `None` and should never be used directly in string operations without coalescing to a string. Sanitization must also explicitly handle empty or pure whitespace results.
**Prevention:** Always coalesce `UploadFile.filename` to an empty string (e.g., `file.filename or ""`) before performing string operations. After sanitizing with `os.path.basename`, strip whitespace and explicitly check if the result is empty, `.`, or `..`, falling back to a safe default like `"unnamed"`.
