## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2024-04-14 - Mandating Validation Headers
**Vulnerability:** Relying solely on the presence of a header (like `Content-Length`) to enforce security limits (e.g., maximum payload size to prevent DoS) allows bypass if the header is completely omitted.
**Learning:** Security validations tied to headers must also mandate the presence of those headers.
**Prevention:** Always explicitly validate and mandate the presence of required security headers (e.g., returning a `411 Length Required` response if `Content-Length` is absent).
