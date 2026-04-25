## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2025-02-23 - DoS via Missing Content-Length Header
**Vulnerability:** The backend enforced a payload size limit (`MAX_FILE_SIZE`) by checking the `Content-Length` header, but allowed requests that entirely omitted this header to bypass the size check, potentially leading to Denial of Service (DoS) due to unconstrained payload parsing.
**Learning:** Relying on an optional header to enforce security constraints is fundamentally flawed if the absence of the header defaults to an open state. Security checks based on headers must strictly mandate the presence of those headers.
**Prevention:** When enforcing size limits based on `Content-Length`, explicitly validate that the header exists (e.g., by returning a 411 Length Required) before evaluating its value.
