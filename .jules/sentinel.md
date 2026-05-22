## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-23 - Missing Filename Validation Causing Errors and Weak Sanitization
**Vulnerability:** The application assumed `UploadFile.filename` was always a non-empty string, failing to handle cases where the filename was `None` (resulting in `AttributeError`), empty, or purely whitespace. In addition, the application did not block or normalize dangerous filenames consisting of just `.` or `..` after base extraction.
**Learning:** FastAPI's `UploadFile.filename` can be `None` or an empty string, and robust sanitization requires checking for these cases explicitly after stripping whitespace.
**Prevention:** Before sanitizing file upload names, ensure `None` is mapped to an empty string fallback. Afterwards, sanitize by getting the base name and stripping whitespace. Finally, ensure the file is not empty, `.`, or `..`, explicitly giving it a safe fallback name such as `'unnamed'`.
