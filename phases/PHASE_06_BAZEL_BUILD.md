# Phase 06 — Bazel Build System

**Status:** Workspace and targets exist; rule versions and builds are unverified.

## Objective and scope
Make Bazel the reproducible build and test path for supported components, not a runtime message transport.

## Existing components to reuse
`MODULE.bazel`, `core/BUILD.bazel`, `adapters/BUILD.bazel`, `mojo/BUILD.bazel`, Cargo manifests and lockfile.

## Required work
- Validate and pin supported rules, toolchains and dependencies; document platform and external prerequisites.
- Establish Rust, Python and supported Mojo targets and cross-language integration tests, with explicit handling of optional toolchains.
- Make builds and tests reproducible in clean local and CI environments; document cache and dependency update policy.
- Resolve discrepancies between direct component checks and Bazel targets.

## Dependencies
Phase 1 toolchain baseline; coordinate evolving interfaces with Phases 2–5. It can progress in parallel with implementation.

## Testing requirements
Run supported build and test targets from clean environments, including bridge integration; verify missing tools and skipped optional checks are clearly reported. Repeat builds and compare relevant outputs.

## Acceptance criteria
- Documented supported components build and test through Bazel in local and CI environments with pinned, reviewable dependencies.
- Reproducibility evidence and any platform or toolchain exclusions are recorded; skips are not counted as passes.

## Outstanding risks
Rule incompatibility, dependency drift, non-hermetic toolchains and Mojo availability.

## Handoff
Provide the supported build/test gate for adapters, Alpha and later deployments.
