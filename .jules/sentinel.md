## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-24 - Edge Cases in Path Traversal Fix
**Vulnerability:** Even when using `os.path.basename` to prevent path traversal in file uploads, the filename logic could fail or be bypassed if `file.filename` is `None`, empty, or consists only of whitespace (resulting in empty strings or just `.`/`..` after stripping).
**Learning:** `os.path.basename` is insufficient on its own for robust security. You must account for null/empty values and special directories like `.` and `..` that can evade simple sanitation if they are the only characters left after processing.
**Prevention:** Always check if `file.filename` is `None` before string operations, explicitly strip whitespace, and verify the resulting string is not empty, `.`, or `..`. Default to a safe placeholder like "unnamed" if any of these conditions are met.
