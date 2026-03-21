## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2024-03-01 - Transfer-Encoding chunked DoS bypass
**Vulnerability:** Exact match check on `Transfer-Encoding: chunked` in HTTP middleware allowed attackers to bypass the check using different casing (`Chunked`) or multiple encodings (`gzip, chunked`), potentially leading to a Denial of Service via resource exhaustion.
**Learning:** Checking HTTP headers like `Transfer-Encoding` with strict equality fails to account for HTTP specification allowances (e.g. comma-separated lists, case insensitivity) which attackers can exploit.
**Prevention:** Always use case-insensitive substring checks or parse lists properly when validating security-sensitive headers like `Transfer-Encoding`.
