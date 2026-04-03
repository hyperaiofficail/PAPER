## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS via Content-Length Header Bypass
**Vulnerability:** A file payload size limit was enforced only if the `Content-Length` header was present. If a client omitted the header, the size limit check was bypassed.
**Learning:** Relying on the presence of an optional or omittable header to enforce a security limit fails if the attacker intentionally omits the header.
**Prevention:** When enforcing payload limits based on headers like `Content-Length`, always explicitly validate and mandate their presence (e.g., returning 411 Length Required if absent) rather than conditionally checking only if they exist.
