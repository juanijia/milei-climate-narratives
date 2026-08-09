#!/usr/bin/env python3
"""
corpus_data.py
Canonical parser for the v4 coded speech corpus — the single place that turns the
annotated markdown files in analysis/coded_speeches/v4/ into structured data for
every downstream consumer (generate_xlsx.py, generate_html.py, update_frequency_tally.py).

This replaces two problems the previous design had:

  1. Duplicated parsing. generate_xlsx.py and generate_html.py each had their own
     regex-based parser for the same `[CODE: ...]` annotation format. They happened
     to agree, but nothing enforced that — a change to one script's passage-buffering
     logic could silently diverge from the other's, producing different counts in
     the xlsx vs. the HTML explorer with no warning. Now there is exactly one parse;
     both outputs are projections of it (see flatten_segments).

  2. Silent code-name drift. A typo'd sub-code, or a retired v3 code applied by
     habit (e.g. "Neo_Marxism", renamed to Anti_Socialism_Anti_Collectivism in v4),
     used to be ingested silently and counted under its own bucket. validate_code()
     flags anything that isn't a current v4 deductive code (INDUCTIVE codes are
     exempt by design — they're meant to be free-form pending formalization).

The frequency tally (frequency_tally_v4.json) is no longer hand-maintained — see
update_frequency_tally.py, which computes it from this same parse.
"""

import re
from pathlib import Path

# ── V4 codebook schema (mirrors coding_book_v4.md) ────────────────────────────
# Single canonical list of valid codes — generate_xlsx.py used to duplicate this
# list three times (SUBCODE_DISPLAY, the sub-code sheet's "ensure all codes present"
# list, and _context_sheet's SUBCODES_V4); it now derives from here instead.

VALID_CODES = {
    "D1.1": [
        "Market_Primacy",
        "Anti_State_Anti_Bureaucratic",
        "Anti_Casta",
        "Delegitimization_of_Regulation",
        "Sustainability_as_Ideological_or_Harmful",
        "Rejection_of_Multilateral_Governance",
    ],
    "D1.2": [
        "Attack_on_Universities_and_Research_Institutions",
        "Attack_on_Experts_and_Technocrats",
        "Climate_Skepticism_or_Dismissal",
        "Pseudo_Science_or_Ideological_Science",
        "Selective_Empiricism",
    ],
    "D1.3": [
        "Woke_Bundling",
        "Anti_Socialism_Anti_Collectivism",
        "Civilizational_Defense",
    ],
}

RETIRED_CODES = {
    "Temporal_Appropriation": "eliminated in v4 (see watchlist in coding_book_v4.md)",
    "Reported_Denial": "retired in v4 — codes third-party paraphrase, not primary discourse",
    "Deregulation_Benefits": "merged into Delegitimization_of_Regulation in v4",
    "Rejection_of_Expert_Mediation": "absorbed into Attack_on_Experts_and_Technocrats in v4",
    "Attack_on_Universities": "merged into Attack_on_Universities_and_Research_Institutions in v4",
    "Attack_on_Public_Research_Institutions": "merged into Attack_on_Universities_and_Research_Institutions in v4",
    "Neo_Marxism": "renamed to Anti_Socialism_Anti_Collectivism in v4",
}

DIMS_ORDER = ["D1.1", "D1.2", "D1.3", "IND"]


def validate_code(dim, sub_key):
    """Returns a warning string if the code is unrecognized or retired, else None.
    INDUCTIVE codes are exempt — they're free-form by design pending formalization."""
    if dim == "IND":
        return None
    if sub_key in RETIRED_CODES:
        return f"retired code `{dim} > {sub_key}` used — {RETIRED_CODES[sub_key]}"
    if sub_key not in VALID_CODES.get(dim, []):
        return f"unrecognized code `{dim} > {sub_key}` — not in the v4 codebook; check for a typo"
    return None


# ── Regexes (one definition, used by the one parser) ──────────────────────────

_CODE_LINE_RE = re.compile(r'`\[CODE:\s*([^\]]+)\]`\s*[—–\-]+\s*\*?(?:Memo:)?\s*(.*)')
_DATE_RE = re.compile(r'^date:\s*(\d{4}-\d{2}-\d{2})', re.MULTILINE)


def _parse_code_tag(tag_str):
    """'D1.1 > Sub_code' or 'INDUCTIVE > Sub_code | ...' -> (dim, sub_key)."""
    m = re.match(r'([A-Z0-9\.]+)\s*>\s*([A-Za-z_]+)', tag_str.strip())
    if not m:
        return None, None
    dim_raw, sub_raw = m.group(1), m.group(2)
    return ("IND" if dim_raw == "INDUCTIVE" else dim_raw), sub_raw


def _clean_text(line):
    line = re.sub(r'\*\*\[([^\]]+)\]\*\*:\s*', r'[\1]: ', line)
    line = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
    line = re.sub(r'\*([^*]+)\*', r'\1', line)
    return ' '.join(line.split()).strip()


def _is_skip(line):
    s = line.strip()
    if not s or s.startswith('---') or s.startswith('#'):
        return True
    if re.match(r'^\*\[', s) or re.match(r'^\[Not coded', s):
        return True
    return False


def get_date(raw):
    m = _DATE_RE.search(raw)
    return m.group(1) if m else None


def parse_speech_segments(path):
    """
    The one canonical parse. Reads a coded speech file and returns
    (segments, warnings):

      segments: ordered list of
          {'type': 'plain', 'text': str} or
          {'type': 'coded', 'text': str, 'codes': [{'dim','sub','memo'}, ...]}

      warnings: list of code-validation warning strings (typos/retired codes)
                found in this file.

    Both the xlsx flat-row view and the HTML full-transcript view are projections
    of this same segment list (see flatten_segments below).
    """
    raw = path.read_text(encoding='utf-8')
    body = re.sub(r'^---\n.*?---\n', '', raw, count=1, flags=re.DOTALL)
    body = re.sub(r'\n---\n## Coding Summary.*$', '', body, flags=re.DOTALL)
    body = re.sub(r'\n## Coding Summary.*$', '', body, flags=re.DOTALL)

    lines = body.split('\n')
    segments = []
    text_buffer = []
    pending_passage = None
    pending_codes = []
    warnings = []

    def flush_pending():
        nonlocal pending_passage, pending_codes
        if pending_passage is not None:
            if pending_codes:
                segments.append({'type': 'coded', 'text': pending_passage,
                                  'codes': pending_codes[:]})
            else:
                segments.append({'type': 'plain', 'text': pending_passage})
        pending_passage = None
        pending_codes = []

    def flush_buffer():
        nonlocal text_buffer, pending_passage, pending_codes
        if text_buffer:
            text = ' '.join(text_buffer).strip()
            text_buffer.clear()
            if len(text) > 10:
                flush_pending()
                pending_passage = text
                pending_codes = []

    for line in lines:
        stripped = line.strip()
        m = _CODE_LINE_RE.match(stripped)
        if m:
            if text_buffer:
                flush_buffer()
            dim, sub = _parse_code_tag(m.group(1))
            memo = m.group(2).strip().strip('*').strip()
            if dim and sub and pending_passage:
                issue = validate_code(dim, sub)
                if issue:
                    warnings.append(f"{path.name}: {issue}")
                pending_codes.append({'dim': dim, 'sub': sub, 'memo': memo})
            continue
        if _is_skip(line):
            flush_buffer()
            continue
        cleaned = _clean_text(line)
        if cleaned and len(cleaned) > 5:
            if pending_codes:
                flush_pending()
            text_buffer.append(cleaned)

    flush_buffer()
    flush_pending()
    return segments, warnings


def flatten_segments(segments, base_row):
    """
    Project the segment list into one flat row per code annotation — the shape
    generate_xlsx.py's Coded Passages sheet needs (one row per code, so a passage
    with two stacked codes yields two rows sharing the same passage text).
    base_row supplies the per-file fields (speech, date, venue, event_type, scope)
    merged into every row.
    """
    rows = []
    for seg in segments:
        if seg['type'] != 'coded':
            continue
        for c in seg['codes']:
            row = dict(base_row)
            row.update({
                'passage': seg['text'],
                'dim': c['dim'],
                'sub_key': c['sub'],
                'memo': c['memo'],
            })
            rows.append(row)
    return rows


def build_corpus(coded_dir, meta_index):
    """
    Parse every coded file in coded_dir exactly once. Returns (files, warnings):

      files: list of per-file dicts (in filename-sorted / chronological order),
          each: {filename, speech, date, venue, event_type, scope,
                 segments, flat_entries}
      warnings: list of code-validation warning strings across the whole corpus
                (typos / retired codes) — metadata-match warnings are handled
                separately by corpus_metadata.build_metadata_index().
    """
    files = []
    warnings = []
    for path in sorted(Path(coded_dir).glob("*.md")):
        if path.name.startswith("frequency_tally"):
            continue
        raw = path.read_text(encoding='utf-8')
        date = get_date(raw) or "0000-00-00"
        meta = meta_index.get(path.name, {})
        base_row = {
            'speech': meta.get('title', path.stem),
            'date': date,
            'venue': meta.get('venue', 'Sin clasificar'),
            'event_type': meta.get('tipo', 'sin clasificar'),
            'venue_group': meta.get('venue_group', 'Unclassified'),
            'scope': meta.get('scope', 'National'),
        }
        segments, file_warnings = parse_speech_segments(path)
        warnings.extend(file_warnings)
        flat_entries = flatten_segments(segments, base_row)
        files.append({
            'filename': path.name,
            **base_row,
            'segments': segments,
            'flat_entries': flat_entries,
        })
    return files, warnings


def print_code_warnings(warnings):
    if not warnings:
        print("  Code validation: all codes recognized (no typos or retired codes found).")
        return
    print(f"  Code validation: {len(warnings)} issue(s) found:")
    for w in warnings:
        print(f"    - {w}")


def compute_frequency_tally(files, version="v4"):
    """
    Build the frequency_tally_v4.json structure directly from the parsed corpus,
    instead of it being hand-maintained. Unknown/retired codes are still counted
    (the tally should reflect what's actually in the files) — they're flagged
    separately as warnings by build_corpus, not hidden here.
    """
    counts = {dim: {} for dim in DIMS_ORDER}
    for f in files:
        for row in f['flat_entries']:
            dim, sub = row['dim'], row['sub_key']
            counts.setdefault(dim, {})
            counts[dim][sub] = counts[dim].get(sub, 0) + 1

    def ordered(dim, canonical):
        d = counts.get(dim, {})
        out = {k: d.get(k, 0) for k in canonical}
        for k, v in d.items():  # surface any extra/legacy/typo'd keys too, don't hide them
            if k not in out:
                out[k] = v
        return out

    return {
        "_metadata": {
            "version": version,
            "corpus_size": len(files),
            "coding_dimension": "Dimension 1 only — speeches corpus",
            "files_coded": [f['filename'] for f in files],
        },
        "D1_Discursive_Delegitimization": {
            "D1.1_State_Intervention_Governance": ordered("D1.1", VALID_CODES["D1.1"]),
            "D1.2_Public_Science_Expertise": ordered("D1.2", VALID_CODES["D1.2"]),
            "D1.3_Cultural_Backlash": ordered("D1.3", VALID_CODES["D1.3"]),
        },
        "Inductive": counts.get("IND", {}),
    }
