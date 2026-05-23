## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-23 - FastAPI File Upload Edge Cases
**Vulnerability:** While `os.path.basename` prevents path traversal, the `UploadFile.filename` attribute can be `None` or an empty string. Additionally, `.basename` can result in just `.` or `..` or empty strings when manipulating strings in certain ways. Failing to explicitly handle these can cause a DoS (AttributeError) or empty/hidden files on disk. Overly permissive CORS wildcards also exposed endpoints unnecessarily.
**Learning:** File upload sanitization isn't just about stripping slashes; the underlying attribute itself must be checked for `None`, and the resulting string must be explicitly checked against `.` and `..` post-sanitization. CORS should follow least privilege.
**Prevention:** Always provide a fallback for `UploadFile.filename` before applying string operations, strip whitespace, and explicitly check if the result is empty, `.`, or `..`, falling back to a safe default. Explicitly list allowed methods and headers for CORS.
