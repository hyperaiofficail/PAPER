## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS bypass via missing Content-Length
**Vulnerability:** The backend enforced a maximum payload size limit (MAX_FILE_SIZE) by reading the `Content-Length` header, but if an attacker entirely omitted the header in a POST/PUT/PATCH request, the limit check was bypassed.
**Learning:** Relying on the presence of a header to enforce security limits is insufficient, as headers are user-controlled and can be absent.
**Prevention:** Always explicitly validate and mandate the presence of required headers for security enforcement (e.g., returning a 411 Length Required response if absent).
