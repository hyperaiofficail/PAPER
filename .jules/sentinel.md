## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - Denial of Service Bypass Missing Header Check
**Vulnerability:** A resource limit check (10MB file max size) relied solely on the `Content-Length` header's value but did not mandate its existence, enabling a DoS attack via large payloads sent without the header.
**Learning:** If a security enforcement mechanism depends on a client-provided header, the server must actively validate that the header is present. If it's missing, the request should be rejected to prevent bypassing the limit.
**Prevention:** Always mandate the presence of required headers (like `Content-Length`) for payload-bearing requests (POST/PUT/PATCH), explicitly returning a 411 Length Required response if it is missing.
