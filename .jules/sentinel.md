## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-03-02 - Hardcoded CORS Configuration
**Vulnerability:** A hardcoded `allow_origins=["http://localhost:3000"]` CORS restriction introduces deployment regressions if the application is promoted to staging or production environments with different domains.
**Learning:** Security fixes should be environment-aware. While restricting CORS from `*` to `http://localhost:3000` is safer for local development, it compromises functionality in other environments.
**Prevention:** Implement security constraints (like CORS allowed origins) using environment variables (e.g., `os.environ.get("ALLOWED_ORIGINS")`) with a secure fallback for local development.
