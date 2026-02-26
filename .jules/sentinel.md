## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2026-02-23 - Unrestricted File Upload Size (DoS)
**Vulnerability:** The application accepted unlimited file uploads without a `Content-Length` check or stream limit, allowing Denial of Service via resource exhaustion.
**Learning:** `UploadFile` in FastAPI streams to disk by default, meaning even if the application logic doesn't read the file, the server still accepts and buffers the entire payload, consuming disk space and bandwidth.
**Prevention:** Implement a middleware to check `Content-Length` headers early and/or use stream-limiting wrappers to reject large payloads before they are fully received.
