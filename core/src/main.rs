//! Bridge: one JSON request per stdin line -> one JSON response per stdout line.
use std::io::{self, BufRead, Write};

fn main() {
    let stdout = io::stdout();
    let mut out = stdout.lock();
    for line in io::stdin().lock().lines() {
        let line = line.expect("stdin read failed");
        if line.trim().is_empty() {
            continue;
        }
        writeln!(out, "{}", delanmar_core::handle(&line)).unwrap();
        out.flush().unwrap();
    }
}
