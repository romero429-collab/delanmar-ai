//! Bridge: one JSON request per stdin line -> one JSON response per stdout line.
//!
//! No trusted launcher is implemented; all requests are denied.
use delanmar_core::{AuthError, Core, PolicyTable};
use std::io::{self, BufRead, Write};

fn main() {
    let core = Core::new(
        Err(AuthError::Unavailable("trusted launcher not implemented".into())),
        Ok(PolicyTable::production()),
    );
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
