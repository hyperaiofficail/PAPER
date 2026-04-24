## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-22 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size based on the `Content-Length` header but did not validate its presence. An attacker could completely omit the header on `POST`/`PUT`/`PATCH` requests to bypass the size limit check, potentially causing a Denial of Service (DoS) through resource exhaustion.
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent).
