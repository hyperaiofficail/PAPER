## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.
## 2026-02-22 - DoS bypass via missing Content-Length header
**Vulnerability:** A DoS protection middleware intended to enforce a maximum payload size of 10MB only checked the size if the `Content-Length` header was provided. If an attacker omitted the header entirely, the validation was bypassed, potentially exposing the server to resource exhaustion via large payloads.
**Learning:** Security logic relying on client-provided headers must explicitly handle the absence of those headers. Bypassing validation simply because a header is missing undermines the security control entirely.
**Prevention:** Always mandate the presence of required headers when enforcing security constraints. If `Content-Length` is needed for payload size limits, return a `411 Length Required` response when it's missing on mutation methods (POST, PUT, PATCH).
