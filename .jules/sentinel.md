## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2023-10-24 - Content-Length Bypass DoS Risk
**Vulnerability:** File upload payload size limits were only enforced if the client provided a `Content-Length` header. Omitting the header bypassed the 10MB limit check entirely, allowing unconstrained resource consumption.
**Learning:** Security validations tied to optional headers can be bypassed by malicious actors omitting the header entirely.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header, responding with HTTP 411 Length Required if absent.
