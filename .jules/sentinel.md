## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-23 - File Upload NoneType DoS and Deep Path Traversal
**Vulnerability:** The application assumed `file.filename` on a FastAPI `UploadFile` was always a string. If an attacker uploaded a file without a filename, it evaluated to `None`, causing `.replace()` to throw an unhandled `AttributeError` leading to a DoS. Furthermore, if a filename resulted in an empty string or `.`/`..` after `os.path.basename` and stripping, it was still used in path structures.
**Learning:** FastAPI `UploadFile.filename` can be `None`. Always handle `None` types safely (e.g., `file.filename or ""`) before performing string operations. Additionally, checking for `.` or `..` or empty names *after* `os.path.basename` extraction is critical to ensure a usable fallback name.
**Prevention:** Coalesce potentially `None` strings before `.replace()` or `.strip()`, and explicitly validate that the finalized basename is not an empty string or traversal dots, reverting to a safe default like `"unnamed"` if so.
