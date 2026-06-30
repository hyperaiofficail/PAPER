## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-24 - DoS and Path Handling Bypass via None Filenames
**Vulnerability:** When a user uploaded a file without a filename (resulting in `UploadFile.filename` being `None`), an unhandled `AttributeError` occurred when calling `.replace()` during filename sanitization, leading to a Denial of Service (DoS). Additionally, whitespace-only or '.'/'..' filenames were not adequately neutralized, which could lead to unexpected behavior in file handling downstream.
**Learning:** In frameworks like FastAPI, properties like `filename` on uploaded files can be `None`. Applying string operations without checking or coalescing these values creates fragility.
**Prevention:** Always coalesce potentially `None` string values from user inputs (e.g., `file.filename or ""`) before manipulation. Furthermore, explicitly check for and safely default out of problematic edge cases like empty strings, whitespace-only names (via `.strip()`), or explicit relative traversal dots (`.` and `..`).
