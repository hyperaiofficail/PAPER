## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-24 - Unhandled AttributeError DoS and Path Traversal on UploadFile.filename
**Vulnerability:** FastAPI's `UploadFile.filename` can be `None` when no filename is provided by the client. Directly invoking string methods like `.replace()` or using `os.path.basename` on `None` results in an `AttributeError` crashing the endpoint (DoS). Furthermore, path traversal attacks that result in an empty filename or `.` / `..` after sanitization can be used in downstream logic.
**Learning:** You cannot assume that input attributes from multipart requests are always populated strings. Even framework-provided objects like `UploadFile` will often default to `None` when properties are missing from the request.
**Prevention:** Always check if string inputs and object attributes are `None` (e.g., `file.filename or ""`) before running string operations. Explicitly handle empty paths and traversal aliases (`.`, `..`) that may occur after typical standard sanitization functions run.
