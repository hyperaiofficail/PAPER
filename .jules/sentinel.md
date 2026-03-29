## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-03-29 - [Missing Content-Length enforcement bypasses DoS protection]
**Vulnerability:** The application had an anti-DoS middleware intended to limit the maximum size of `POST`/`PUT`/`PATCH` request bodies to 10MB by checking the `Content-Length` header. However, if the `Content-Length` header was completely omitted from the request, the application would simply bypass the check and process the request anyway, allowing an attacker to submit arbitrarily large payloads and potentially crash the service via memory exhaustion.
**Learning:** Security validations that rely on an optional header must account for the absence of that header. If the check is skipped when the header is missing, the security measure can be easily bypassed. We must mandate the presence of required headers, or rely on streaming validation instead of just header claims.
**Prevention:** Mandate a `Content-Length` header for requests with bodies (returning `411 Length Required` if missing), and additionally reject chunked transfer encoding (`Transfer-Encoding: chunked`) if streaming validation is not implemented, ensuring that body sizes are explicitly declared and checked before being processed.
