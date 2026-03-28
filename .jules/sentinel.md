## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS via Transfer-Encoding Bypass
**Vulnerability:** Exact match check for `Transfer-Encoding == "chunked"` allowed attackers to bypass the 10MB `Content-Length` limit using variations like `"Chunked"` or `"gzip, chunked"`, risking server resource exhaustion (DoS).
**Learning:** Security controls based on HTTP headers must account for case-insensitivity and comma-separated multiple values according to HTTP standards.
**Prevention:** Use case-insensitive substring checks (e.g., `"chunked" in header.lower()`) or proper header parsing libraries when validating security-sensitive headers like `Transfer-Encoding`.
