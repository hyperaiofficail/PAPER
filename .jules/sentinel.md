## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-24 - DoS and Path Traversal via UploadFile.filename
**Vulnerability:** The application used `file.filename` directly in an `os.path.basename` call without verifying if the attribute was `None` or an empty string, which could result in an `AttributeError` or allow arbitrary default names leading to issues. Additionally, if path traversal attacks leave the sanitized string as `.` or `..`, it could lead to directory manipulation.
**Learning:** `UploadFile.filename` from FastAPI can be `None` or empty. Path sanitization using `os.path.basename` alone isn't sufficient if the resulting string evaluates to directory references like `.` or `..`.
**Prevention:** Always verify if `file.filename` is valid before processing. Set a secure fallback (e.g., `'unnamed'`), strip whitespace, and explicitly check if the sanitized filename is `.`, `..`, or empty to prevent directory manipulation and DoS errors.
