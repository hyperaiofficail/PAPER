## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-22 - Missing Content-Length header bypasses size limit
**Vulnerability:** The application enforced payload size limits by checking the `Content-Length` header, but bypassed the size check if the header was omitted entirely, leaving the server vulnerable to Denial of Service (DoS) attacks via resource exhaustion.
**Learning:** Relying purely on the presence of an optional HTTP header to enforce security constraints is flawed. If a constraint depends on a header value, the header itself must be mandatory.
**Prevention:** When enforcing payload size limits, explicitly validate and mandate the presence of the `Content-Length` header for all requests where body payload size matters (e.g., POST, PUT, PATCH). Return a 411 Length Required response if absent.
