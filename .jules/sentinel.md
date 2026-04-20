## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2025-02-23 - Content-Length Bypass in Payload Size Limits
**Vulnerability:** The backend file upload size limit (10MB) relied solely on checking the `Content-Length` header if it was present. A client could omit the header entirely and bypass the size limit, leading to potential Denial of Service (DoS) via resource exhaustion.
**Learning:** Relying on the presence of a header to enforce a security limit fails if an attacker simply removes the header. Defense controls must actively mandate required data.
**Prevention:** When enforcing payload size limits based on headers, always explicitly validate and mandate the presence of the `Content-Length` header (e.g., returning a 411 Length Required response if absent).
