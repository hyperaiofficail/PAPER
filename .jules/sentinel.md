## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - Overly Permissive CORS Configuration
**Vulnerability:** The FastAPI application used a hardcoded wildcard (`allow_origins=["*"]`) for CORS. This allowed any website to make cross-origin requests to the API, potentially leading to unauthorized data access if session cookies or credentials are used.
**Learning:** Default configurations often prioritize developer convenience over security. A wildcard allows any domain to access the application's resources, bypassing the Same-Origin Policy.
**Prevention:** Always use a specific whitelist of allowed origins or an environment variable (`ALLOWED_ORIGINS`) to restrict CORS access to trusted domains.
