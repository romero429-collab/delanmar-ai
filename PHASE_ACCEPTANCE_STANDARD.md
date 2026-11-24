# Phase Acceptance Standard

## Maturity levels

| Level | Meaning |
|---|---|
| Implemented | Code exists. |
| Tested | A test has demonstrated the behavior. |
| Piloted | It has operated in a controlled real-world workflow. |
| Production-ready | Security, reliability, recovery and operational requirements have been validated. |

A component can be implemented without being production-ready. Skipped or unavailable tests are not passes.

## Rules for declaring a phase complete

1. All deliverables in the phase specification in `phases/` meet the maturity level the phase requires.
2. All dependency phases have passed their gates.
3. Evidence is recorded: revision, environment, commands, results, limitations and reviewer.
4. Authorization-related work includes negative tests (denied, malformed, unauthenticated, bypass attempts fail closed).
5. No integration bypasses the Rust Core authorization contract: no agent may exercise authority the Core has not explicitly granted.
6. Unresolved risks and approved exceptions are documented; security gates are not silently weakened.
7. [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) is updated.
8. The human owner approves closure.
