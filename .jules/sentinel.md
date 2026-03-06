## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2024-05-20 - Fix Overly Permissive CORS Configuration
**Vulnerability:** The backend was configured with a wildcard (`*`) for CORS `allow_origins`. This could potentially allow any external origin to make cross-origin requests to the API.
**Learning:** Hardcoded wildcard allowed origins can leave the API vulnerable. Although the backend was a basic API and did not authenticate users, any cross-origin requests could read sensitive information returned by tools if authentication is ever introduced.
**Prevention:** Always restrict CORS configurations to exactly the trusted origins needed for an application, defaulting to the application's frontend origin.
