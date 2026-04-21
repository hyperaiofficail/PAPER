## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.
## 2025-02-23 - DoS Limit Bypass via Missing Header
**Vulnerability:** The backend enforced a 10MB `Content-Length` file size limit but failed to enforce that the `Content-Length` header was actually present. Missing the header bypassed the size check completely, leaving the application vulnerable to DoS attacks via resource exhaustion.
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits based on headers, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent).
