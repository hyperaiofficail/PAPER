## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Vulnerability via Missing Content-Length Header
**Vulnerability:** The backend endpoint enforced a file upload size limit (MAX_FILE_SIZE) by reading the `Content-Length` header but did not mandate its presence. An attacker could completely omit the header to bypass the size limitation, leading to potential Denial of Service (DoS) due to resource exhaustion when uploading arbitrarily large payloads.
**Learning:** Relying purely on header values for security limits without verifying that the header actually exists allows for easy bypass. The presence of crucial security-related headers must always be strictly validated.
**Prevention:** Always explicitly validate and mandate the presence of critical headers (e.g., returning `411 Length Required` if absent) before evaluating their values.
