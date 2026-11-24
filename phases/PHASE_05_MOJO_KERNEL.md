# Phase 05 — Mojo Compute Kernel

**Status:** Initial analytics example exists; toolchain and interoperability are unverified.

## Objective and scope
Verify a justified compute workload and a supported interface while keeping security authority in Rust.

## Existing components to reuse
`mojo/metrics.mojo`, `mojo/run_mojo.sh`, its Bazel shell target, and the constitution's compute responsibilities.

## Required work
- Select and document a supported Mojo toolchain and a bounded compute task with measurable correctness requirements.
- Define data ownership, validated inputs/outputs, error handling and an interoperable Rust interface; avoid granting compute code policy authority.
- Implement and document the workload and integration path, with performance claims only where measured.

## Dependencies
Phase 1 baseline; coordinate interface and governance with Phases 2–4 and build support with Phase 6. This work can proceed in parallel where interfaces permit.

## Testing requirements
Test reference results, invalid and boundary inputs, Rust interoperability, toolchain reproducibility and failure propagation. Report an unavailable or skipped Mojo test separately from a pass.

## Acceptance criteria
- The selected workload produces verified results through a documented Rust interoperability path.
- Supported toolchain, build, tests and limitations are reproducible; benchmark claims have evidence if made.

## Outstanding risks
Toolchain churn, platform support, unsafe boundaries, unverified performance benefit and accidental authority leakage.

## Handoff
Provide the verified compute interface to Phase 6 and to any later workload that actually requires it.
