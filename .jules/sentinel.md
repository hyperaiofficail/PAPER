## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-03-26 - DoS Bypass via Transfer-Encoding Variations
**Vulnerability:** A DoS protection mechanism enforcing `Content-Length` could be bypassed because `Transfer-Encoding: chunked` was validated with a strict exact match (`"chunked"`). An attacker could bypass it by sending headers like `Transfer-Encoding: Chunked` (case) or `Transfer-Encoding: gzip, chunked` (composite values).
**Learning:** HTTP headers that accept comma-separated lists of values and are case-insensitive by spec can lead to trivial bypasses when validated using exact string matching.
**Prevention:** When validating HTTP headers against specific directives, always convert the header value to lowercase and use a substring check (e.g., `"chunked" in header.lower()`) rather than exact equality.
