## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS via Missing Content-Length Header Bypass
**Vulnerability:** The application enforced maximum file sizes using the `Content-Length` header but did not mandate the header's presence, allowing an attacker to bypass the size check simply by omitting the header or attempting to stream data.
**Learning:** Checking the value of a header is insufficient if the header itself is optional; attackers can bypass validation logic if there is a path where validation is skipped entirely.
**Prevention:** Always mandate the presence of critical security control headers (e.g., returning 411 Length Required) before proceeding with payload processing.
