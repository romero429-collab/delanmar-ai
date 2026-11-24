"""Pilot metric: percent change versus baseline (docs: OpenWorks pilot setup, section 6).
Mojo owns numeric/analytics kernels. Not yet built or run: no Mojo toolchain in the dev environment."""


fn percent_change(baseline: Float64, current: Float64) raises -> Float64:
    if baseline == 0.0:
        raise Error("baseline must be non-zero")
    return (current - baseline) / baseline * 100.0


fn main() raises:
    print(percent_change(10.0, 7.5))  # -25.0
