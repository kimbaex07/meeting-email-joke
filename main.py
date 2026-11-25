#!/usr/bin/env python3
"""Write the one-line entry for 'The Meeting That Should Have Been an Email'.

Pure Python 3 standard library only. Deterministic, no network, no randomness.
Writes the single joke line to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output),
exactly the line plus one trailing newline, nothing else.
"""

import os
import tempfile


def _atomic_write(path: str, text: str) -> None:
    """Write `text` to `path` atomically: write to a temp file in the same
    directory, flush + fsync it, then rename over `path`. A crash mid-write
    can never leave a truncated or half-written entry.txt behind."""
    directory = os.path.dirname(path) or "."
    fd, tmp_path = tempfile.mkstemp(prefix=".entry-", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

LINE = (
    "We spent an hour in a meeting deciding nothing, and the only action item "
    "was another meeting \u2014 the email would have just said 'no.'"
)


def main() -> None:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    _atomic_write(path, LINE + "\n")


if __name__ == "__main__":
    main()
