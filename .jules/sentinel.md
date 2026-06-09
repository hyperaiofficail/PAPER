## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-06-09 - DoS and Path Traversal via Empty or Missing Filename
**Vulnerability:** The application used `file.filename` directly to perform string operations (like `.replace()`) without checking if it was `None` (which FastAPI's `UploadFile` can return if no filename is provided). This could cause an unhandled `AttributeError` leading to Denial of Service. Additionally, relying solely on `os.path.basename` could result in empty filenames or purely relative paths like `.` or `..` being used in download URLs if the user supplied them.
**Learning:** FastAPI's `UploadFile.filename` can be `None`. Always coalesce this value before performing string operations. Furthermore, filename sanitization must explicitly handle cases where the resulting base name is empty or a relative path component to prevent path traversal bypasses or malformed URLs.
**Prevention:** Always use `file.filename or ""` before string operations. Strip whitespace from the sanitized filename and explicitly check if it is empty, `.`, or `..`, falling back to a safe default like `"unnamed"` if necessary.
