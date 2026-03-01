## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - Overly Permissive CORS Configuration
**Vulnerability:** The FastAPI backend used a wildcard `allow_origins=["*"]` combined with `allow_credentials=True`. This is inherently insecure, allowing any external origin to send requests with credentials (like cookies or Authorization headers) to the backend. Modern browsers and web frameworks (like Starlette) also actively reject this configuration as invalid.
**Learning:** Default configurations in quickstart guides or legacy code often use `["*"]` for ease of development, masking the significant security risk and functional incompatibility when credentials are required.
**Prevention:** Always restrict CORS origins to a specific list of trusted domains. Use environment variables (e.g., `ALLOWED_ORIGINS`) to define these dynamically for different environments (development, staging, production) while providing safe defaults (like `http://localhost:3000`).
