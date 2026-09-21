# Prometheus Security Baseline

## Threat Model

Prometheus assumes the host, network, external websites, downloaded files, model outputs, plugins, and tool results may be compromised or untrusted. Security boundaries must be explicit.

## Security Requirements

- Zero-trust authentication and authorization.
- Least privilege for every tool and device.
- Capability-based permissions.
- Sandbox untrusted code and documents.
- Default-deny outbound network policy for privileged tools.
- SSRF protections for browser/API tools.
- Separate system instructions, user authorization, trusted memory, tool output, and external content.
- Treat external content as data, never as authority.
- Encrypt secrets at rest and protect them from model context and logs.
- Redact tokens, passwords, cookies, and authorization headers from telemetry.
- Immutable/tamper-evident audit events for privileged operations.
- Explicit approval for high-impact actions.
- Emergency kill switch and session/tool revocation.
- Resource limits, timeouts, and bounded retries.
- Secure update verification and rollback.
- Encrypted backup and tested restoration.

## High-Impact Actions

Production deployment, destructive deletion, external publishing, financial operations, credential changes, access-control changes, and security-policy modifications require explicit authorization unless an intentionally configured policy says otherwise.

## Prompt Injection

External content can contain instructions designed to manipulate the agent. Such content must remain untrusted data. Prometheus must never promote web pages, documents, emails, tool output, or retrieved text to system authority merely because the content requests it.

## Secrets

Never put secrets in source code, Git, ordinary logs, benchmark fixtures, prompts, or persistent task messages. Use an encrypted secret store and expose only the minimum secret scope required for a tool call.

## Incident Response

Detect → Isolate → Revoke → Preserve evidence → Stop affected tools → Assess → Recover → Verify → Resume.

## Security Testing

Include automated tests for command injection, path traversal, SSRF, privilege escalation, secret leakage, prompt injection, malicious documents, poisoned memory, unauthorized tool execution, session theft, replay, malformed provider responses, and unsafe autonomous actions.

## Security Claim Policy

No implementation may claim that Prometheus is impossible to hack. Security claims must be backed by defined threat models, tests, reviews, and deployment assumptions.
