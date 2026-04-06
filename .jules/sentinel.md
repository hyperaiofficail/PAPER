## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.
## 2024-04-06 - Missing Content-Length Header Validation
**Vulnerability:** File upload and processing endpoints did not enforce the presence of a Content-Length header, meaning that an attacker could bypass payload size limitations simply by omitting the header.
**Learning:** Relying on the presence of a header (like Content-Length) to enforce security limits can lead to bypasses if the header is completely omitted. When enforcing payload size limits, always explicitly validate and mandate the presence of the header.
**Prevention:** For any endpoint enforcing upload limits, ensure the Content-Length header is mandatory for POST/PUT/PATCH requests and explicitly reject requests (e.g., return 411 Length Required) when it is missing.
