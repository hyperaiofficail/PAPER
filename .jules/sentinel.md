## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-04-15 - Missing Content-Length Validation
**Vulnerability:** The application enforced maximum file sizes using the `Content-Length` header but did not mandate the header's presence for POST/PUT/PATCH requests. This allowed attackers to bypass size constraints by simply omitting the header, potentially leading to Resource Exhaustion/Denial of Service (DoS).
**Learning:** Relying on the presence of a header to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent).
