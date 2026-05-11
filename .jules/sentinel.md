## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2024-05-11 - Content-Length Header Omission Bypass
**Vulnerability:** The application enforced maximum file size limits by checking the `Content-Length` header, but completely allowed the request if the header was omitted, leading to a bypass of the security limit and potential DoS via resource exhaustion.
**Learning:** Security limits relying on optional request metadata (like headers) must explicitly mandate the presence of that metadata or use a secure fallback. Failing to validate the presence of the header nullifies the security check.
**Prevention:** When enforcing size limits based on `Content-Length`, explicitly check if the header exists and return a 411 Length Required if it is missing for methods that expect a body (POST, PUT, PATCH).
