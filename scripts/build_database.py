#!/usr/bin/env python3
"""
build_database.py - FLAME Database Builder

Parses markdown threat path files, extracts YAML frontmatter,
builds a SQLite index database and exports a JSON data file
for the static frontend.

Usage:
    python scripts/build_database.py [--root /path/to/flame-fraud]

The script scans ThreatPaths/ and Baselines/
directories for markdown files, parses their YAML frontmatter
(code-fenced blocks), and produces:
    - database/flame.db    (SQLite index)
    - database/flame-data.json (flat JSON for frontend)
"""

import argparse
import csv
import json
import logging
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from email.utils import format_datetime as _format_rfc822
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from regulatory.dates import normalize_date_to_iso  # noqa: E402

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
log = logging.getLogger("build_database")

# ---------------------------------------------------------------------------
# Frontmatter extraction
# ---------------------------------------------------------------------------

# Matches code-fenced YAML blocks: ```yaml ... ``` with --- delimiters inside
FRONTMATTER_PATTERN = re.compile(
    r"```ya?ml\s*\n---\s*\n(.*?)\n---\s*\n```",
    re.DOTALL
)


def extract_frontmatter(filepath: Path) -> dict | None:
    """Extract YAML frontmatter from a markdown file.

    Supports the FLAME convention where frontmatter is wrapped in
    a code-fenced yaml block with --- delimiters.
    """
    text = filepath.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.search(text)
    if not match:
        log.warning("No frontmatter found in %s", filepath)
        return None

    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        log.error("YAML parse error in %s: %s", filepath, e)
        return None

    if not isinstance(data, dict):
        log.warning("Frontmatter in %s is not a mapping", filepath)
        return None

    return data


def extract_body(filepath: Path) -> str:
    """Extract the body content after the frontmatter block."""
    text = filepath.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.search(text)
    if match:
        # Everything after the closing ``` of the frontmatter
        end = text.find("```", match.end() - 3) + 3
        body = text[end:].strip()
    else:
        body = text.strip()
    return body


def extract_summary(body: str) -> str:
    """Extract the Summary section content from the body."""
    lines = body.split("\n")
    capture = False
    summary_lines = []
    for line in lines:
        if re.match(r"^##\s+Summary", line):
            capture = True
            continue
        if capture:
            if re.match(r"^##\s+", line):
                break
            summary_lines.append(line)
    return "\n".join(summary_lines).strip()


# Evidence ID pattern: ### EV-TPXXXX-YYYY-NNN: Title
EVIDENCE_HEADER = re.compile(r"^###\s+(EV-[A-Z0-9-]+):\s+(.+)$")
# Field patterns: - **Field**: Value
EVIDENCE_FIELD = re.compile(r"^-\s+\*\*(.+?)\*\*:\s+(.+)$")


def extract_evidence(body: str) -> list[dict]:
    """Extract Operational Evidence entries from the body.

    Parses the ## Operational Evidence section for structured evidence
    entries identified by ### EV-* headers with bullet-point fields.
    """
    lines = body.split("\n")
    in_section = False
    entries = []
    current = None

    for line in lines:
        stripped = line.strip()

        # Detect entering the Operational Evidence section
        if re.match(r"^##\s+Operational Evidence", stripped):
            in_section = True
            continue

        # Detect leaving the section (next ## heading)
        if in_section and re.match(r"^##\s+", stripped) and not re.match(r"^###", stripped):
            if current:
                entries.append(current)
                current = None
            break

        if not in_section:
            continue

        # Check for evidence entry header
        header_match = EVIDENCE_HEADER.match(stripped)
        if header_match:
            if current:
                entries.append(current)
            current = {
                "evidence_id": header_match.group(1),
                "title": header_match.group(2),
            }
            continue

        # Check for field within current entry
        if current:
            field_match = EVIDENCE_FIELD.match(stripped)
            if field_match:
                key = field_match.group(1).lower().replace(" ", "_")
                current[key] = field_match.group(2)

    # Capture final entry if section ends without a ## boundary
    if current:
        entries.append(current)

    return entries


# ---------------------------------------------------------------------------
# Database schema
# ---------------------------------------------------------------------------

SCHEMA = """
CREATE TABLE IF NOT EXISTS submissions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    date TEXT,
    author TEXT,
    source TEXT,
    tlp TEXT DEFAULT 'WHITE',
    summary TEXT,
    body TEXT,
    file_path TEXT NOT NULL,
    confidence_score INTEGER,
    source_reliability TEXT,
    info_credibility INTEGER,
    infrastructure_generation_method TEXT,
    geopolitical_timing TEXT,
    nation_state_nexus TEXT,
    fraud_family TEXT,
    primary_phase TEXT,
    short_name TEXT
);

CREATE TABLE IF NOT EXISTS submission_sectors (
    submission_id TEXT NOT NULL,
    sector TEXT NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submissions(id)
);

CREATE TABLE IF NOT EXISTS submission_fraud_types (
    submission_id TEXT NOT NULL,
    fraud_type TEXT NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submissions(id)
);

CREATE TABLE IF NOT EXISTS submission_tags (
    submission_id TEXT NOT NULL,
    tag TEXT NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submissions(id)
);

CREATE TABLE IF NOT EXISTS submission_cfpf_phases (
    submission_id TEXT NOT NULL,
    phase TEXT NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submissions(id)
);

CREATE TABLE IF NOT EXISTS submission_mitre_attack (
    submission_id TEXT NOT NULL,
    technique_id TEXT NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submissions(id)
);

CREATE TABLE IF NOT EXISTS submission_ft3_tactics (
    submission_id TEXT NOT NULL,
    tactic_id TEXT NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submissions(id)
);

CREATE TABLE IF NOT EXISTS submission_mitre_f3 (
    submission_id TEXT NOT NULL,
    technique_id TEXT NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submissions(id)
);

CREATE TABLE IF NOT EXISTS submission_groupib_stages (
    submission_id TEXT NOT NULL,
    stage TEXT NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submissions(id)
);

CREATE TABLE IF NOT EXISTS submission_regulatory_refs (
    submission_id TEXT NOT NULL,
    reg_id TEXT NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submissions(id)
);
CREATE INDEX IF NOT EXISTS idx_regulatory_refs ON submission_regulatory_refs(reg_id);

CREATE TABLE IF NOT EXISTS techniques (
    id TEXT PRIMARY KEY,
    phase TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    indicators TEXT,
    mitre_attack TEXT,
    fraud_types TEXT
);

CREATE INDEX IF NOT EXISTS idx_infra_gen ON submissions(infrastructure_generation_method);
CREATE INDEX IF NOT EXISTS idx_geo_timing ON submissions(geopolitical_timing);
CREATE INDEX IF NOT EXISTS idx_ns_nexus ON submissions(nation_state_nexus);
CREATE INDEX IF NOT EXISTS idx_fraud_family ON submissions(fraud_family);
CREATE INDEX IF NOT EXISTS idx_primary_phase ON submissions(primary_phase);
CREATE INDEX IF NOT EXISTS idx_sectors ON submission_sectors(sector);
CREATE INDEX IF NOT EXISTS idx_fraud_types ON submission_fraud_types(fraud_type);
CREATE INDEX IF NOT EXISTS idx_cfpf ON submission_cfpf_phases(phase);
CREATE INDEX IF NOT EXISTS idx_tags ON submission_tags(tag);

CREATE TABLE IF NOT EXISTS regulatory_alerts (
    alert_id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    date TEXT,
    category TEXT,
    severity TEXT,
    url TEXT,
    summary TEXT
);

CREATE TABLE IF NOT EXISTS regulatory_alert_tp_mapping (
    alert_id TEXT NOT NULL,
    tp_id TEXT NOT NULL,
    FOREIGN KEY (alert_id) REFERENCES regulatory_alerts(alert_id)
);

CREATE TABLE IF NOT EXISTS submission_ucff_domains (
    submission_id TEXT NOT NULL,
    domains_json TEXT NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submissions(id)
);

CREATE TABLE IF NOT EXISTS submission_baseline_ids (
    submission_id TEXT NOT NULL,
    baseline_id TEXT NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submissions(id)
);

CREATE TABLE IF NOT EXISTS submission_related_tps (
    submission_id TEXT NOT NULL,
    related_tp_id TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submissions(id)
);

CREATE INDEX IF NOT EXISTS idx_baseline_ids ON submission_baseline_ids(baseline_id);
CREATE INDEX IF NOT EXISTS idx_related_tps ON submission_related_tps(related_tp_id);
CREATE INDEX IF NOT EXISTS idx_reg_source ON regulatory_alerts(source);
CREATE INDEX IF NOT EXISTS idx_reg_date ON regulatory_alerts(date);
CREATE INDEX IF NOT EXISTS idx_reg_tp ON regulatory_alert_tp_mapping(tp_id);

"""


def init_database(db_path: Path) -> sqlite3.Connection:
    """Create or recreate the database with the schema."""
    if db_path.exists():
        db_path.unlink()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_submission(conn: sqlite3.Connection, meta: dict, body: str, summary: str, filepath: Path):
    """Insert a single submission and its related data into the database."""
    sub_id = meta.get("id", "")
    if not sub_id:
        log.warning("Skipping %s: no 'id' in frontmatter", filepath)
        return

    conn.execute(
        """INSERT OR REPLACE INTO submissions
           (id, title, category, date, author, source, tlp, summary, body, file_path,
            confidence_score, source_reliability, info_credibility,
            infrastructure_generation_method, geopolitical_timing, nation_state_nexus,
            fraud_family, primary_phase, short_name)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            sub_id,
            meta.get("title", ""),
            meta.get("category", ""),
            str(meta.get("date", "")),
            meta.get("author", ""),
            meta.get("source", ""),
            meta.get("tlp", "WHITE"),
            summary,
            body,
            str(filepath),
            meta.get("confidence_score"),
            meta.get("source_reliability"),
            meta.get("info_credibility"),
            meta.get("infrastructure_generation_method"),
            meta.get("geopolitical_timing"),
            meta.get("nation_state_nexus"),
            meta.get("fraud_family"),
            meta.get("primary_phase"),
            meta.get("short_name"),
        )
    )

    # Multi-value fields
    _insert_multi(conn, "submission_sectors", sub_id, "sector", meta.get("sector", []))
    _insert_multi(conn, "submission_fraud_types", sub_id, "fraud_type", meta.get("fraud_types", []))
    _insert_multi(conn, "submission_tags", sub_id, "tag", meta.get("tags", []))
    _insert_multi(conn, "submission_cfpf_phases", sub_id, "phase", meta.get("cfpf_phases", []))
    _insert_multi(conn, "submission_mitre_attack", sub_id, "technique_id", meta.get("mitre_attack", []))
    _insert_multi(conn, "submission_ft3_tactics", sub_id, "tactic_id", meta.get("ft3_tactics", []))
    _insert_multi(conn, "submission_mitre_f3", sub_id, "technique_id", meta.get("mitre_f3", []))
    _insert_multi(conn, "submission_groupib_stages", sub_id, "stage", meta.get("groupib_stages", []))
    _insert_multi(conn, "submission_regulatory_refs", sub_id, "reg_id", meta.get("regulatory_refs", []))

    # UCFF domains — stored as JSON object (not multi-value array)
    ucff = meta.get("ucff_domains")
    if ucff and isinstance(ucff, dict):
        conn.execute(
            "INSERT OR REPLACE INTO submission_ucff_domains (submission_id, domains_json) VALUES (?, ?)",
            (sub_id, json.dumps(ucff))
        )

    # Baseline IDs — link TPs to applicable baselines
    baseline_ids = meta.get("baseline_ids")
    if baseline_ids and isinstance(baseline_ids, list):
        for bl_id in baseline_ids:
            if bl_id:
                conn.execute(
                    "INSERT INTO submission_baseline_ids (submission_id, baseline_id) VALUES (?, ?)",
                    (sub_id, str(bl_id))
                )

    # Related TPs — typed cross-references
    related_tps = meta.get("related_tps")
    if related_tps and isinstance(related_tps, list):
        for rel in related_tps:
            if isinstance(rel, dict) and rel.get("id") and rel.get("relationship"):
                conn.execute(
                    "INSERT INTO submission_related_tps (submission_id, related_tp_id, relationship_type) VALUES (?, ?, ?)",
                    (sub_id, str(rel["id"]), str(rel["relationship"]))
                )


# Whitelist of valid (table, column) pairs for multi-value operations.
# Prevents SQL injection if table/col ever comes from untrusted input.
_VALID_MULTI_TABLES = {
    ("submission_sectors", "sector"),
    ("submission_fraud_types", "fraud_type"),
    ("submission_tags", "tag"),
    ("submission_cfpf_phases", "phase"),
    ("submission_mitre_attack", "technique_id"),
    ("submission_ft3_tactics", "tactic_id"),
    ("submission_mitre_f3", "technique_id"),
    ("submission_groupib_stages", "stage"),
    ("submission_regulatory_refs", "reg_id"),
    ("submission_baseline_ids", "baseline_id"),
}


def _insert_multi(conn: sqlite3.Connection, table: str, sub_id: str, col: str, values):
    """Insert multi-value list entries for a submission."""
    if (table, col) not in _VALID_MULTI_TABLES:
        raise ValueError(f"Invalid table/column pair: {table}.{col}")
    if not values or not isinstance(values, list):
        return
    for val in values:
        if val:  # skip empty strings/None
            conn.execute(
                f"INSERT INTO {table} (submission_id, {col}) VALUES (?, ?)",  # nosec B608
                (sub_id, str(val))
            )


def load_techniques(conn: sqlite3.Connection, techniques_path: Path):
    """Load CFPF techniques from cfpf_techniques.json."""
    if not techniques_path.exists():
        log.warning("cfpf_techniques.json not found at %s", techniques_path)
        return 0

    data = json.loads(techniques_path.read_text(encoding="utf-8"))
    count = 0
    phases = data.get("phases", {})
    for phase_id, phase_data in phases.items():
        for tech in phase_data.get("techniques", []):
            conn.execute(
                """INSERT OR REPLACE INTO techniques
                   (id, phase, name, description, indicators, mitre_attack, fraud_types)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    tech["id"],
                    phase_id,
                    tech["name"],
                    tech.get("description", ""),
                    json.dumps(tech.get("indicators", [])),
                    json.dumps(tech.get("mitre_attack", [])),
                    json.dumps(tech.get("fraud_types", [])),
                )
            )
            count += 1
    return count


# Detection rule ingestion removed — see github.com/elchacal801/flame-detections


# ---------------------------------------------------------------------------
# Regulatory alerts
# ---------------------------------------------------------------------------

# Month abbreviations (including informal ones like "Sept." used by some sources)
def build_regulatory_alerts(conn: sqlite3.Connection, csv_path: Path) -> int:
    """Ingest regulatory alerts from a CSV file into the database.

    Returns the number of alerts inserted.  If the CSV does not exist,
    logs a warning and returns 0.
    """
    if not csv_path.exists():
        log.warning("Regulatory alerts CSV not found at %s", csv_path)
        return 0

    # Clear previous mappings so re-runs are idempotent
    conn.execute("DELETE FROM regulatory_alert_tp_mapping")

    count = 0
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            alert_id = row.get("alert_id", "").strip()
            if not alert_id:
                continue

            conn.execute(
                """INSERT OR REPLACE INTO regulatory_alerts
                   (alert_id, source, title, date, category, severity, url, summary)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    alert_id,
                    row.get("source", "").strip(),
                    row.get("title", "").strip(),
                    normalize_date_to_iso(row.get("date", "")),
                    row.get("category", "").strip(),
                    row.get("severity", "").strip(),
                    row.get("url", "").strip(),
                    row.get("summary", "").strip(),
                ),
            )

            # Split mapped_tp_ids on | and insert each mapping
            tp_ids_raw = row.get("mapped_tp_ids", "").strip()
            if tp_ids_raw:
                for tp_id in tp_ids_raw.split("|"):
                    tp_id = tp_id.strip()
                    if tp_id:
                        conn.execute(
                            "INSERT INTO regulatory_alert_tp_mapping (alert_id, tp_id) VALUES (?, ?)",
                            (alert_id, tp_id),
                        )

            count += 1

    conn.commit()
    return count


def export_regulatory_json(conn: sqlite3.Connection, output_path: Path) -> int:
    """Export regulatory alerts as a JSON file.

    Returns the number of alerts exported.
    """
    cursor = conn.execute(
        "SELECT alert_id, source, title, date, category, severity, url, summary "
        "FROM regulatory_alerts ORDER BY date DESC"
    )
    columns = [desc[0] for desc in cursor.description]
    alerts = []

    for row in cursor.fetchall():
        entry = dict(zip(columns, row))
        # Fetch TP mappings for this alert
        tp_rows = conn.execute(
            "SELECT tp_id FROM regulatory_alert_tp_mapping WHERE alert_id = ? ORDER BY tp_id",
            (entry["alert_id"],),
        ).fetchall()
        entry["mapped_tp_ids"] = [r[0] for r in tp_rows]
        alerts.append(entry)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(alerts, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return len(alerts)


# ---------------------------------------------------------------------------
# JSON export
# ---------------------------------------------------------------------------

def export_json(conn: sqlite3.Connection, output_path: Path):
    """Export the database to a flat JSON array for the frontend."""
    cursor = conn.execute("SELECT * FROM submissions WHERE lower(category) = 'threatpath' ORDER BY id")
    columns = [desc[0] for desc in cursor.description]
    submissions = []

    for row in cursor.fetchall():
        entry = dict(zip(columns, row))
        sub_id = entry["id"]

        # Attach multi-value lists
        entry["sectors"] = _fetch_list(conn, "submission_sectors", "sector", sub_id)
        entry["fraud_types"] = _fetch_list(conn, "submission_fraud_types", "fraud_type", sub_id)
        entry["tags"] = _fetch_list(conn, "submission_tags", "tag", sub_id)
        entry["cfpf_phases"] = _fetch_list(conn, "submission_cfpf_phases", "phase", sub_id)
        entry["mitre_attack"] = _fetch_list(conn, "submission_mitre_attack", "technique_id", sub_id)
        entry["ft3_tactics"] = _fetch_list(conn, "submission_ft3_tactics", "tactic_id", sub_id)
        entry["mitre_f3"] = _fetch_list(conn, "submission_mitre_f3", "technique_id", sub_id)
        entry["groupib_stages"] = _fetch_list(conn, "submission_groupib_stages", "stage", sub_id)
        entry["regulatory_refs"] = _fetch_list(conn, "submission_regulatory_refs", "reg_id", sub_id)

        # UCFF domains (object, not array)
        ucff_row = conn.execute(
            "SELECT domains_json FROM submission_ucff_domains WHERE submission_id = ?",
            (sub_id,)
        ).fetchone()
        entry["ucff_domains"] = json.loads(ucff_row[0]) if ucff_row else {}

        # Remove full body from JSON export (too large for frontend)
        entry.pop("body", None)

        submissions.append(entry)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(submissions, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    return len(submissions)


def _fetch_list(conn: sqlite3.Connection, table: str, col: str, sub_id: str) -> list:
    """Fetch a list of values from a multi-value table."""
    if (table, col) not in _VALID_MULTI_TABLES:
        raise ValueError(f"Invalid table/column pair: {table}.{col}")
    rows = conn.execute(
        f"SELECT {col} FROM {table} WHERE submission_id = ? ORDER BY rowid",  # nosec B608
        (sub_id,)
    ).fetchall()
    return [r[0] for r in rows]



def _build_full_entry(conn: sqlite3.Connection, entry: dict) -> dict:
    """Attach all multi-value lists to a submission entry dict."""
    sub_id = entry["id"]
    entry["sectors"] = _fetch_list(conn, "submission_sectors", "sector", sub_id)
    entry["fraud_types"] = _fetch_list(conn, "submission_fraud_types", "fraud_type", sub_id)
    entry["tags"] = _fetch_list(conn, "submission_tags", "tag", sub_id)
    entry["cfpf_phases"] = _fetch_list(conn, "submission_cfpf_phases", "phase", sub_id)
    entry["mitre_attack"] = _fetch_list(conn, "submission_mitre_attack", "technique_id", sub_id)
    entry["ft3_tactics"] = _fetch_list(conn, "submission_ft3_tactics", "tactic_id", sub_id)
    entry["mitre_f3"] = _fetch_list(conn, "submission_mitre_f3", "technique_id", sub_id)
    entry["groupib_stages"] = _fetch_list(conn, "submission_groupib_stages", "stage", sub_id)
    entry["regulatory_refs"] = _fetch_list(conn, "submission_regulatory_refs", "reg_id", sub_id)

    # UCFF domains (object, not array)
    ucff_row = conn.execute(
        "SELECT domains_json FROM submission_ucff_domains WHERE submission_id = ?",
        (sub_id,)
    ).fetchone()
    entry["ucff_domains"] = json.loads(ucff_row[0]) if ucff_row else {}

    # Baseline IDs
    entry["baseline_ids"] = _fetch_list(conn, "submission_baseline_ids", "baseline_id", sub_id)

    # Related TPs — typed cross-references
    related_rows = conn.execute(
        "SELECT related_tp_id, relationship_type FROM submission_related_tps WHERE submission_id = ? ORDER BY related_tp_id",
        (sub_id,)
    ).fetchall()
    entry["related_tps"] = [{"id": r[0], "relationship": r[1]} for r in related_rows]

    return entry


def export_index_json(conn: sqlite3.Connection, output_path: Path,
                      evidence_map: dict | None = None):
    """Export metadata-only index for fast frontend initial load."""
    cursor = conn.execute("SELECT * FROM submissions WHERE lower(category) = 'threatpath' ORDER BY id")
    columns = [desc[0] for desc in cursor.description]
    index_entries = []

    if evidence_map is None:
        evidence_map = {}

    for row in cursor.fetchall():
        entry = dict(zip(columns, row))
        entry = _build_full_entry(conn, entry)

        # Truncate summary for index (first 200 chars)
        full_summary = entry.get("summary", "")
        entry["summary"] = full_summary[:200] + ("..." if len(full_summary) > 200 else "")

        # Add evidence count
        sub_id = entry["id"]
        entry["evidence_count"] = len(evidence_map.get(sub_id, []))

        # Remove body — not needed for browse view
        entry.pop("body", None)
        # Remove file_path — internal only
        entry.pop("file_path", None)

        index_entries.append(entry)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(index_entries, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    return len(index_entries)


def export_content_files(conn: sqlite3.Connection, output_dir: Path,
                         evidence_map: dict | None = None):
    """Export individual TP-XXXX.json files for lazy loading."""
    cursor = conn.execute("SELECT * FROM submissions WHERE lower(category) = 'threatpath' ORDER BY id")
    columns = [desc[0] for desc in cursor.description]
    count = 0

    if evidence_map is None:
        evidence_map = {}

    output_dir.mkdir(parents=True, exist_ok=True)

    for row in cursor.fetchall():
        entry = dict(zip(columns, row))
        entry = _build_full_entry(conn, entry)

        # Remove file_path — internal only
        entry.pop("file_path", None)

        sub_id = entry["id"]
        entry["evidence"] = evidence_map.get(sub_id, [])
        entry["evidence_count"] = len(entry["evidence"])

        filepath = output_dir / f"{sub_id}.json"
        filepath.write_text(
            json.dumps(entry, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        count += 1

    return count


def export_stats_json(conn: sqlite3.Connection, output_path: Path):
    """Export pre-computed aggregate statistics."""
    total = conn.execute("SELECT COUNT(*) FROM submissions WHERE lower(category) = 'threatpath'").fetchone()[0]

    fraud_types = conn.execute(
        "SELECT DISTINCT fraud_type FROM submission_fraud_types sft JOIN submissions s ON sft.submission_id = s.id WHERE lower(s.category) = 'threatpath' ORDER BY fraud_type"
    ).fetchall()
    fraud_type_list = [r[0] for r in fraud_types]

    sectors = conn.execute(
        "SELECT DISTINCT sector FROM submission_sectors ss JOIN submissions s ON ss.submission_id = s.id WHERE lower(s.category) = 'threatpath' ORDER BY sector"
    ).fetchall()
    sector_list = [r[0] for r in sectors]

    tags = conn.execute(
        "SELECT tag, COUNT(*) as cnt FROM submission_tags st JOIN submissions s ON st.submission_id = s.id WHERE lower(s.category) = 'threatpath' GROUP BY tag ORDER BY cnt DESC"
    ).fetchall()
    top_tags = [{"tag": r[0], "count": r[1]} for r in tags[:20]]

    # CFPF phase coverage: count of TPs per phase
    phases = conn.execute(
        "SELECT phase, COUNT(*) as cnt FROM submission_cfpf_phases sp JOIN submissions s ON sp.submission_id = s.id WHERE lower(s.category) = 'threatpath' GROUP BY phase ORDER BY phase"
    ).fetchall()
    phase_coverage = {r[0]: r[1] for r in phases}

    # Coverage matrix: fraud_type × phase
    coverage_matrix = []
    for ft in fraud_type_list:
        # Find all TPs with this fraud type
        tp_rows = conn.execute(
            "SELECT sft.submission_id FROM submission_fraud_types sft JOIN submissions s ON sft.submission_id = s.id WHERE sft.fraud_type = ? AND lower(s.category) = 'threatpath'",
            (ft,)
        ).fetchall()
        tp_ids = [r[0] for r in tp_rows]
        phases_for_ft = {}
        for tp_id in tp_ids:
            tp_phases = conn.execute(
                "SELECT phase FROM submission_cfpf_phases WHERE submission_id = ?",
                (tp_id,)
            ).fetchall()
            for p in tp_phases:
                phases_for_ft[p[0]] = phases_for_ft.get(p[0], 0) + 1
        coverage_matrix.append({
            "fraud_type": ft,
            "phases": phases_for_ft,
            "total_tps": len(tp_ids)
        })

    # Regulatory alert stats
    reg_total = conn.execute("SELECT COUNT(*) FROM regulatory_alerts").fetchone()[0]
    reg_by_severity_rows = conn.execute(
        "SELECT severity, COUNT(*) FROM regulatory_alerts GROUP BY severity ORDER BY severity"
    ).fetchall()
    reg_by_severity = {r[0]: r[1] for r in reg_by_severity_rows if r[0]}
    reg_by_source_rows = conn.execute(
        "SELECT source, COUNT(*) FROM regulatory_alerts GROUP BY source ORDER BY source"
    ).fetchall()
    reg_by_source = {r[0]: r[1] for r in reg_by_source_rows if r[0]}

    stats = {
        "total": total,
        "fraudTypes": len(fraud_type_list),
        "fraudTypeList": fraud_type_list,
        "sectors": len(sector_list),
        "sectorList": sector_list,
        "phaseCoverage": phase_coverage,
        "topTags": top_tags,
        "coverageMatrix": coverage_matrix,
        "regulatoryAlerts": {
            "total": reg_total,
            "bySeverity": reg_by_severity,
            "bySource": reg_by_source,
            "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        },
        "generatedAt": datetime.now(timezone.utc).isoformat(),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(stats, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    return stats


def export_evidence_index(evidence_map: dict, output_path: Path):
    """Export cross-TP evidence index for deduplication and discovery.

    Generates flame-evidence-index.json listing all evidence entries
    across all threat paths with key metadata for fast lookup.
    """
    flat_entries = []
    for tp_id, entries in sorted(evidence_map.items()):
        for ev in entries:
            flat_entries.append({
                "evidence_id": ev.get("evidence_id", ""),
                "tp_id": tp_id,
                "title": ev.get("title", ""),
                "source": ev.get("source", ""),
                "cluster": ev.get("cluster", ""),
                "domain_count": ev.get("domain_count", ""),
                "confidence": ev.get("confidence", ""),
                "cfpf_phase_coverage": ev.get("cfpf_phase_coverage", ""),
            })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(flat_entries, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    return len(flat_entries)


def export_search_index(conn: sqlite3.Connection, output_path: Path) -> int:
    """Export a unified search index covering TPs, DL rules, and Baselines."""
    entries = []

    # ThreatPaths
    tp_rows = conn.execute(
        "SELECT id, title, summary FROM submissions "
        "WHERE lower(category) = 'threatpath' ORDER BY id"
    ).fetchall()
    for row in tp_rows:
        entries.append({
            "id": row[0],
            "type": "threat_path",
            "title": row[1],
            "text": row[2] or "",
        })

    # Baselines
    bl_rows = conn.execute(
        "SELECT id, title, summary FROM submissions "
        "WHERE lower(category) = 'baseline' ORDER BY id"
    ).fetchall()
    for row in bl_rows:
        entries.append({
            "id": row[0],
            "type": "baseline",
            "title": row[1],
            "text": row[2] or "",
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    return len(entries)


def export_index_md(conn: sqlite3.Connection, output_path: Path, stats: dict):
    """Programmatically generate INDEX.md based on parsed database."""
    lines = [
        "# FLAME Threat Path Index",
        "",
        f"> {stats['total']} threat paths covering {stats['fraudTypes']} fraud types across {stats['sectors']} sectors",
        "> Framework-agnostic: mapped to CFPF phases with cross-references to FT3, ATT&CK, and Group-IB Fraud Matrix",
        "",
        "## Coverage Summary",
        "",
        "| ID | Title | Fraud Types | Sectors | CFPF Phases |",
        "|----|-------|-------------|---------|-------------|"
    ]
    cursor = conn.execute("SELECT id, title FROM submissions WHERE lower(category) = 'threatpath' ORDER BY id")
    for row in cursor.fetchall():
        sub_id = row[0]
        title = row[1]
        fraud_types = ", ".join(_fetch_list(conn, "submission_fraud_types", "fraud_type", sub_id))
        sectors = ", ".join(map(str.capitalize, _fetch_list(conn, "submission_sectors", "sector", sub_id)))
        phases = _fetch_list(conn, "submission_cfpf_phases", "phase", sub_id)
        
        def format_phases(p_list):
            if not p_list: return ""
            nums = sorted([int(p.replace("P", "")) for p in p_list if p.startswith("P")])
            if not nums: return ""
            if len(nums) == 1: return f"P{nums[0]}"
            # Simple grouping
            if nums == list(range(nums[0], nums[-1]+1)):
                return f"P{nums[0]}-P{nums[-1]}"
            return ", ".join(f"P{n}" for n in nums)

        phase_str = format_phases(phases)
        lines.append(f"| {sub_id} | {title} | {fraud_types} | {sectors} | {phase_str} |")

    lines.append("")
    lines.append("## Coverage by Fraud Type")
    lines.append("")
    lines.append("| Fraud Type | Threat Paths |")
    lines.append("|------------|-------------|")
    
    for ft in stats["fraudTypeList"]:
        tp_rows = conn.execute("SELECT submission_id FROM submission_fraud_types WHERE fraud_type = ? ORDER BY submission_id", (ft,)).fetchall()
        tps = ", ".join([r[0] for r in tp_rows])
        lines.append(f"| {ft.title().replace('-', ' ')} | {tps} |")
        
    lines.append("")
    lines.append("## Coverage by Sector")
    lines.append("")
    lines.append("| Sector | Threat Paths |")
    lines.append("|--------|-------------|")
    for sec in stats["sectorList"]:
        tp_rows = conn.execute("SELECT submission_id FROM submission_sectors WHERE sector = ? ORDER BY submission_id", (sec,)).fetchall()
        tps = ", ".join([r[0] for r in tp_rows])
        lines.append(f"| {sec.title().replace('-', ' ')} | {tps} |")

    # Framework stats
    mitre_count = conn.execute("SELECT COUNT(DISTINCT sm.submission_id) FROM submission_mitre_attack sm JOIN submissions s ON sm.submission_id = s.id WHERE lower(s.category) = 'threatpath'").fetchone()[0]
    groupib_count = conn.execute("SELECT COUNT(DISTINCT sg.submission_id) FROM submission_groupib_stages sg JOIN submissions s ON sg.submission_id = s.id WHERE lower(s.category) = 'threatpath'").fetchone()[0]

    lines.append("")
    lines.append("## Framework Coverage Status")
    lines.append("")
    lines.append("| Framework | Mapping Status | Notes |")
    lines.append("|-----------|---------------|-------|")
    ft3_count = conn.execute("SELECT COUNT(DISTINCT sf.submission_id) FROM submission_ft3_tactics sf JOIN submissions s ON sf.submission_id = s.id WHERE lower(s.category) = 'threatpath'").fetchone()[0]
    ucff_count = conn.execute("SELECT COUNT(DISTINCT su.submission_id) FROM submission_ucff_domains su JOIN submissions s ON su.submission_id = s.id WHERE lower(s.category) = 'threatpath'").fetchone()[0]

    lines.append(f"| FS-ISAC CFPF | All {stats['total']} TPs mapped | Primary organizational structure |")
    lines.append(f"| MITRE ATT&CK | {mitre_count} of {stats['total']} TPs mapped | Where applicable (some fraud-only TPs lack ATT&CK equivalents) |")
    if ft3_count > 0:
        lines.append(f"| Stripe FT3 | Mapped ({ft3_count}/{stats['total']}) | MIT-licensed JSON vendored in data/ft3/ |")
    else:
        lines.append("| Stripe FT3 | Pending | MIT-licensed JSON available for parsing |")
    lines.append("| MITRE F3 | Awaiting release | Will map when F3 ships |")
    lines.append(f"| Group-IB Fraud Matrix | {groupib_count} of {stats['total']} TPs mapped | 10-stage lifecycle; stage names referenced for interoperability |")
    if ucff_count > 0:
        lines.append(f"| Group-IB UCFF | {ucff_count} of {stats['total']} TPs aligned | 7-domain lifecycle maturity assessment |")
    else:
        lines.append("| Group-IB UCFF | Pending | 7-domain lifecycle maturity assessment |")
    
    lines.append("")
    lines.append("## Cross-Threat Path Connections")
    lines.append("")
    lines.append("The fraud ecosystem is interconnected. Key relationships:")
    lines.append("")
    lines.append("```")
    lines.append("TP-0011 (Romance/Mule Recruitment) ──provides mule accounts to──▶ TP-0001, TP-0002, TP-0006, TP-0009")
    lines.append("TP-0003 (Synthetic Identity) ──provides fraudulent accounts to──▶ TP-0009, TP-0013")
    lines.append("TP-0014 (Insider Threat) ──provides customer data to──▶ TP-0001, TP-0005, TP-0008, TP-0012")
    lines.append("TP-0007 (Deepfake Voice) ──enhances social engineering in──▶ TP-0001, TP-0006, TP-0012")
    lines.append("TP-0008 (SIM Swap) ──bypasses MFA controls in──▶ TP-0001, TP-0005, TP-0013")
    lines.append("```")
    
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Static JSON API v1
# ---------------------------------------------------------------------------

def _api_envelope(data, total=None):
    """Wrap data in the standard API v1 envelope."""
    if total is None:
        total = len(data) if isinstance(data, list) else 1
    return {
        "meta": {
            "version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total": total,
        },
        "data": data,
    }


def _write_api_json(filepath: Path, obj):
    """Write a JSON API file, creating parent dirs as needed."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(
        json.dumps(obj, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )



def _xml_escape(text: str) -> str:
    """Escape special characters for safe XML embedding."""
    if not text:
        return ""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    return text


def generate_rss_feed(conn: sqlite3.Connection, root: Path) -> int:
    """Generate an RSS 2.0 feed at database/feed.xml.

    Returns the number of items written.
    """
    BASE_URL = "https://flameintel.org"
    feed_path = root / "database" / "feed.xml"
    feed_path.parent.mkdir(parents=True, exist_ok=True)

    items_xml: list[str] = []

    # --- Threat Path items ---
    cur = conn.execute(
        "SELECT id, title, summary, date, confidence_score, source_reliability "
        "FROM submissions WHERE lower(category) = 'threatpath' ORDER BY id"
    )
    columns = [desc[0] for desc in cur.description]
    for row in cur.fetchall():
        entry = dict(zip(columns, row))
        tp_id = entry["id"]
        title = entry.get("title", "")
        summary = entry.get("summary", "") or ""
        desc_text = _xml_escape(summary)  # Full summary, not truncated
        link = f"{BASE_URL}/#detail/{tp_id}"
        confidence = entry.get("confidence_score") or ""
        reliability = entry.get("source_reliability") or ""

        # RFC 822 pubDate
        pub_date = ""
        raw_date = entry.get("date", "")
        if raw_date:
            try:
                dt = datetime.strptime(raw_date, "%Y-%m-%d").replace(
                    tzinfo=timezone.utc
                )
                pub_date = _format_rfc822(dt)
            except (ValueError, TypeError):
                pass

        # Category tags: fraud_types
        ft_rows = conn.execute(
            "SELECT fraud_type FROM submission_fraud_types "
            "WHERE submission_id = ? ORDER BY fraud_type",
            (tp_id,),
        ).fetchall()
        # Category tags: cfpf_phases
        phase_rows = conn.execute(
            "SELECT phase FROM submission_cfpf_phases "
            "WHERE submission_id = ? ORDER BY phase",
            (tp_id,),
        ).fetchall()
        # Category tags: sectors
        sector_rows = conn.execute(
            "SELECT sector FROM submission_sectors "
            "WHERE submission_id = ? ORDER BY sector",
            (tp_id,),
        ).fetchall()
        # Category tags: mitre_attack
        mitre_rows = conn.execute(
            "SELECT technique_id FROM submission_mitre_attack "
            "WHERE submission_id = ? ORDER BY technique_id",
            (tp_id,),
        ).fetchall()
        cats = []
        for (ft,) in ft_rows:
            cats.append(f"        <category>{_xml_escape(ft)}</category>")
        for (ph,) in phase_rows:
            cats.append(f"        <category>CFPF-{_xml_escape(ph)}</category>")
        for (sec,) in sector_rows:
            cats.append(f"        <category>sector-{_xml_escape(sec)}</category>")
        for (tech,) in mitre_rows:
            cats.append(f"        <category>attack-{_xml_escape(tech)}</category>")

        parts = []
        parts.append("    <item>")
        parts.append(f"      <title>{_xml_escape(f'[{tp_id}] {title}')}</title>")
        parts.append(f"      <link>{_xml_escape(link)}</link>")
        parts.append(f'      <guid isPermaLink="true">{_xml_escape(link)}</guid>')
        parts.append(f"      <description>{desc_text}</description>")
        if pub_date:
            parts.append(f"      <pubDate>{pub_date}</pubDate>")
        if confidence:
            parts.append(f"      <flame:confidence>{confidence}</flame:confidence>")
        if reliability:
            parts.append(f"      <flame:sourceReliability>{_xml_escape(str(reliability))}</flame:sourceReliability>")
        parts.extend(cats)
        parts.append("    </item>")
        items_xml.append("\n".join(parts))

    # --- Assemble feed ---
    header_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:flame="https://flameintel.org/ns/1.0">',
        "  <channel>",
        "    <title>FLAME Intelligence Feed</title>",
        f"    <link>{BASE_URL}</link>",
        "    <description>FLAME \u2014 Fraud Lifecycle Analysis &amp; Mitigation Exchange. "
        "Community-driven fraud detection intelligence.</description>",
        f'    <atom:link href="{BASE_URL}/database/feed.xml" '
        f'rel="self" type="application/rss+xml" />',
    ]
    footer_lines = [
        "  </channel>",
        "</rss>",
    ]

    all_parts = header_lines + items_xml + footer_lines
    feed_xml = "\n".join(all_parts) + "\n"

    feed_path.write_text(feed_xml, encoding="utf-8")
    log.info("Generated RSS feed with %d items at %s", len(items_xml), feed_path)
    return len(items_xml)


def export_api_v1(conn: sqlite3.Connection, root: Path,
                  evidence_map: dict, stats: dict) -> int:
    """Generate static JSON API files under api/v1/.

    Returns the total number of JSON files written.
    """
    api_dir = root / "api" / "v1"
    file_count = 0

    # -------------------------------------------------------------------
    # 1. threat-paths.json — list of all TPs (metadata, no body)
    # -------------------------------------------------------------------
    cursor = conn.execute(
        "SELECT * FROM submissions WHERE lower(category) = 'threatpath' ORDER BY id"
    )
    columns = [desc[0] for desc in cursor.description]
    tp_list = []

    for row in cursor.fetchall():
        entry = dict(zip(columns, row))
        entry = _build_full_entry(conn, entry)
        sub_id = entry["id"]
        entry["evidence_count"] = len(evidence_map.get(sub_id, []))
        # Remove body and file_path — metadata only
        entry.pop("body", None)
        entry.pop("file_path", None)
        tp_list.append(entry)

    _write_api_json(api_dir / "threat-paths.json", _api_envelope(tp_list))
    file_count += 1

    # -------------------------------------------------------------------
    # 2. threat-paths/TP-XXXX.json — individual full TPs with body
    # -------------------------------------------------------------------
    tp_detail_dir = api_dir / "threat-paths"
    cursor = conn.execute(
        "SELECT * FROM submissions WHERE lower(category) = 'threatpath' ORDER BY id"
    )
    columns = [desc[0] for desc in cursor.description]

    for row in cursor.fetchall():
        entry = dict(zip(columns, row))
        entry = _build_full_entry(conn, entry)
        sub_id = entry["id"]
        entry["evidence"] = evidence_map.get(sub_id, [])
        entry["evidence_count"] = len(entry["evidence"])
        entry.pop("file_path", None)

        _write_api_json(
            tp_detail_dir / f"{sub_id}.json",
            _api_envelope(entry, total=1),
        )
        file_count += 1

    # -------------------------------------------------------------------
    # 3. baselines.json — all baselines (metadata from DB)
    # -------------------------------------------------------------------
    bl_cursor = conn.execute(
        "SELECT * FROM submissions WHERE lower(category) = 'baseline' ORDER BY id"
    )
    bl_columns = [desc[0] for desc in bl_cursor.description]
    bl_list = []

    for row in bl_cursor.fetchall():
        entry = dict(zip(bl_columns, row))
        entry = _build_full_entry(conn, entry)
        entry.pop("body", None)
        entry.pop("file_path", None)
        bl_list.append(entry)

    _write_api_json(api_dir / "baselines.json", _api_envelope(bl_list))
    file_count += 1

    # -------------------------------------------------------------------
    # 4. taxonomy.json — sectors + fraud types from flame_taxonomy.json
    # -------------------------------------------------------------------
    taxonomy_path = root / "data" / "flame_taxonomy.json"
    if taxonomy_path.exists():
        taxonomy_data = json.loads(taxonomy_path.read_text(encoding="utf-8"))
    else:
        log.warning("flame_taxonomy.json not found at %s", taxonomy_path)
        taxonomy_data = {"sectors": [], "fraud_types": []}

    _write_api_json(api_dir / "taxonomy.json", _api_envelope(taxonomy_data, total=1))
    file_count += 1

    # -------------------------------------------------------------------
    # 5. coverage-matrix.json — phase x fraud-type coverage matrix
    # -------------------------------------------------------------------
    coverage_matrix = stats.get("coverageMatrix", [])
    _write_api_json(
        api_dir / "coverage-matrix.json",
        _api_envelope(coverage_matrix),
    )
    file_count += 1

    # -------------------------------------------------------------------
    # 6. stats.json — aggregate statistics
    # -------------------------------------------------------------------
    _write_api_json(api_dir / "stats.json", _api_envelope(stats, total=1))
    file_count += 1

    return file_count


# ---------------------------------------------------------------------------
# Contributor extraction
# ---------------------------------------------------------------------------


def extract_contributors(conn: sqlite3.Connection, root: Path) -> list[dict]:
    """Extract contributor data from submission frontmatter and EP files."""
    contributors: dict[str, dict] = {}  # name -> stats

    def _ensure(author: str) -> None:
        if author not in contributors:
            contributors[author] = {
                "name": author,
                "threat_paths": 0,
                "detection_rules": 0,
                "baselines": 0,
                "emulation_playbooks": 0,
                "total": 0,
            }

    # Count TPs and Baselines from submissions table
    cur = conn.execute("SELECT id, author FROM submissions")
    for row in cur.fetchall():
        sub_id = row[0]
        author = row[1] or "Unknown"
        _ensure(author)
        if sub_id.startswith("TP-"):
            contributors[author]["threat_paths"] += 1
        elif sub_id.startswith("BL-") or sub_id.startswith("BASE-"):
            contributors[author]["baselines"] += 1

    # Detection rule contributor counting removed — see github.com/elchacal801/flame-detections

    # Count EPs from EmulationPlaybooks/ directory
    ep_dir = root / "EmulationPlaybooks"
    if ep_dir.exists():
        for ep_file in ep_dir.glob("EP-*.json"):
            try:
                ep_data = json.loads(ep_file.read_text(encoding="utf-8"))
                author = ep_data.get("author", "Unknown")
                _ensure(author)
                contributors[author]["emulation_playbooks"] += 1
            except (json.JSONDecodeError, OSError):
                continue

    # Calculate totals and sort
    for c in contributors.values():
        c["total"] = (
            c["threat_paths"] + c["detection_rules"]
            + c["baselines"] + c["emulation_playbooks"]
        )

    return sorted(contributors.values(), key=lambda x: x["total"], reverse=True)


def export_contributors_json(contributors: list[dict], root: Path) -> int:
    """Export contributor data to JSON file."""
    output = {
        "contributors": contributors,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    path = root / "database" / "flame-contributors.json"
    path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    return len(contributors)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def find_markdown_files(root: Path) -> list[Path]:
    """Find all markdown files in submission directories."""
    dirs = ["ThreatPaths", "Baselines"]
    files = []
    for d in dirs:
        dir_path = root / d
        if dir_path.exists():
            for f in sorted(dir_path.glob("*.md")):
                # Skip index files
                if f.name.upper() == "INDEX.MD":
                    continue
                files.append(f)
    return files


def main():
    parser = argparse.ArgumentParser(description="FLAME Database Builder")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Root directory of the FLAME repository"
    )
    args = parser.parse_args()
    root = args.root.resolve()

    log.info("FLAME Database Builder")
    log.info("Root: %s", root)

    # Find submission files
    md_files = find_markdown_files(root)
    log.info("Found %d markdown files", len(md_files))

    if not md_files:
        log.error("No markdown files found. Check directory structure.")
        sys.exit(1)

    # Initialize database
    db_path = root / "database" / "flame.db"
    conn = init_database(db_path)
    log.info("Database initialized: %s", db_path)

    # Load techniques catalog
    techniques_path = root / "data" / "cfpf_techniques.json"
    tech_count = load_techniques(conn, techniques_path)
    log.info("Loaded %d CFPF techniques", tech_count)

    # Process each submission file — collect evidence per TP
    loaded = 0
    errors = 0
    evidence_map: dict[str, list] = {}  # tp_id -> list of evidence dicts
    for filepath in md_files:
        meta = extract_frontmatter(filepath)
        if meta is None:
            errors += 1
            continue

        body = extract_body(filepath)
        summary = extract_summary(body)
        load_submission(conn, meta, body, summary, filepath)

        # Extract operational evidence from body
        sub_id = meta.get("id", "")
        ev_entries = extract_evidence(body)
        if ev_entries:
            evidence_map[sub_id] = ev_entries
            log.info("  Loaded: %s (%s) — %d evidence entries",
                     sub_id, meta.get("title", "?"), len(ev_entries))
        else:
            log.info("  Loaded: %s (%s)", sub_id, meta.get("title", "?"))
        loaded += 1

    conn.commit()

    total_evidence = sum(len(v) for v in evidence_map.values())
    log.info("Extracted %d evidence entries across %d TPs",
             total_evidence, len(evidence_map))

    # Detection rule ingestion removed — see github.com/elchacal801/flame-detections

    # Load regulatory alerts
    reg_csv = root / "data" / "regulatory_alerts.csv"
    reg_count = build_regulatory_alerts(conn, reg_csv)
    log.info("Loaded %d regulatory alerts", reg_count)

    # Export JSON (legacy — backward compatibility)
    json_path = root / "database" / "flame-data.json"
    count = export_json(conn, json_path)
    log.info("Exported %d submissions to %s (legacy)", count, json_path)

    # Export v2 data files
    index_path = root / "database" / "flame-index.json"
    idx_count = export_index_json(conn, index_path, evidence_map)
    log.info("Exported %d submissions to %s (index)", idx_count, index_path)

    content_dir = root / "database" / "flame-content"
    ct_count = export_content_files(conn, content_dir, evidence_map)
    log.info("Exported %d content files to %s", ct_count, content_dir)

    # Export evidence index
    ev_index_path = root / "database" / "flame-evidence-index.json"
    ev_count = export_evidence_index(evidence_map, ev_index_path)
    log.info("Exported %d evidence entries to %s", ev_count, ev_index_path)

    # Export regulatory alerts JSON
    reg_json_path = root / "database" / "regulatory-alerts.json"
    reg_json_count = export_regulatory_json(conn, reg_json_path)
    log.info("Exported %d regulatory alerts to %s", reg_json_count, reg_json_path)

    # Export search index
    search_index_path = root / "database" / "flame-search-index.json"
    search_count = export_search_index(conn, search_index_path)
    log.info("Exported %d search index entries to %s", search_count, search_index_path)

    stats_path = root / "database" / "flame-stats.json"
    stats = export_stats_json(conn, stats_path)
    log.info("Exported stats to %s (total=%d)", stats_path, stats["total"])

    # Export auto-generated markdown index
    md_index_path = root / "ThreatPaths" / "INDEX.md"
    export_index_md(conn, md_index_path, stats)
    log.info("Exported markdown index to %s", md_index_path)

    # Export API v1
    api_dir = root / "api" / "v1"
    api_count = export_api_v1(conn, root, evidence_map, stats)
    log.info("Exported API v1 to %s (%d files)", api_dir, api_count)

    # Generate RSS feed
    rss_count = generate_rss_feed(conn, root)
    log.info("Generated RSS feed with %d items", rss_count)

    # Extract and export contributor data
    contributors = extract_contributors(conn, root)
    contrib_count = export_contributors_json(contributors, root)
    log.info("Exported %d contributors to %s", contrib_count, root / "database" / "flame-contributors.json")

    conn.close()

    # Summary
    log.info("---")
    log.info("Build complete: %d loaded, %d errors, %d techniques",
             loaded, errors, tech_count)

    if errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
