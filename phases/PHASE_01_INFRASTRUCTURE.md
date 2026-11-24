# Phase 01 — Development Infrastructure

**Status:** Partially established; baseline and reproducibility remain to be verified.

## Objective and scope
Establish and record a repeatable development environment, dependency inventory, CI and verification baseline for existing components.

## Existing components to reuse
`core/Cargo.toml` and `Cargo.lock`, `MODULE.bazel`, component `BUILD.bazel` files, existing Rust and Python tests, `mojo/run_mojo.sh`, and [implementation status](../docs/ARCHITECTURE.md).

## Required work
- Inventory supported platforms, toolchain versions, dependency sources and installation prerequisites; identify missing or unpinned tools.
- Run existing Rust, Python bridge, Mojo and Bazel checks where prerequisites are available; record exact commands, revision, environment, outcomes and blockers.
- Define reproducible setup, dependency management, CI and security checks without claiming unavailable or skipped checks pass.
- Document ownership and a process for updating verification evidence as components change.

## Dependencies
Phase 0 authority. Phase 6 builds on this baseline to establish the final supported Bazel targets; Phase 1 does not depend on Phase 6 being complete.

## Testing requirements
Run the existing tests and builds in a clean environment and repeat the documented setup independently; exercise CI on a representative change.

## Acceptance criteria
- A new contributor can reproduce the documented supported environment and checks.
- Results, missing toolchains, unverified framework integrations and remediation owners are recorded; CI reports failures and skips distinctly.
- Required dependencies and versions are documented with a maintenance and security review process.

## Outstanding risks
Toolchain availability, network or platform differences, unpinned framework packages, and false confidence from skipped tests.

## Handoff
Provide a trustworthy baseline to Phases 2–7 and outstanding gaps to Phase 6.
