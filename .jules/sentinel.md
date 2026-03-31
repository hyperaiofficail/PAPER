## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-03-31 - DoS Risk from Missing Content-Length Enforcement
**Vulnerability:** The application enforced a MAX_FILE_SIZE limit by checking the Content-Length header, but bypassed the check if the header was entirely missing on POST/PUT/PATCH requests.
**Learning:** Relying on the presence of a header to enforce security limits can lead to bypasses if the header is omitted. Attackers could send massive payloads without a Content-Length header, leading to resource exhaustion (DoS).
**Prevention:** When enforcing size limits based on headers, always mandate the presence of the header (e.g., returning 411 Length Required) and strictly validate its value.
