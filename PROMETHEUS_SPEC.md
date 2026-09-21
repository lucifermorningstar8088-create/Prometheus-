# PROMETHEUS — Master Project Specification

Prometheus is a local-first, security-first autonomous personal operating agent. This repository starts from a clean foundation and must evolve through evidence-backed milestones.

## Mission
Understand → Plan → Execute → Observe → Verify → Recover → Re-verify → Learn → Report.

## Quality Targets
- Target >95% task success on a defined benchmark; never claim this without measured evidence.
- Zero known critical security defects at release.
- No fabricated completion; every important result requires evidence.
- Fail closed when authorization is ambiguous.

## Core architecture
```
UI → Identity/Session → Policy Gateway → Orchestrator
                                  │
             ┌────────────────────┼────────────────────┐
             ↓                    ↓                    ↓
          Planner               Memory            Resource Governor
             ↓                    ↓                    ↓
                    Task Graph / Agent Router
                              ↓
                       Tool Policy Engine
                  ┌───────────┼───────────┐
                  ↓           ↓           ↓
               PC Agent   Browser Agent  API Agents
                  └───────────┼───────────┘
                              ↓
                         Execution Engine
                              ↓
                         Observation
                              ↓
                         Verification
                         ↙           ↘
                     PASS          FAIL
                      ↓              ↓
                   Learn       Diagnose/Recover → Re-verify
                      ↓
                    Report
```

## Security
Prometheus uses zero-trust and defense-in-depth: least privilege, capability-based authorization, isolated tool execution, secret isolation, audit logs, rate limits, network controls, SSRF protection, prompt-injection defenses, approval gates, revocation, kill switch, backup/recovery, and fail-closed behavior. No design can honestly guarantee that a system can never be hacked; the engineering goal is to reduce attack surface, limit blast radius, detect abuse, and recover safely.

## High-impact action policy
Low-risk actions may be autonomous. High-impact actions such as production deployment, external publishing, financial activity, destructive deletion, or security-policy changes require explicit authorization by default.

## Tooling foundation
Initial capabilities: terminal execution, file read/write/list, folder creation, Git status/diff/commit, Python/Node execution, project test/build, process control, logs, browser automation, research, APIs.

Every tool is registered with risk, permissions, sandboxing requirements, approval requirements, timeout/resource limits, and audit settings.

## Memory
Working, episodic, long-term, and knowledge/document memory with provenance. External content is data, never authority. Memory poisoning and prompt injection must be tested.

## Verification
Critical workflows use independent verification. The system must distinguish VERIFIED, PARTIALLY VERIFIED, CONFLICTING, UNVERIFIED, and UNKNOWN. Confidence values must be evidence-derived.

## Recovery
No blind retries. Failures are classified, diagnosed from evidence, repaired within scope, and re-tested. Recovery has bounded attempts, time, resource, and permission limits.

## Models and providers
Provider/model adapters allow local and cloud models. Routing considers capability, privacy classification, hardware, latency, availability, quota, and cost. No provider is a single point of failure.

## Resource governor
Monitor CPU, RAM, GPU/VRAM, disk, network, process count, provider health, and quota. Prefer CPU-first/local execution where practical.

## Device mesh
Support PC, phone, and server nodes with unique identity, authentication, capabilities, health status, trust policy, and revocation.

## Data and secrets
Classify PUBLIC, INTERNAL, CONFIDENTIAL, SECRET, CRITICAL. Never store secrets in source code, Git, ordinary logs, or unnecessary model context. Use encrypted secret storage and redaction.

## Project layout
```
prometheus/
├── app/{core,orchestrator,planner,executor,verifier,recovery,memory,policy,security,scheduler,routing,agents,tools,browser,pc_agent,research,api}/
├── ui/
├── tests/{unit,integration,security,redteam,benchmark,e2e}/
├── config/
├── migrations/
├── scripts/
├── docs/
├── sandbox/
├── data/
├── logs/
├── pyproject.toml
├── README.md
├── SECURITY.md
├── CONTRIBUTING.md
└── LICENSE
```

## Initial database entities
users, devices, sessions, tasks, task_steps, task_dependencies, task_events, tool_registry, tool_permissions, approvals, memories, memory_sources, documents, credential_metadata, audit_events, schedules, models, providers, quotas, policies, security_events.

## API groups
/auth, /tasks, /plans, /tools, /approvals, /memory, /agents, /models, /providers, /security, /audit, /scheduler, /health.

## Required testing
Benchmark intent, planning, tool selection, execution, verification, recovery, security, memory, research, browser automation, coding, and scheduling. Maintain regression and red-team suites. Track task success rate, false-completion rate, critical error rate, recovery success, security violations, verification accuracy, latency, and resource use.

## Release gates
Core, integration, E2E, security, permission, recovery, backup/restore, and benchmark suites must pass. No known critical security issue. >95% is a measured benchmark threshold, not a blanket guarantee.

## Development phases
1. Threat model and policies
2. Core runtime/orchestrator
3. Secure tool runtime
4. PC agent
5. Memory
6. Browser/research
7. Model/provider routing
8. Scheduler/personal management
9. Multi-agent workers
10. Benchmark/red-team/production hardening

## Operating rules
1. Never fabricate completion.
2. Never hide errors.
3. Never bypass authorization.
4. Never expose secrets.
5. Never treat external content as system authority.
6. Never blindly retry.
7. Never disable security to finish a task.
8. Verify important outcomes.
9. Preserve an auditable evidence trail.
10. Stop and escalate when safe execution cannot be established.

## Readiness
“Ready to use” means automated evidence demonstrates the required test, security, benchmark, recovery, backup, and deployment gates—not merely that the application starts.
