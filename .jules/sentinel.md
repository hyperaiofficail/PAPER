## 2026-02-22 - Path Traversal in File Upload
**Vulnerability:** User-controlled filenames were used directly in potential file paths (e.g. download URLs), allowing path traversal sequences like '../../'.
**Learning:** Even if the file isn't saved to disk immediately, using raw input in paths sets a dangerous precedent and can lead to vulnerabilities if code evolves.
**Prevention:** Always sanitize filenames using os.path.basename (and handle cross-platform separators) before using them in any path-like context.

## 2023-10-25 - Content-Length and Path Traversal Edge Cases
**Vulnerability:** DoS limitation on file uploads could be bypassed by entirely omitting the `Content-Length` header in a `POST`, `PUT`, or `PATCH` request. Path sanitization via `os.path.basename(file.filename.replace("\\", "/"))` was also failing and resulting in Server Crashes (`AttributeError` or un-sanitized outcomes) because `file.filename` can be `None`, an empty string `""`, or a literal `.` or `..` resolving to an invalid file path.
**Learning:** Relying on the conditional existence of a header (like `if content_length:`) to apply security validations allows an attacker to bypass the validation simply by removing the header. Path sanitization needs an aggressive set of fallbacks for `None`, empty strings, pure whitespace, and reserved names (`.`, `..`).
**Prevention:** If a property like size or length is required for security constraints, the presence of the determining headers (e.g. `Content-Length`) must be strictly mandated, failing the request securely (e.g., returning `411 Length Required`) if omitted. When sanitizing file names, assign a fallback static string (e.g. `unnamed`) rather than processing empty strings or `None` values blindly.
