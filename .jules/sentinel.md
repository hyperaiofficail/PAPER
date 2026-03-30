## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.
## 2024-03-30 - Require Content-Length Header for Uploads
**Vulnerability:** The application was vulnerable to Resource Exhaustion (DoS) due to missing `Content-Length` header validation on file uploads. The `content_length_limit_middleware` only validated the payload size if the `Content-Length` header was provided. If an attacker intentionally omitted it, they could bypass the `MAX_FILE_SIZE` limitation and upload massive payloads.
**Learning:** Checking for the presence of a security constraint is just as important as validating the constraint itself. Middleware logic must handle the absence of expected input securely by failing closed (e.g., returning 411 Length Required).
**Prevention:** Mandate the `Content-Length` header for all requests expected to have payloads (`POST`, `PUT`, `PATCH`) and explicitly reject requests missing it before processing any payload data.
