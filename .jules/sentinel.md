## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-04-02 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced payload size limits based on the Content-Length header, but didn't mandate its presence. By omitting the header, attackers could bypass the size checks and cause DoS.
**Learning:** Relying on optional headers for security controls can be bypassed if the header is completely omitted.
**Prevention:** When enforcing payload size limits based on headers, explicitly validate and mandate the presence of the header (e.g. returning 411 Length Required).
