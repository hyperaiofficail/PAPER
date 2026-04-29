## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS via Missing Content-Length Header
**Vulnerability:** The ASGI middleware enforcing maximum payload sizes relied on the presence of the `Content-Length` header. If an attacker omitted the header entirely, the validation was bypassed, potentially allowing arbitrarily large payloads to exhaust server memory (DoS). Furthermore, exact-case matching on `Transfer-Encoding: chunked` allowed bypasses via alternate casing or multiple values.
**Learning:** Security validations that rely on headers must mandate the presence of those headers if their absence implies undefined or unbounded behavior.
**Prevention:** Always explicitly check for and mandate required security headers (e.g., returning 411 Length Required if `Content-Length` is missing on state-changing requests), and use robust, case-insensitive substring checks for headers that can contain multiple values or varying casing.
