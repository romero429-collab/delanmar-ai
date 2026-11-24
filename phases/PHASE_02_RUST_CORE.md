# Phase 02 — Rust Core Hardening

**Status:** Prototype exists; trusted controls are not yet implemented.

## Objective and scope
Make Rust the authoritative enforcement point for identity, permissions, policy, task state, approval and audit.

## Existing components to reuse
`core/src/lib.rs` contains the 24-agent roster, shared routine-action allowlist and approval decisions; `core/src/main.rs` exposes the current JSON-lines handler. These are prototypes, not a security boundary.

## Required work
- Define authenticated caller and agent identities, role- and action-based, per-agent least-privilege capabilities and deny-by-default authorization.
- Ensure all action execution paths are mediated by core; framework tool availability must never confer authority.
- Define durable task lifecycle and tamper-evident or otherwise protected audit events, with appropriate access, retention and recovery controls.
- Record human approval decisions, approver identity, scope, expiry and action binding; reauthorize before execution and prevent replay or use of stale approvals.
- Specify failure and escalation behavior, including the distinction between denied actions and explicitly approval-eligible actions.

## Dependencies
Phases 0 and 1; coordinate interface decisions with Phases 3 and 4.

## Testing requirements
Test unknown or spoofed identities, cross-agent access, permitted and denied actions, approval scope/expiry/replay, persistence and recovery, concurrent state transitions, and unavailable policy or audit services. Verify bypass attempts fail closed.

## Acceptance criteria
- Every governed execution is authenticated, authorized against agent-specific policy, and auditable; failures cannot grant access.
- Human approval is attributable and bound to the exact authorized action, and restricted actions do not run without it.
- Test evidence covers negative paths, audit integrity, and recovery; residual security risks have an owner.

## Outstanding risks
Bypass through adapters or tools, privilege escalation, stale approvals, sensitive audit data and incomplete enforcement.

## Handoff
Supply authoritative decisions and lifecycle semantics to the agent contract, bridge and certified adapters.
