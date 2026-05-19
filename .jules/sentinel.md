## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2024-05-19 - Unhandled None and Relative Paths in Filename Sanitization
**Vulnerability:** The application attempted to sanitize filenames using `os.path.basename` and string replacements, but it did not account for cases where `UploadFile.filename` is `None` (which would cause an `AttributeError`) or where the sanitized filename resolves to relative directories like `.` or `..`, or an empty string. This could lead to crashes or bypasses in subsequent file operations.
**Learning:** Robust filename sanitization requires more than just extracting the base name. It must handle cases where the input is missing (`None`) and ensure the output is a valid, non-relative filename after sanitization.
**Prevention:** Always provide a safe fallback (e.g., 'unnamed') if `file.filename` is `None`. After applying `os.path.basename`, explicitly strip whitespace and check if the resulting filename is empty, `.`, or `..`, falling back to a safe default if necessary.
