## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-23 - Path Traversal Bypass via Empty or Special Filenames
**Vulnerability:** Even when filenames are passed through `os.path.basename`, `UploadFile.filename` could be `None` or special directory representations like `.` or `..`. The `os.path.basename` operation can fail with an `AttributeError` on `None` inputs, and allows `.` or `..` to pass through, potentially leading to directory traversal issues if used directly in path concatenations.
**Learning:** `os.path.basename` is not sufficient to prevent all path traversals. You must ensure the fallback logic applies not only to directory traversal patterns like `../` but also to the special dot (`.`) and dot-dot (`..`) strings. Furthermore, `None` inputs or empty inputs from the client must be caught early to avoid errors.
**Prevention:** Always provide a default empty string for potential `None` filenames. After running `os.path.basename` and stripping whitespace, explicitly check if the filename is `.` or `..` or empty, and provide a safe fallback like `"unnamed"` if so.
