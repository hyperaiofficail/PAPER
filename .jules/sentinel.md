## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-23 - DoS and Path Traversal via Unhandled UploadFile.filename
**Vulnerability:** The application used `file.filename.replace()` directly on `UploadFile` objects. If a client provided a file without a filename, `file.filename` would be `None`, causing an unhandled `AttributeError` DoS crash. Furthermore, if the sanitized filename was empty or navigated to the root directory, it could still result in unexpected paths.
**Learning:** FastAPI's `UploadFile.filename` can legitimately be `None` and must be coalesced before string operations. Also, standard sanitization (like `os.path.basename` and `.strip()`) can sometimes result in empty or special strings (like `.` or `..`) which must be explicitly handled.
**Prevention:** Always coalesce `UploadFile.filename` (e.g. `file.filename or ""`) to avoid `AttributeError` DoS. Always verify that the final sanitized filename is not empty and is not restricted paths like `.` or `..`, falling back to a safe default like `"unnamed"` if necessary.
