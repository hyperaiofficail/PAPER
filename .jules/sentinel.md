## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS via Missing Content-Length in Payload Limit
**Vulnerability:** The application enforced maximum file size limits by checking the `Content-Length` header, but allowed requests through without verifying the header was present. This allowed attackers to bypass the check entirely by omitting the header or disguising `Transfer-Encoding: chunked`, leading to potential Denial of Service (DoS) via resource exhaustion.
**Learning:** Relying on the *presence* of an HTTP header to enforce security constraints without mandating its existence creates an easy bypass mechanism. Attackers control headers.
**Prevention:** When enforcing size constraints using HTTP headers like `Content-Length`, always explicitly mandate its presence (e.g., returning a 411 Length Required) and robustly reject workarounds like chunked encoding using case-insensitive substring checks.
