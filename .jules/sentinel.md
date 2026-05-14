## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-22 - DoS Vulnerability via Payload Size Limit Bypass
**Vulnerability:** The `Content-Length` enforcement middleware allowed requests to bypass size limits entirely by omitting the `Content-Length` header, or by using case variations and multiple values in the `Transfer-Encoding: chunked` header.
**Learning:** Relying on the presence of an optional header to enforce critical security limits (like payload size) can lead to bypasses if the header is omitted or manipulated. Always validate explicitly.
**Prevention:** Always mandate the presence of critical security headers (e.g., returning 411 Length Required for missing `Content-Length`) and use case-insensitive, substring-based checks when looking for disallowed encodings like "chunked".
