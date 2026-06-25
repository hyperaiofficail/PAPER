## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-24 - DoS and Path Traversal via None/Empty Upload Filename
**Vulnerability:** The application assumed `UploadFile.filename` was always a string when attempting to sanitize it against path traversal, but FastAPI sets it to `None` if the client omits the filename. Calling `.replace()` on `None` causes an `AttributeError`, resulting in a Denial of Service (DoS) for the file processing endpoint. Additionally, resolving `.` or `..` could result in empty strings after basename operations, bypassing sanitization if empty checks weren't explicit.
**Learning:** File metadata from HTTP requests should never be implicitly trusted to be non-null or well-formed. A robust sanitization process must handle `None` types explicitly, and default to a safe value when potentially dangerous traversal outcomes result in empty strings.
**Prevention:** Always coalesce `UploadFile.filename` (e.g., `file.filename or ""`) before processing. After replacing path separators and extracting the basename, strip whitespace and explicitly check if the resulting filename is empty, `.`, or `..`, falling back to a safe default like "unnamed" to prevent DoS crashes and traversal edge-cases.
