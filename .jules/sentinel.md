## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-23 - DoS and Path Traversal via Unhandled UploadFile.filename
**Vulnerability:** The application accessed `UploadFile.filename` directly to parse filenames and sanitize them using `os.path.basename`. However, `UploadFile.filename` can be `None` if no filename is provided, leading to an unhandled `AttributeError` crashing the app (DoS). Furthermore, passing empty strings or strings that evaluate to `.` or `..` to `os.path.basename` could result in potential traversal or unexpected filesystem behavior.
**Learning:** `UploadFile.filename` can be `None`. Furthermore, sanitization logic must actively handle edge cases (like `.` or whitespace) instead of assuming valid structure.
**Prevention:** Always coalesce `UploadFile.filename` to a string (e.g. `file.filename or ""`) before processing, and add explicit fallback defaults (like "unnamed") when sanitized filenames are empty, `.`, or `..`.
