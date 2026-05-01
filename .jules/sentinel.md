## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-22 - DoS Bypass in Payload Size Limits
**Vulnerability:** The application enforced maximum file size limits by checking the `Content-Length` header, but allowed requests to proceed if the header was completely omitted, leaving the server vulnerable to resource exhaustion (DoS) via unbounded payloads.
**Learning:** Relying on the presence of a header to enforce security limits can lead to fail-open bypasses if the header is missing. Security enforcement must explicitly validate the presence of the required data.
**Prevention:** Always mandate the presence of required headers (like `Content-Length` for payloads) by returning a 411 Length Required response if absent, before enforcing the size constraints.
