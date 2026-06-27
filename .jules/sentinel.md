## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-23 - AttributeError DoS & Incomplete Path Traversal
**Vulnerability:** A missing check on `file.filename` meant that if a client provided a file upload without a filename (causing FastAPI to parse `file.filename` as `None`), attempting string operations like `.replace()` on it would trigger an unhandled `AttributeError`, leading to a Denial of Service. Furthermore, `os.path.basename` could return `.` or `..` or be empty after stripping whitespace, potentially leading to incomplete path traversal mitigation when constructing download URLs or saving files.
**Learning:** External user input, even metadata like filenames, can be explicitly `None` in FastAPI depending on how the client crafts the request. Additionally, `os.path.basename` does not guarantee a safe, non-navigational string on its own.
**Prevention:** Always coalesce potentially `None` filename values (e.g., `file.filename or ""`) before performing string operations. After extracting the base name, explicitly strip whitespace and check if the resulting filename is empty, `.`, or `..`, falling back to a safe default like `unnamed`.
