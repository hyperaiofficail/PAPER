## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2024-05-23 - Missing Content-Security-Policy Header
**Vulnerability:** The application was missing the `Content-Security-Policy` HTTP header, exposing it to Cross-Site Scripting (XSS) and data injection attacks.
**Learning:** Security middleware functions should be comprehensively audited against standard lists of recommended security headers (CSP, HSTS, X-Content-Type-Options, etc.). Partial implementation of security headers can leave critical vulnerabilities unresolved while creating a false sense of security.
**Prevention:** Establish a standardized checklist of security headers to implement for all web applications, and include automated tests asserting the presence and correct values of these headers to prevent regressions.
