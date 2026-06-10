## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-23 - DoS via Unhandled None in Uploaded Filename
**Vulnerability:** The application attempted to sanitize the uploaded file's name using `.replace()`, but it failed to account for `UploadFile.filename` potentially being `None`. When no filename was provided by the client, this resulted in an unhandled `AttributeError`, causing a Denial of Service. Furthermore, strings reducing to `.` or `..` were not handled as exceptions.
**Learning:** Always coalesce optional attributes (`file.filename or ""`) before performing string manipulations, as they might be `None` in certain edge cases like no provided filename. Additionally, properly stripping the resolved filename and checking it against anomalies is required.
**Prevention:** Explicitly enforce a fallback or default value string when `os.path.basename` resolves to an empty value or `.`/`..` and coalesce optional variables.
