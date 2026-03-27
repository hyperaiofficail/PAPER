## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.
## 2026-02-23 - Missing File Size Limitations on Upload
**Vulnerability:** The `/process/{tool_name}` endpoint accepted file uploads without enforcing any size limits.
**Learning:** This exposes the application to Denial of Service (DoS) attacks via resource exhaustion (disk space or memory), particularly given the general utility nature of the platform where many tools accept files.
**Prevention:** Always implement explicit file size limits for `UploadFile` inputs. In FastAPI, this can be securely achieved by seeking to the end of the file (`file.file.seek(0, os.SEEK_END)`) and reading its position (`file.file.tell()`), ensuring the pointer is reset afterwards so downstream processing remains unaffected.
