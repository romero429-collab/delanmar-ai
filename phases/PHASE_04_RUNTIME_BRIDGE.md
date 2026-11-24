# Phase 04 — Runtime Communication Bridge

**Status:** JSON-lines prototype exists; it is not an authenticated or production-ready boundary.

## Objective and scope
Harden communication between the trusted core and adapters, with versioned interfaces and a path to future language bindings.

## Existing components to reuse
`core/src/main.rs`, `core/src/lib.rs` request handler, `adapters/delanmar_adapters/bridge.py` and `adapters/tests/bridge_test.py`.

## Required work
- Define versioned request/response envelopes and contract validation, identity propagation, authorization and auditable correlation.
- Handle malformed input, size limits, process startup/shutdown, timeouts, errors, concurrency and recovery without silent execution or data loss.
- Define compatibility and migration behavior and the security requirements for future bindings.
- Ensure a missing core decision or unavailable audit/approval service cannot result in governed execution.

## Dependencies
Phases 2 and 3 supply authority and semantics; Phase 1 supplies toolchain baseline.

## Testing requirements
Exercise malformed and oversized messages, incompatible versions, caller spoofing, timeouts, process exits, retries, concurrent requests, partial responses and core outages. Test full Rust/Python request and response paths.

## Acceptance criteria
- Supported boundary operations validate versions and caller context, preserve task and audit references, and fail closed.
- Lifecycle and failure tests pass in documented environments; supported compatibility and recovery behavior is documented.

## Outstanding risks
Protocol desynchronization, subprocess hangs, duplicate side effects on retries, authentication bypass and lost audit context.

## Handoff
Provide a tested runtime boundary to Phase 7 adapters and Phase 8 Alpha; provide interface requirements to Phase 5.
