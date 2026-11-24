# Architecture

The [Core Architecture v1.0](../DELANMAR_CORE_ARCHITECTURE_v1.0.md) is the foundational technical authority and describes the target architecture. This document describes the current implementation and its verification limits.

| Layer | Language | Role |
|---|---|---|
| `core/` | Rust | 24-agent roster and human-approval policy (blueprint §8); JSON-lines bridge binary |
| `mojo/` | Mojo | Numeric/analytics kernels (pilot metrics) |
| `adapters/` | Python | Preliminary LangChain, LangGraph, CrewAI, and BeeAI integration seams |
| Root | Bazel | Builds, tests, and wires all languages |

Bazel builds `//core:delanmar_bridge`; the Python bridge client communicates with the Rust process through a versioned (`version: 1`) JSON-lines contract (`{"version":1,"op":"list_agents"}`, `{"version":1,"op":"authorize","agent":..,"action":..}`) via `adapters/delanmar_adapters/bridge.py`. Bazel itself does not carry runtime messages.

Phase 1 Increment 1 (identity and authorization contract): the launcher binds the bridge process to one of the 24 stable agent identities over a private inherited descriptor (`--caller-fd`); the `agent` in a request is only a claim and must match the bound caller. Authorization is default-deny with per-agent permission tables; decisions are `allow`, `deny` or `approval_required`. `approval_required` never means allowed, and the nine blueprint actions can never be `allow`. Malformed requests, unsupported versions, unauthenticated callers and policy failure all deny. The production policy grants no permissions for any agent; test fixtures in `core/src/lib.rs` are labeled and are not business permissions.

Not implemented in Increment 1: approval records and audit (Increment 2), execution broker and resource restrictions (3), framework bypass prevention (4: the Python helper remains voluntary), adversarial certification (5). The inherited-descriptor binding is a first mechanism for a local trusted launcher; it is not verified against a hostile same-user process.

The current policy is a prototype, not an enforced system-wide security boundary: the bridge does not authenticate callers, apply per-agent permissions, execute approved actions, or provide an approval workflow. Some adapter helpers call the gate, but framework execution and tools are not universally constrained by it. The common agent contract and AG2 adapter described in the constitution are not yet implemented.

## Status (verified vs. not)

- Previously verified: Rust core unit tests and bridge via `cargo test` / `cargo run` in `core/`.
- Not verified: Bazel files and rule versions, the Mojo kernel, and all LangChain/LangGraph/CrewAI/BeeAI calls (frameworks are not version-pinned; BeeAI is only a documented seam).

### Local verification snapshot

On 2026-11-24, against code at revision `c6905aa`, a Linux environment with Rust/Cargo 1.100.0 and Python 3.12.3 produced the following results (commands are run from the repository root):

| Check | Result |
|---|---|
| `cargo test --locked --manifest-path core/Cargo.toml` | Passed: three Rust unit tests; no binary or doc tests. |
| `cargo build --locked --manifest-path core/Cargo.toml` | Passed: built the Rust bridge. |
| `PYTHONPATH=adapters DELANMAR_BRIDGE="$PWD/core/target/debug/delanmar_bridge" python3 -m unittest discover -s adapters/tests -p '*_test.py' -v` | Passed: three Python bridge tests. Python reported unclosed-file `ResourceWarning`s; process cleanup needs investigation. |
| `bazel --version` | Timed out after 12 seconds; no Bazel build or test was verified. |
| Mojo | `mojo` executable unavailable; no Mojo test was run. |

This snapshot does not verify framework calls, CI, reproducibility, security enforcement, or other environments. See [IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md) and [Phase 1](../phases/PHASE_01_SECURITY_CORE.md) for the remaining work.
