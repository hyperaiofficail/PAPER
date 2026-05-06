## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass in Payload Limit Middleware
**Vulnerability:** The `content_length_limit_middleware` only enforced payload size limits if the `Content-Length` header was present. Omission of the header bypassed size limits. Additionally, the `Transfer-Encoding: chunked` check was strictly case-sensitive exact match, allowing bypasses using mixed case or multiple values (e.g. `Transfer-Encoding: gzip, chunked`).
**Learning:** Security middleware cannot passively rely on the existence or exact casing of HTTP headers. Attackers will actively manipulate or omit headers to evade detection.
**Prevention:** When enforcing size limits on POST/PUT/PATCH, explicitly mandate the `Content-Length` header (returning 411 if absent). Validate HTTP header contents using robust logic such as lowercase normalization and substring matching.
