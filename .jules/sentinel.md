## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.
## 2024-03-18 - Chunked Transfer-Encoding Bypass
**Vulnerability:** The backend middleware checked for `request.headers.get("Transfer-Encoding") == "chunked"` using an exact case-sensitive match. This could allow attackers to bypass the 10MB payload size limit by using case variations (e.g., `CHUNKED`) or adding whitespace.
**Learning:** Security checks on HTTP headers must always be case-insensitive and ideally check for substring inclusion when dealing with values that might have extra whitespace or comma-separated lists.
**Prevention:** Use `.lower()` and the `in` operator (e.g., `"chunked" in te.lower()`) when verifying header values to prevent trivial bypasses.
