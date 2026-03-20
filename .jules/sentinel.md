## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2024-05-24 - DoS Bypass via Transfer-Encoding Variations
**Vulnerability:** The application was vulnerable to Denial of Service (DoS) attacks because the file size limit check could be bypassed by sending a composite `Transfer-Encoding` header (e.g., `Transfer-Encoding: gzip, chunked`). The application previously checked for exact string match (`== "chunked"`).
**Learning:** Exact string matching is insufficient for HTTP headers like `Transfer-Encoding` which allow multiple encodings separated by commas.
**Prevention:** Always use case-insensitive substring matching (e.g., `"chunked" in te.lower()`) when verifying if an encoding is present in an HTTP header that supports lists.
