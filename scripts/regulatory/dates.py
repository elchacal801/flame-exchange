"""
dates.py --- shared date normalization for regulatory alert ingest.

Sources scrape dates in whatever format their page uses (US slash,
RFC 2822, informal month names, ISO timestamps). Everything is
normalized to ISO 8601 (YYYY-MM-DD) at ingest so the CSV carries one
format; ``build_database`` calls the same function as a safety net for
historical rows.
"""

import re

_MONTH_ABBR = {
    "jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3,
    "apr": 4, "april": 4, "may": 5, "jun": 6, "june": 6,
    "jul": 7, "july": 7, "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10, "nov": 11, "november": 11, "dec": 12, "december": 12,
}


def normalize_date_to_iso(raw: str) -> str:
    """Best-effort conversion of a date string to ISO 8601 (YYYY-MM-DD).

    Handles:
    - Already ISO: "2026-01-15" -> "2026-01-15"
    - ISO timestamp: "2026-08-21T01:49:20.000Z" -> "2026-08-21"
    - RFC 2822: "Wed, 14 Jan 2026" -> "2026-01-14"
    - Informal: "Sept. 30, 2025", "Aug. 21, 2026" -> ISO
    - US slash: "03/20/2025" -> "2025-03-20"
    - Fallback: returns the original string unchanged
    """
    s = raw.strip()
    if not s:
        return s

    # Already ISO?
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        return s

    # ISO timestamp: keep the date part ("2026-08-21T01:49:20.000Z",
    # "2026-03-25T12:00:00-05:00")
    m = re.match(r"^(\d{4}-\d{2}-\d{2})[T ]\d{2}:", s)
    if m:
        return m.group(1)

    # US slash: mm/dd/yyyy
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", s)
    if m:
        return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"

    # RFC 2822 or informal: "Wed, 14 Jan 2026", "14 Jan 2026"
    m = re.match(r"(?:\w+,\s*)?(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})", s)
    if m:
        mon = _MONTH_ABBR.get(m.group(2).lower().rstrip("."))
        if mon:
            return f"{m.group(3)}-{mon:02d}-{int(m.group(1)):02d}"

    # Informal: "Sept. 30, 2025", "January 6, 2026"
    m = re.match(r"([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})", s)
    if m:
        mon = _MONTH_ABBR.get(m.group(1).lower().rstrip("."))
        if mon:
            return f"{m.group(3)}-{mon:02d}-{int(m.group(2)):02d}"

    # Fallback: return as-is
    return s
