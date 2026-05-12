## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS via Missing Content-Length Check Bypass
**Vulnerability:** The `content_length_limit_middleware` enforced maximum payload limits and blocked chunked requests, but only conditionally checked these if the `Content-Length` or `Transfer-Encoding` headers were present. An attacker could completely omit `Content-Length` to bypass the `MAX_FILE_SIZE` limit and cause DoS via resource exhaustion. Also, case-sensitive checking allowed bypassing chunked restrictions.
**Learning:** Security limits relying on specific headers must explicitly mandate the presence of those headers. Furthermore, header values must be normalized (e.g., lowercased) and checked robustly (e.g., substring matching) rather than using strict equality.
**Prevention:** Mandate critical security headers (like `Content-Length` for POST/PUT) and reject requests with a `411 Length Required` if absent. Always use case-insensitive substring checks when validating HTTP header semantics.
