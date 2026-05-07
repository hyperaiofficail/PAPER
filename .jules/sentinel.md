## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS via Missing Headers and Case-Sensitive Checks
**Vulnerability:** The size limits enforced for file uploads relied on the presence of the Content-Length header, allowing an attacker to omit the header entirely and bypass the payload size restriction, leading to a Denial of Service (DoS) vulnerability via resource exhaustion. Further, the check for chunked encoding was strictly case-sensitive ("chunked"), opening a potential bypass via "ChUnKeD" or if presented alongside other encodings (e.g. "gzip, chunked").
**Learning:** Security validations that rely solely on headers must ensure those headers are explicitly mandated if they define payload characteristics. Omitting a required header is a bypass tactic. Case-insensitivity and substring matching are essential for robust string verification.
**Prevention:** Mandate the presence of explicitly verified security headers (e.g., returning a 411 Length Required for missing Content-Length). Validate header contents with case-insensitive, comprehensive substring checks instead of strict equality.
