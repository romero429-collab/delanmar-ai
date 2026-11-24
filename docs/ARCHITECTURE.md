# Architecture

The [Core Architecture v1.0](../DELANMAR_CORE_ARCHITECTURE_v1.0.md) is the foundational technical authority and describes the target architecture. This document describes the current implementation and its verification limits.

| Layer | Language | Role |
|---|---|---|
| `core/` | Rust | 24-agent roster, default-deny policy, and JSON-lines bridge binary |
| `mojo/` | Mojo | Numeric/analytics kernels (pilot metrics) |
| `adapters/` | Python | Preliminary LangChain, LangGraph, CrewAI, and BeeAI integration seams |
| Root | Bazel | Configuration intended to build, test, and wire the languages; unverified |

The Python bridge client in `adapters/delanmar_adapters/bridge.py` communicates with the Rust process over JSON lines. The strict v2 contract requires a request ID for each operation and, for authorization, an agent, action, resource (`kind` and `id`), and context (`operation` and `purpose`). Responses carry a structured decision and reason; malformed requests and unsupported versions are denied. Bazel itself does not carry runtime messages, and the `//core:delanmar_bridge` build has not been verified.

Phase 1 identity and authorization work is in progress. Per-agent policy is default-deny; production grants are empty, and test fixtures are not business permissions. Decisions include `allow`, `deny`, and `approval_required`; the latter is not permission to execute. The nine blueprint actions cannot be `allow`. There is no trustworthy caller authentication yet: inherited-descriptor self-assertion has been removed, and the production bridge denies all calls. Resource and context are contract fields, not enforced policy scopes.

### Identity boundary and migration

The former Python-created pipe conveyed an **identity assertion**, not an authenticated identity: any same-user process could launch a bridge and write `admin` to its own pipe. The binary now ignores that mechanism and cannot establish a caller. A future trusted launcher must authenticate workloads independently, map them to permitted agents, protect its binary and policy, and isolate workloads from the launcher's authority. A Unix socket with peer credentials alone cannot distinguish adversaries sharing one OS user; separate OS identities or equivalent isolation and a reviewed identity mapping are needed. No supported secure deployment or launcher is implemented. `Core::new` accepts a principal from its embedding process and is not an authentication boundary; callers must not supply an untrusted assertion as a principal.

Version 2 is a deliberate breaking migration: version 1 requests and caller bindings are not accepted. Callers must supply the required v2 fields; there is no automatic legacy fallback. IDs and other fields are nonempty ASCII identifiers of at most 128 bytes, using letters, digits, `.`, `_`, `:`, `-`, or `/`; identifiers must not contain secrets or personal data. A structurally valid request's response echoes its request ID; an unparseable request has a null request ID, which the Python client rejects. The client generates a random ID and validates response fields, correlation, decisions and reasons. IDs are for correlation only: replay prevention, Rust input line limits, trusted context, resource-level policy, and execution binding are not implemented.

The Python client supports POSIX pipe I/O only and rejects concurrent calls or concurrent close on a bridge instance. It uses a configurable positive timeout (default five seconds) for each request's pipe exchange, limits each client-side message to 64 KiB, and closes and terminates the direct subprocess on errors, timeouts or explicit close. A context manager provides cleanup on exceptions. These controls do not authenticate the executable selected by the caller or contain its descendants; a malicious executable or compromised same-user process is outside this reliability mechanism. The client mirrors the nine consequential actions as a defense-in-depth response check; maintain this list in sync with Rust. Network and multi-tenant deployment are unsupported.

Approval records and workflow, audit, an execution broker, resource/context enforcement, framework bypass prevention, and adversarial certification are not implemented.

The current policy is a prototype, not an enforced system-wide security boundary. LangChain and LangGraph helpers voluntarily call the gate, but framework execution and tools can bypass them; the CrewAI helper uses the roster and does not gate execution. BeeAI is a callable seam, not a verified integration. The common agent contract and AG2 adapter described in the constitution are not yet implemented.

## Status (verified vs. not)

- The snapshots below apply only to their stated revisions.
- Not verified: Bazel files and rule versions, the Mojo kernel, and all LangChain/LangGraph/CrewAI/BeeAI calls (frameworks are not version-pinned; BeeAI is only a documented seam).

### Increment 1 correction verification

#### Final PR #7 review snapshot

On 2026-11-24, code revision `7379f362560eaa756468e9f10010ae25b7bb85e9` was tested against main revision `b730a88150fbd632cf73f3c0a52192c2cd577563` on Linux 7.0.0-1017-azure x86_64, Rust/Cargo 1.100.0 and Python 3.12.3. Commands ran from the repository root:

| Command | Result |
|---|---|
| `cargo test --locked --manifest-path core/Cargo.toml` | Passed: 15 Rust unit tests, including malformed contracts, both operations' unknown fields, policy errors, duplicate grants and synthetic identity mismatch. |
| `cargo build --locked --manifest-path core/Cargo.toml` | Passed. |
| `PYTHONPATH=adapters DELANMAR_BRIDGE="$PWD/core/target/debug/delanmar_bridge" python3 -m unittest discover -s adapters/tests -p '*_test.py' -v` | Passed: 18 Python tests, including subprocess termination, EOF, invalid responses, timeout, blocked write, cleanup, concurrency rejection and same-user identity assertion. LangChain and LangGraph checks use stubs, not installed frameworks. |
| `cargo fmt --manifest-path core/Cargo.toml -- --check` | Passed. |
| `git diff --check` | Passed on the committed code revision. |
| `timeout 90s bazel test //core:delanmar_core_test //adapters:bridge_test` | Not verified: Bazel launcher could not resolve/download its `latest` version because DNS for `www.googleapis.com` failed; no Bazel tests ran. |
| CodeQL checker | No Python or Rust alerts; Rust was analyzed before the final Python-only change. |

Review status: Copilot performed code and automated review; a reliability review identified blocked-worker and inconsistent-decision risks, which were addressed. Independent human security reviewer and owner approval remain pending. Framework integrations, hostile-process isolation, authenticated identity, approval and execution enforcement, resource-scoped authorization, and production readiness remain unverified or unimplemented. This is a fail-closed transition, not Phase 1 acceptance.

#### Earlier correction snapshot

On 2026-11-24, the code subsequently committed as `5ef091da7f41ef855dc16b46e4f19f70c725a5d7` was tested in Linux 7.0.0-1017-azure x86_64, Rust/Cargo 1.100.0 and Python 3.12.3. Commands ran from the repository root:

| Command | Result |
|---|---|
| `cargo test --locked --manifest-path core/Cargo.toml` | Passed: 14 Rust unit tests, including malformed contracts, policy validation and synthetic caller mismatch; no binary or doc tests. |
| `cargo build --locked --manifest-path core/Cargo.toml` | Passed. |
| `PYTHONPATH=adapters DELANMAR_BRIDGE="$PWD/core/target/debug/delanmar_bridge" python3 -m unittest discover -s adapters/tests -p '*_test.py' -v` | Passed: 7 tests, including same-user forged launcher and identity claims, malformed requests and synthetic BeeAI seam coverage. |
| `cargo fmt --manifest-path core/Cargo.toml -- --check` | Passed. |
| `git diff --check` | Passed for the then-uncommitted changes. |
| CodeQL checker | No Python or Rust alerts; Rust was analyzed before the final Python-only change. |

Review status: automated analysis and a code review identified a BeeAI seam regression, which was corrected and tested. Independent security approval is pending. These results do not establish authentication, resource-scoped authorization, framework enforcement, or production readiness. No Bazel, Mojo, or actual framework integration tests were run for this correction.

### Historical local verification snapshot

On 2026-11-24, against code at revision `c6905aa`, a Linux environment with Rust/Cargo 1.100.0 and Python 3.12.3 produced the following results (commands are run from the repository root):

| Check | Result |
|---|---|
| `cargo test --locked --manifest-path core/Cargo.toml` | Passed: three Rust unit tests; no binary or doc tests. |
| `cargo build --locked --manifest-path core/Cargo.toml` | Passed: built the Rust bridge. |
| `PYTHONPATH=adapters DELANMAR_BRIDGE="$PWD/core/target/debug/delanmar_bridge" python3 -m unittest discover -s adapters/tests -p '*_test.py' -v` | Passed: three Python bridge tests. Python reported unclosed-file `ResourceWarning`s; process cleanup needs investigation. |
| `bazel --version` | Timed out after 12 seconds; no Bazel build or test was verified. |
| Mojo | `mojo` executable unavailable; no Mojo test was run. |

This snapshot does not verify framework calls, CI, reproducibility, security enforcement, or other environments. See [IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md) and [Phase 1](../phases/PHASE_01_SECURITY_CORE.md) for the remaining work.
