## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-04-07 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a file size limit by checking the Content-Length header, but failed to mandate the presence of the header itself. An attacker could bypass the DoS limit by completely omitting the header.
**Learning:** Relying on the presence of a header to enforce security limits can lead to bypasses if the header is omitted entirely.
**Prevention:** When enforcing payload size limits, explicitly validate and mandate the presence of the required header (e.g., returning 411 Length Required if absent).
