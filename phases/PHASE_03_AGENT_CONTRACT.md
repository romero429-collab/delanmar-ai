# Phase 03 — Common Agent Contract

**Status:** Not implemented; the constitution specifies required fields.

## Objective and scope
Define one versioned, framework-independent contract for agents, tasks and governed interactions.

## Existing components to reuse
[Constitution §6](../DELANMAR_CORE_ARCHITECTURE_v1.0.md), the Rust roster and policy prototype, workforce role definitions, and the current bridge request shapes.

## Required work
- Specify stable identity, role, capabilities, tool references, permissions, input/output schemas, communication, and access-controlled memory/state references.
- Define task lifecycle, execution history, errors, escalation, approvals and audit references; make the core authoritative for identity and permissions.
- Define schema validation, version compatibility and migration rules, plus adapter conformance and state portability requirements.
- Separate business-specific policy and data from reusable contract definitions.

## Dependencies
Phases 0–2 for governing principles and core semantics; coordinate versioning with Phase 4.

## Testing requirements
Validate compliant and malformed messages, unknown versions and fields, lifecycle transitions, unauthorized references, and portability across independent adapter representations.

## Acceptance criteria
- A reviewed, versioned contract specifies required fields, ownership, access boundaries, compatibility and failure behavior.
- Conformance tests demonstrate that adapters cannot expand permissions or lose approval and audit context.

## Outstanding risks
Framework-specific leakage, incompatible version changes, exposed memory references and ambiguity about authoritative state.

## Handoff
Use the contract as the basis for Phase 4 protocol and Phase 7 adapter certification.
