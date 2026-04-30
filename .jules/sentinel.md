## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS via Missing Headers and Encoding Bypasses
**Vulnerability:** The size limits for payloads in file uploads were vulnerable to bypass. First, the size check could be bypassed completely by simply omitting the `Content-Length` header. Second, the filter for `Transfer-Encoding: chunked` was strict and case-sensitive, allowing bypass via mixed case (e.g., `Chunked`) or comma-separated lists (e.g., `gzip, chunked`). This could lead to a Denial of Service via resource exhaustion.
**Learning:** Checking for the presence of a header and its value is not enough when the absence of the header allows a bypass. Likewise, HTTP headers are case-insensitive and can hold multiple values, meaning exact string matches are unsafe.
**Prevention:** Mandate the presence of critical security headers explicitly (e.g., return a 411 Length Required if `Content-Length` is missing) and use case-insensitive substring matching (`"chunked" in header.lower()`) to robustly filter unwanted encodings.
