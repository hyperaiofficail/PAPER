## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS bypass in HTTP Headers
**Vulnerability:** Transfer-Encoding chunked logic used exact string match (`== "chunked"`), allowing bypasses using variations like `Transfer-Encoding: Chunked` or `Transfer-Encoding: gzip, chunked`, which bypasses maximum payload limits.
**Learning:** Checking HTTP headers strictly via case-sensitive matches can lead to vulnerabilities since headers are case-insensitive and can combine values (e.g. gzip, chunked).
**Prevention:** Always use case-insensitive checks and look for substrings (e.g., `in te.lower()`) when verifying HTTP header mechanisms like Transfer-Encoding.
