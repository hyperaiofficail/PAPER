## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2024-04-08 - DoS Bypass via Missing Content-Length Header
**Vulnerability:** The `Content-Length` payload size enforcement logic assumed the header would be present. If an attacker omitted the header entirely, the validation logic (`if content_length:`) was bypassed, allowing arbitrarily large payloads to be processed and leading to a potential Denial of Service (DoS) via resource exhaustion.
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent).
