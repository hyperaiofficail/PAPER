## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-23 - DoS via Unhandled None in File Uploads
**Vulnerability:** The application used `file.filename.replace(...)` directly without checking if `file.filename` was `None`. Since FastAPI's `UploadFile.filename` can be `None` when a client does not provide a filename, this could lead to an unhandled `AttributeError`, causing a Denial of Service (DoS) for the endpoint. Furthermore, the path traversal mitigation was incomplete as it allowed strings like `.` or `..` directly.
**Learning:** Never assume optional request attributes (like filenames from multipart forms) are strings. They can be empty or `None`. Always coalesce and validate before using string operations.
**Prevention:** Always check if `filename` is `None` (e.g., `raw_filename = file.filename or ""`), explicitly strip whitespace, and handle edge cases where the sanitized output becomes empty or restricted values like `.` and `..` by providing a safe fallback like `"unnamed"`.
