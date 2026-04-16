## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2025-02-23 - DoS Bypass in Payload Limit
**Vulnerability:** The application enforced maximum payload sizes by checking the `Content-Length` header. However, if the header was completely omitted, the check was skipped, allowing an attacker to send arbitrarily large payloads and cause a Denial of Service (DoS) due to resource exhaustion.
**Learning:** Security checks that rely on the presence of a specific header can be bypassed if the application defaults to "allow" when the header is missing.
**Prevention:** When enforcing size limits or other security properties that rely on metadata (like headers), always enforce the presence of that metadata explicitly (e.g., return a 411 Length Required response if absent).
