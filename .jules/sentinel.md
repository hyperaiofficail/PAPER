## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-24 - Edge Cases in FastAPI UploadFile.filename
**Vulnerability:** FastAPI's `UploadFile.filename` can be `None` or resolve to empty strings or path traversal sequences like `.` or `..`. Directly using it in string manipulations or paths without defaults can lead to `AttributeError` (causing 500 Server Errors) or unsafe file operations.
**Learning:** Never assume standard web framework objects for uploaded files always contain valid, non-null, or safe strings. Always explicitly handle `None` and empty string edge cases before sanitizing.
**Prevention:** Implement a fallback mechanism (like "unnamed") for null/empty filenames, apply `os.path.basename` to prevent path traversal, and finally verify the result isn't empty, `.`, or `..` before use.
