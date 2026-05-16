## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-24 - DoS and Path Traversal via None/Empty Filename
**Vulnerability:** The application was susceptible to `AttributeError` crashing the endpoint if `UploadFile.filename` was `None`, as it attempted to run string replacements on it. Furthermore, it did not robustly handle strings evaluating to empty or dot sequences (like " . ") after trimming.
**Learning:** `UploadFile.filename` in FastAPI can legitimately be `None` or empty. String operations must safely handle this (e.g. falling back to `""` before processing) and further validate that the remaining filename is safe after extraction and stripping.
**Prevention:** Ensure that `file.filename` is coerced to a string before string operations, explicitly strip whitespace from the extracted basename, and fall back to a safe default (like 'unnamed') if the resulting name is empty or effectively `.` or `..`.
