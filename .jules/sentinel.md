## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-22 - Bypass of Payload Size Limit (DoS)
**Vulnerability:** The application enforced payload size limits by checking the `Content-Length` header, but did not mandate its presence. An attacker could bypass the limit entirely by simply omitting the header. It also improperly rejected `Transfer-Encoding: chunked` by doing an exact case-sensitive match.
**Learning:** Relying on the presence of a header to enforce security limits can lead to bypasses if the header is completely omitted or casing/formats aren't handled securely.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). When validating headers like Transfer-Encoding, normalize the value to lowercase and use substring matching.
