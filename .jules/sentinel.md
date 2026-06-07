## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - DoS Bypass via Missing Content-Length
**Vulnerability:** The application enforced a maximum payload size limit by checking the `Content-Length` header, but it did not mandate the header's presence for methods like POST/PUT/PATCH. This meant attackers could bypass the size limit entirely by omitting the `Content-Length` header or using `Transfer-Encoding: chunked` (with non-standard casings or multiple values).
**Learning:** Relying on the presence of a header (like `Content-Length`) to enforce security limits can lead to bypasses if the header is completely omitted.
**Prevention:** When enforcing payload size limits, always explicitly validate and mandate the presence of the header (e.g., returning a 411 Length Required response if absent). Also ensure `Transfer-Encoding: chunked` checks are case-insensitive and handle multiple values.

## 2026-02-24 - DoS via Unhandled AttributeError in Filename Processing
**Vulnerability:** The application attempted to access and perform string operations on `UploadFile.filename` directly (e.g., `file.filename.replace()`), without handling the case where `filename` is `None` (which can occur if the client does not provide a filename). This could lead to an unhandled `AttributeError`, resulting in a Denial of Service (DoS) crash for the endpoint.
**Learning:** Framework objects (like FastAPI's `UploadFile`) may have fields that are unexpectedly `None` based on client input. Always defensive program against these possibilities.
**Prevention:** Always coalesce potentially `None` values (e.g., `file.filename or ""`) before executing string operations to prevent unhandled `AttributeError` crashes. Ensure any resulting empty or dangerous values (like `""`, `"."`, `".."`) are safely defaulted.
