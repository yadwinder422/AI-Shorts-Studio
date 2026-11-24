# Security policy

## Reporting vulnerabilities
Please use the repository's Security tab and private vulnerability reporting if enabled. Do not publish credentials, private media, or exploit details in public issues. If private reporting is unavailable, request a private contact without disclosing sensitive details.

## Privacy and scope
The current CLI runs locally, with no network calls, external AI APIs, telemetry, or third-party Python packages. Input is restricted to UTF-8 text up to 1 MiB; output uses exclusive creation to avoid overwriting existing files. Generated subtitles contain narration text and are not encrypted. Restrict local folder access and keep private assets outside the repository. Do not run in directories writable by untrusted users.

Git ignore rules are preventive only and cannot remove previously committed secrets. Revoke and rotate any exposed credentials immediately. Enable GitHub two-factor authentication and secret scanning/push protection where available. Review changes before merging. No independent security audit has been performed.
