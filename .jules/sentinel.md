## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2024-04-13 - Missing Content-Length DoS Bypass
**Vulnerability:** The application enforced maximum file size limits by checking the `Content-Length` header, but allowed requests to proceed if the header was completely omitted, exposing the server to DoS attacks via resource exhaustion from oversized payloads.
**Learning:** Relying on the presence of a header to enforce security limits is flawed if the absence of that header is not handled. Attackers can simply omit the header to bypass the check.
**Prevention:** When enforcing payload size limits, explicitly mandate the presence of the size indicator (e.g., returning a 411 Length Required response if `Content-Length` is missing for request methods that expect a body like POST/PUT/PATCH).
