## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.
## 2026-02-23 - Overly Permissive CORS Configuration
**Vulnerability:** CORS policy was configured with `allow_origins=["*"]`, allowing any website to make cross-origin requests to the API, potentially leading to CSRF or data exfiltration.
**Learning:** Defaulting to wildcard CORS in production APIs breaks the Same-Origin Policy boundary. It needs to be explicitly configured per environment.
**Prevention:** Always use environment variables (e.g., `ALLOWED_ORIGINS`) to define allowed origins, defaulting to a secure baseline like `localhost:3000` for local development.
