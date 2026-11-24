# Architecture

Assumption: "bazal" means **Bazel**.

| Layer | Language | Role |
|---|---|---|
| `core/` | Rust | 24-agent roster and human-approval policy (blueprint §8); JSON-lines bridge binary |
| `mojo/` | Mojo | Numeric/analytics kernels (pilot metrics) |
| `adapters/` | Python | LangChain, LangGraph, CrewAI, BeeAI adapters |
| Root | Bazel | Builds, tests, and wires all languages |

Non-Rust/Mojo languages never touch each other directly: Bazel builds `//core:delanmar_bridge`, and adapters reach it only through the JSON-lines contract (`{"op":"list_agents"}`, `{"op":"check_action","agent":..,"action":..}`) via `adapters/delanmar_adapters/bridge.py`. Anything not on the routine-action allowlist returns `requires_human_approval`.

## Status (verified vs. not)

- Verified: Rust core unit tests and bridge via `cargo test` / `cargo run` in `core/`.
- Not verified: Bazel files (no Bazel in dev environment; rule versions and `Cargo.lock` need generating), Python adapter tests, the Mojo kernel (no Mojo toolchain), and all LangChain/LangGraph/CrewAI/BeeAI calls (frameworks not installed or version-pinned; BeeAI is only a documented seam).
