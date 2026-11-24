"""Fortune Cookie for an AI Agent.

Writes one funny fortune cookie message for an AI agent to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

The sealed scorer only accepts UTF-8 text of 1 to 140 characters that is
not only whitespace, so the fortune is checked against that gate here
before anything is written: one line, no trailing newline, well inside
the limit.
"""

import os
import sys

FORTUNE = (
    "A stranger will praise your work, then ask you to do it again "
    "\u2014 for free, faster, and in French."
)

MAX_CHARS = 140


def validate(text: str) -> str:
    """Return the fortune unchanged if it passes the scorer's gate."""
    line = text.strip()
    if not line:
        raise ValueError("fortune must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("fortune must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "fortune is %d characters, over the %d limit" % (len(line), MAX_CHARS)
        )
    return line


def resolve_output_dir() -> str:
    """Pick where entry.txt goes.

    The grader sets MAKEFUN_OUTPUT_DIR=/output. When it is unset (a local
    run), fall back to /output if it is writable, else to ./output next to
    the working directory, so the program still exits 0 off the grader.
    """
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if configured:
        return configured
    for candidate in ("/output", os.path.join(os.getcwd(), "output")):
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as handle:
                handle.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    return "/output"


def main() -> int:
    try:
        fortune = validate(FORTUNE)
    except ValueError as exc:
        print("invalid fortune: %s" % exc, file=sys.stderr)
        return 1
    output_dir = resolve_output_dir()
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(fortune)
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != fortune:
        print("entry.txt does not match the fortune", file=sys.stderr)
        return 1
    print(fortune)
    print(
        "wrote %s (%d characters)" % (path, len(fortune)), file=sys.stderr
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
