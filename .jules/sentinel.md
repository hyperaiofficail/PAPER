## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-23 - DoS via Missing Filename in Uploads
**Vulnerability:** A missing or `None` filename in `UploadFile` (e.g. `file.filename`) would cause the server to crash when it attempted to call string operations (like `.replace()`) on it, leading to a Denial of Service (DoS) during file upload processing.
**Learning:** Security mitigations (like path traversal sanitization using `os.path.basename`) can inadvertently introduce crash vulnerabilities (DoS) if attributes like `filename` are blindly assumed to be strings.
**Prevention:** Always default potentially missing file properties to safe strings (e.g., `file.filename or ""`) and perform explicit validation against edge cases (like whitespace only, `.` or `..`) before allowing them to be used in operations or paths.
