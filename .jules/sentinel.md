## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS via Content-Length Bypass
**Vulnerability:** The size enforcement middleware relied on the presence of the `Content-Length` header but did not mandate it, allowing large payloads to bypass size limits if the header was omitted entirely.
**Learning:** Security limits (like payload sizes) must enforce explicit prerequisites (e.g., mandating `Content-Length` presence) and validate HTTP headers case-insensitively and thoroughly (e.g., checking substrings for `chunked` encodings) to prevent bypasses.
**Prevention:** Always mandate header presence when relying on it for security checks and use robust, case-insensitive substring matching for HTTP header values.
