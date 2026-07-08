## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-24 - DoS and Path Traversal in File Upload
**Vulnerability:** FastAPI's `UploadFile.filename` can be `None`. Accessing string methods like `.replace()` directly on it causes an `AttributeError` resulting in a Denial of Service. In addition, an empty or whitespace-only filename, or a directory traversal bypass like '.' or '..' could be mishandled.
**Learning:** Always treat user-provided filenames as untrusted and potentially missing.
**Prevention:** Coalesce the filename value (`file.filename or ""`), strip it of whitespace, check for dangerous values like '.' and '..', and explicitly fall back to a safe default like "unnamed".
