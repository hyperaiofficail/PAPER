## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS via Missing Content-Length Header
**Vulnerability:** The application relied on the `Content-Length` header to enforce a 10MB payload size limit. However, if the header was omitted entirely, the check was bypassed, allowing arbitrarily large payloads and creating a Denial of Service (DoS) risk.
**Learning:** Security controls should never default to an allow-state when required metadata (like `Content-Length`) is missing. Relying on optional headers for enforcement is dangerous.
**Prevention:** Explicitly validate and mandate the presence of the `Content-Length` header for all requests where a payload is expected (POST, PUT, PATCH). Return a 411 Length Required response if the header is absent.
