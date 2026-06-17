## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-23 - Denial of Service via Unhandled None in UploadFile
**Vulnerability:** The application was vulnerable to an AttributeError crash (resulting in a 500 Internal Server Error) when processing file uploads without a provided filename because `file.filename` evaluated to `None`, which does not support the `.replace()` string method.
**Learning:** FastAPI's `UploadFile.filename` can be `None` if the client does not specify a filename in the multipart/form-data payload. Failing to handle this can lead to a Denial of Service.
**Prevention:** Always safely coalesce potentially `None` variables (like `file.filename or ""`) before invoking string methods on them. Additionally, perform robust sanitization by explicitly rejecting empty strings, whitespace, '.', and '..'.
