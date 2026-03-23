## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-03-23 - Transfer-Encoding Bypass Vulnerability
**Vulnerability:** The 10MB `Content-Length` limit check could be bypassed using `Transfer-Encoding: chunked` due to an exact string match, posing a DoS risk.
**Learning:** Middleware checking headers must be robust against varied casing and edge cases (e.g. `chunked` within a broader string like `gzip, chunked`).
**Prevention:** Ensure header checks utilize lowercased substring matching (e.g., `'chunked' in te.lower()`) rather than exact matches.
