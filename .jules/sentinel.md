## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-04-11 - DoS Vulnerability via Missing Content-Length Header
**Vulnerability:** Security checks that rely on optional headers (like enforcing a file upload size limit via `Content-Length`) can be bypassed if the header is entirely omitted, rendering the security check ineffective and leading to potential Denial of Service (DoS).
**Learning:** Checking if a header exists before enforcing a limit is an anti-pattern. If a payload size limit is enforced, the size metadata must be explicitly mandated for validation.
**Prevention:** Always mandate the presence of the required header (e.g., return a 411 Length Required response) before proceeding to validate its value.
