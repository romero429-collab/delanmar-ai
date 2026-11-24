# Architecture

The [Core Architecture v1.0](../DELANMAR_CORE_ARCHITECTURE_v1.0.md) is the foundational technical authority and describes the target architecture. This document describes the current implementation and its verification limits.

| Layer | Language | Role |
|---|---|---|
| `core/` | Rust | 24-agent roster and human-approval policy (blueprint §8); JSON-lines bridge binary |
| `mojo/` | Mojo | Numeric/analytics kernels (pilot metrics) |
| `adapters/` | Python | Preliminary LangChain, LangGraph, CrewAI, and BeeAI integration seams |
| Root | Bazel | Builds, tests, and wires all languages |

Bazel builds `//core:delanmar_bridge`; the Python bridge client communicates with the Rust process through a JSON-lines contract (`{"op":"list_agents"}`, `{"op":"check_action","agent":..,"action":..}`) via `adapters/delanmar_adapters/bridge.py`. Bazel itself does not carry runtime messages. For known agents, actions not on the routine-action allowlist return `requires_human_approval`; unknown agents return `unknown_agent`.

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
