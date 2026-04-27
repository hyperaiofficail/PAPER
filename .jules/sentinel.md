## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-04-27 - DoS Bypass in Payload Size Limit Enforcement
**Vulnerability:** The application enforced a maximum payload size by checking the `Content-Length` header, but did not mandate its presence. It also blocked `Transfer-Encoding: chunked` using an exact, case-sensitive match. This allowed attackers to bypass the size limit by omitting `Content-Length` or using non-standard casings for `Transfer-Encoding`.
**Learning:** Relying on the presence of a header to enforce security limits can lead to bypasses if the header is missing. Furthermore, HTTP headers are case-insensitive and can contain multiple comma-separated values.
**Prevention:** When enforcing payload size limits, explicitly validate and mandate the presence of the header (e.g., returning 411 Length Required if absent). When validating headers like `Transfer-Encoding`, normalize to lowercase and use substring matching.
