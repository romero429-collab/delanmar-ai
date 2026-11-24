//! Bridge: one JSON request per stdin line -> one JSON response per stdout line.
//!
//! The caller identity is established from a binding the trusted launcher writes to a
//! private inherited descriptor (`--caller-fd N`), never from request content or the
//! environment. Without a valid binding every request is denied.
use delanmar_core::{authenticate_binding, AuthError, Core, PolicyTable};
use std::io::{self, BufRead, Write};

#[cfg(unix)]
fn caller() -> Result<delanmar_core::Principal, AuthError> {
    use std::os::fd::FromRawFd;
    let mut args = std::env::args().skip(1);
    let fd: i32 = match (args.next().as_deref(), args.next()) {
        (Some("--caller-fd"), Some(n)) => n
            .parse()
            .map_err(|_| AuthError::Unavailable("invalid --caller-fd".into()))?,
        _ => return Err(AuthError::Unavailable("missing --caller-fd".into())),
    };
    if fd < 3 {
        return Err(AuthError::Unavailable("caller fd must be >= 3".into()));
    }
    // SAFETY: the trusted launcher hands this descriptor to us; we take sole ownership.
    let file = unsafe { std::fs::File::from_raw_fd(fd) };
    authenticate_binding(file)
}

#[cfg(not(unix))]
fn caller() -> Result<delanmar_core::Principal, AuthError> {
    Err(AuthError::Unavailable("caller authentication unsupported on this platform".into()))
}

fn main() {
    let core = Core::new(caller(), Ok(PolicyTable::production()));
    let stdout = io::stdout();
    let mut out = stdout.lock();
    for line in io::stdin().lock().lines() {
        let line = line.expect("stdin read failed");
        if line.trim().is_empty() {
            continue;
        }
        writeln!(out, "{}", core.handle(&line)).unwrap();
        out.flush().unwrap();
    }
}
