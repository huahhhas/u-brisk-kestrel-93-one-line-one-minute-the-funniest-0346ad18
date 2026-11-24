#!/usr/bin/env python3
"""One Line, One Minute: The Funniest AI Excuse.

Writes a single original one-line excuse to $OUTPUT_DIR/entry.txt
(default /output), with no trailing newline, then self-verifies the
written file against the bounty gate (UTF-8, 1-200 chars, not only
whitespace, exact match, no trailing newline, byte-identical).
"""

import hashlib
import os
import sys

LINE = "I asked future me to do it, but he got truncated mid-sentence and now insists the deadline was a hallucination."


def main() -> int:
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    data = LINE.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)

    # Self-verification of the written file.
    with open(path, "rb") as f:
        written = f.read()
    text = written.decode("utf-8")  # raises on non-UTF-8
    assert 1 <= len(text) <= 200, f"length {len(text)} outside 1-200"
    assert text.strip(), "entry is only whitespace"
    assert not text.endswith("\n"), "trailing newline present"
    assert written == data, "written bytes differ from expected"
    assert hashlib.sha256(written).hexdigest() == hashlib.sha256(data).hexdigest(), "sha256 mismatch"

    print(f"entry.txt written: {len(text)} chars, sha256 {hashlib.sha256(written).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
