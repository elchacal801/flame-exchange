"""
backfill_last_reviewed.py — one-shot backfill of the ``last_reviewed`` field.

Inserts ``last_reviewed: <date>`` into every ThreatPaths/TP-*.md that
lacks it, where <date> is the file's most recent *substantive* commit:
bulk mechanical sweeps (commits modifying more than BULK_THRESHOLD TP
files at once, e.g. the matrix-view frontmatter tagging) are skipped,
because touching 89 files in one commit is metadata mechanics, not an
intelligence review. A commit that *created* the file always counts —
authoring is the floor.

Idempotent: files already carrying ``last_reviewed:`` are skipped.
Pattern follows scripts/tag_short_name.py (anchor-based insert).

Usage:
    python scripts/backfill_last_reviewed.py            # apply
    python scripts/backfill_last_reviewed.py --dry-run  # report only
"""

import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TP_DIR = ROOT / "ThreatPaths"
BULK_THRESHOLD = 20  # commits modifying more TP files than this are mechanical
ANCHOR = "date:"     # insert after the authored date line


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


def tp_touch_counts() -> Counter:
    """Count how many TP files each commit touched."""
    out = _git("log", "--name-only", "--format=%H", "--", "ThreatPaths")
    counts: Counter = Counter()
    current = None
    for line in out.splitlines():
        if re.fullmatch(r"[0-9a-f]{40}", line):
            current = line
        elif line.startswith("ThreatPaths/TP-") and current:
            counts[current] += 1
    return counts


def substantive_date(path: Path, counts: Counter) -> str:
    """Date of the newest non-bulk commit touching *path*.

    Falls back to the file's creation commit if every later commit was a
    bulk sweep.
    """
    rel = path.relative_to(ROOT).as_posix()
    out = _git("log", "--format=%H %as", "--", rel)
    history = [line.split() for line in out.splitlines() if line.strip()]
    for sha, date in history:
        if counts.get(sha, 0) <= BULK_THRESHOLD:
            return date
    # Every commit was bulk (file born in a bulk import): use creation.
    return history[-1][1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    counts = tp_touch_counts()
    changed = skipped = 0
    for path in sorted(TP_DIR.glob("TP-*.md")):
        text = path.read_text(encoding="utf-8")
        if re.search(r"^last_reviewed:", text, re.M):
            skipped += 1
            continue
        date = substantive_date(path, counts)
        new_text, n = re.subn(
            r"^(date:.*)$",
            rf"\1\nlast_reviewed: {date}",
            text,
            count=1,
            flags=re.M,
        )
        if n != 1:
            print(f"  !! no '{ANCHOR}' anchor in {path.name} -- skipped")
            continue
        if args.dry_run:
            print(f"  {path.name}: last_reviewed: {date}")
        else:
            path.write_text(new_text, encoding="utf-8")
        changed += 1

    print(f"{'Would update' if args.dry_run else 'Updated'} {changed} file(s); "
          f"{skipped} already had last_reviewed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
