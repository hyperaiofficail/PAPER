## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.
## 2026-02-23 - Overly Permissive CORS Configuration
**Vulnerability:** The CORS configuration used wildcards (`*`) for `allow_methods` and `allow_headers`. This is a security risk because it allows any HTTP method and any custom headers from the allowed origins, violating the principle of least privilege.
**Learning:** Even when origins are restricted, overly permissive methods and headers can lead to unexpected vulnerabilities or bypasses if the application or its middleware isn't perfectly hardened against obscure methods or headers.
**Prevention:** Always explicitly define the allowed HTTP methods (e.g., `["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]`) and headers (e.g., `["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"]`) in CORS configurations.
