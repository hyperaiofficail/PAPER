## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Payload Size Bypass
**Vulnerability:** The application enforced a maximum payload size based on the `Content-Length` header but allowed bypass if the header was omitted entirely. Additionally, an exact string match check allowed bypassing the `Transfer-Encoding: chunked` block using casing differences or multiple header values.
**Learning:** Security controls based on HTTP headers must explicitly mandate the presence of those headers if their absence results in a fail-open condition. String matching for HTTP headers should be robust against canonicalization and common variants (e.g., lowercase substring checks).
**Prevention:** Mandate `Content-Length` for POST/PUT/PATCH requests and use robust case-insensitive partial matching (e.g., `"chunked" in transfer_encoding.lower()`) for detecting disallowed transfer encodings.
