# Phase Acceptance Standard

## Maturity levels

| Level | Meaning |
|---|---|
| Implemented | The required artifact or capability exists. |
| Tested | Tests or documented verification demonstrate the required behavior. |
| Piloted | It has operated in a controlled real-world workflow. |
| Production-ready | Security, reliability, recovery and operational requirements have been validated. |

A component can be implemented without being production-ready. Skipped or unavailable tests are not passes.

Each specification identifies its minimum maturity and observable exit criteria. Assess the exact artifact, capability or certification track in scope rather than assigning a maturity level to the whole platform. Documentation of requirements alone does not complete a phase or certification track.

## Rules for declaring a phase complete

1. All deliverables in the phase specification in `phases/` meet the maturity level the phase requires.
2. Applicable dependency gates have passed. A pilot may use a validated subset without full acceptance of unrelated platform work, but must pass all security, authorization, operational and human-approval gates applicable to that workflow. Record the scope and any deferred work.
3. Evidence is recorded: revision, environment, commands or procedure, results, limitations and reviewer.
4. Authorization-related work includes positive tests and negative tests (denied, malformed, unauthenticated and bypass attempts fail closed), as applicable to the phase and its scope.
5. No integration bypasses the Rust Core authorization contract: no agent may exercise authority the Core has not explicitly granted.
6. Unresolved risks and approved exceptions are documented; security gates are not silently weakened.
7. [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) is updated.
8. The human owner approves closure.
