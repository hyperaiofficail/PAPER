## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-04-17 - DoS Bypass via Missing Content-Length
**Vulnerability:** The `content_length_limit_middleware` relied on the presence of the `Content-Length` header to validate payload size. If the header was omitted, the check was completely bypassed, allowing potential Denial of Service via excessively large payloads.
**Learning:** Relying on optional client-provided metadata to enforce security restrictions is flawed. If a constraint depends on metadata, the presence of that metadata must be mandated.
**Prevention:** Always explicitly validate and mandate the presence of required headers (like `Content-Length` for state-changing methods) before attempting to evaluate their contents.
