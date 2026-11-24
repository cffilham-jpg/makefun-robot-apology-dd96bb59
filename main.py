#!/usr/bin/env python3
"""Write a two-line robot apology to entry.txt.

Writes the entry to $MAKEFUN_OUTPUT_DIR/entry.txt, or to
/output/entry.txt when the variable is unset. No trailing newline.
"""

import os
import sys
import unicodedata

ENTRY = (
    "I printed two hundred copies of the meeting agenda instead of two "
    "because I typed an extra zero and never checked the number.\n"
    "Now I read the copy count out loud before I press print, "
    "so a typo can't turn into a tower of paper."
)


def validate(text: str) -> None:
    """Reject text that breaks the bounty rules."""
    if not text or not text.strip():
        raise ValueError("entry is empty")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if len(text) > 400:
        raise ValueError("entry is over 400 characters")
    lines = text.split("\n")
    if len(lines) != 2 or not all(line.strip() for line in lines):
        raise ValueError("entry must be exactly two non-empty lines")
    for line in lines:
        for ch in line:
            if unicodedata.category(ch) in ("Cc", "Cf", "Zl", "Zp"):
                raise ValueError(
                    f"entry contains a forbidden character: U+{ord(ch):04X}"
                )


def main() -> int:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    print(f"wrote {path} ({len(ENTRY)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
