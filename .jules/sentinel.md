## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2025-02-23 - Content-Length Bypass Vulnerability
**Vulnerability:** The `content_length_limit_middleware` only enforced the payload limit if the `Content-Length` header was present. If a client omitted the header, the size check was bypassed entirely, allowing arbitrarily large payloads to be processed and potentially leading to Denial of Service (DoS). The check for `Transfer-Encoding: chunked` was also bypassable due to strict exact-match checking rather than case-insensitive substring matching.
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted or obfuscated via casing.
**Prevention:** Always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Perform case-insensitive substring matching for headers that can contain multiple values or non-standard casing (e.g., `Transfer-Encoding`).
