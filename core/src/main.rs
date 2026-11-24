//! Bridge: one JSON request per stdin line -> one JSON response per stdout line.
//!
//! No trusted launcher is implemented; all requests are denied.
use delanmar_core::{AuthError, Core, PolicyTable};
use std::io::{self, BufRead, Read, Write};

// Includes the trailing newline, if present, matching the Python client limit.
const MAX_LINE_BYTES: u64 = 65_536;

fn main() {
    let core = Core::new(
        Err(AuthError::Unavailable(
            "trusted launcher not implemented".into(),
        )),
        Ok(PolicyTable::production()),
    );
    let stdout = io::stdout();
    let mut out = stdout.lock();
    let stdin = io::stdin();
    let mut input = stdin.lock();
    loop {
        let mut line = Vec::new();
        let read = input
            .by_ref()
            .take(MAX_LINE_BYTES + 1)
            .read_until(b'\n', &mut line);
        let Ok(size) = read else { break };
        if size == 0 {
            break;
        }
        if size as u64 > MAX_LINE_BYTES {
            let _ = writeln!(out, "{}", Core::reject_oversized_request());
            let _ = out.flush();
            break;
        }
        let Ok(line) = std::str::from_utf8(&line) else {
            if writeln!(out, "{}", core.handle("{")).is_err() || out.flush().is_err() {
                break;
            }
            continue;
        };
        if line.trim().is_empty() {
            continue;
        }
        if writeln!(out, "{}", core.handle(line)).is_err() || out.flush().is_err() {
            break;
        }
    }
}
