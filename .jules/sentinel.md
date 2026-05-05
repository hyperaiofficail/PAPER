## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS via Missing Content-Length
**Vulnerability:** The `content_length_limit_middleware` only checked payload size if the `Content-Length` header was present. An attacker could bypass the 10MB limit by simply omitting the header, potentially leading to DoS.
**Learning:** Enforcing security limits based on optional headers is flawed. Always explicitly mandate the presence of required headers.
**Prevention:** Explicitly validate that `Content-Length` exists and return a `411 Length Required` response if it is missing.
