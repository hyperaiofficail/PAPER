## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS via Missing Content-Length Header
**Vulnerability:** The payload size limit middleware only checked the `Content-Length` header if it was present, allowing attackers to bypass the check and potentially cause Denial of Service (DoS) by sending large payloads without the header.
**Learning:** Relying on the presence of a header to enforce a security limit can lead to bypasses if the header is completely omitted. Security enforcement mechanisms must handle cases where expected data is missing.
**Prevention:** When enforcing payload size limits, explicitly validate and mandate the presence of the `Content-Length` header (e.g., returning a 411 Length Required response if absent).
