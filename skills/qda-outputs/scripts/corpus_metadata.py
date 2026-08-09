#!/usr/bin/env python3
"""
corpus_metadata.py
Shared metadata loader for the QDA output generators (generate_xlsx.py, generate_html.py).

Replaces the old approach of hardcoding a per-speech dict (DATE_TO_SPEECH / SPEECH_META /
SPEECH_META_BY_FILE) inside each script. Those dicts only covered the speeches coded at the
time they were written and had to be hand-edited for every new speech — silently degrading
to "Unknown" metadata (xlsx) or being skipped outright (HTML) when a file had no entry.

Instead, this module derives title/venue/event-type/scope for every coded speech file
directly from the master corpus database (data/sources/milei_discursos_index_2023-2026_
updated260718.csv.csv), which the researchers maintain for the full 193-speech corpus.
No per-speech script edits are needed as new speeches are coded — the outputs scale
automatically with the corpus.

Matching strategy (per coded file):
  1. Match by source_url (frontmatter) == CSV `link` column (normalized). Most reliable —
     works even when several speeches share the same date.
  2. Fall back to date match if the date is unique in the CSV.
  3. Fall back to keyword overlap between the filename slug and `evento-discurso` if the
     date collides across multiple CSV rows and none has a matching link.
  4. If nothing matches, the file is still included (never silently dropped) with metadata
     derived from its own frontmatter and a "sin clasificar" event type — and the mismatch
     is returned in `warnings` so the caller can print it.
"""

import csv
import re
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

CSV_RELATIVE_PATH = Path("data") / "sources" / "milei_discursos_index_2023-2026_updated260718.csv.csv"

TIPO_SHORT_LABELS = {
    "acto institucional": "Acto Inst.",
    "foro economico": "Foro Econ.",
    "evento ideologico/politico": "Evento Ideol.",
    "premio / reconocimiento": "Premio",
    "fundacion / think tank": "Think Tank",
    "bilateral / diplomatico": "Bilateral",
    "cumbre internacional": "Cumbre Int'l",
    "bolsa / camara de comercio": "Bolsa/Cámara",
    "empresa": "Empresa",
    "cadena nacional": "Cadena Nac.",
    "sectorial": "Sectorial",
    "acto conmemorativo/patrio": "Conmem./Patrio",
    "consejo empresarial": "Consejo Emp.",
    "clase magistral / universidad": "Clase Magistral",
    "acto conmemorativo": "Conmemorativo",
    "foro economico / empresarial": "Foro Emp.",
    "comunitario / religioso": "Comunitario",
    "organismo internacional": "Org. Int'l",
    "foro economico / financiero": "Foro Financ.",
    "evento empresarial": "Evento Emp.",
    "evento economico / cultural": "Evento Econ/Cult",
    "debate presidencial": "Debate",
    "acto institucional / bilateral": "Inst./Bilateral",
    "sin clasificar": "Sin Clasificar",
}

VENUE_TYPE_PALETTE = [
    "7c3aed", "0e7490", "065f46", "92400e", "be185d", "0369a1",
    "4d7c0f", "b45309", "6d28d9", "0f766e", "c2410c", "475569",
    "9333ea", "0891b2", "15803d", "a16207", "db2777", "1d4ed8",
]

# ── Venue-type meta-groups (added 2026-08-08) ──────────────────────────────────
# The master CSV's 23 raw `tipo` values are too granular to chart or cross-tab
# legibly (see analysis/results/v4 formatting review). These 6 groups collapse
# them into analytically coherent buckets — approved by the research team.
# Group sizes (of the 193 coded speeches): Economic & Business Forums 61,
# State & Institutional Acts 37, Awards/Academic/Think Tanks 33,
# International & Diplomatic 26, Ideological & Political Events 22,
# Commemorative & Community 14.
VENUE_GROUPS_ORDER = [
    "Economic & Business Forums",
    "State & Institutional Acts",
    "Awards, Academic & Think Tanks",
    "International & Diplomatic",
    "Ideological & Political Events",
    "Commemorative & Community",
    "Unclassified",
]

TIPO_GROUP = {
    # Economic & Business Forums
    "foro economico": "Economic & Business Forums",
    "foro economico / empresarial": "Economic & Business Forums",
    "foro economico / financiero": "Economic & Business Forums",
    "bolsa / camara de comercio": "Economic & Business Forums",
    "empresa": "Economic & Business Forums",
    "consejo empresarial": "Economic & Business Forums",
    "evento empresarial": "Economic & Business Forums",
    "sectorial": "Economic & Business Forums",
    # State & Institutional Acts
    "acto institucional": "State & Institutional Acts",
    "acto institucional / bilateral": "State & Institutional Acts",
    "cadena nacional": "State & Institutional Acts",
    # Awards, Academic & Think Tanks
    "premio / reconocimiento": "Awards, Academic & Think Tanks",
    "fundacion / think tank": "Awards, Academic & Think Tanks",
    "clase magistral / universidad": "Awards, Academic & Think Tanks",
    "evento economico / cultural": "Awards, Academic & Think Tanks",
    # International & Diplomatic
    "bilateral / diplomatico": "International & Diplomatic",
    "cumbre internacional": "International & Diplomatic",
    "organismo internacional": "International & Diplomatic",
    # Ideological & Political Events
    "evento ideologico/politico": "Ideological & Political Events",
    "debate presidencial": "Ideological & Political Events",
    # Commemorative & Community
    "acto conmemorativo/patrio": "Commemorative & Community",
    "acto conmemorativo": "Commemorative & Community",
    "comunitario / religioso": "Commemorative & Community",
}

VENUE_GROUP_PALETTE = {
    "Economic & Business Forums": "0e7490",
    "State & Institutional Acts": "1d4ed8",
    "Awards, Academic & Think Tanks": "7c3aed",
    "International & Diplomatic": "0f766e",
    "Ideological & Political Events": "b45309",
    "Commemorative & Community": "475569",
    "Unclassified": "6b7280",
}


def group_for_tipo(tipo):
    if not tipo:
        return "Unclassified"
    return TIPO_GROUP.get(tipo.strip().lower(), "Unclassified")


def short_label(tipo):
    if not tipo:
        return "Sin Clasificar"
    return TIPO_SHORT_LABELS.get(tipo.strip().lower(), tipo.strip().title()[:16])


def _norm_url(u):
    if not u:
        return ""
    return u.strip().rstrip("/").lower()


def _norm_words(s):
    return set(re.findall(r"[a-záéíóúñ]+", (s or "").lower()))


def _load_csv_rows(project_root):
    csv_path = project_root / CSV_RELATIVE_PATH
    if not csv_path.exists():
        raise FileNotFoundError(f"Master corpus CSV not found: {csv_path}")
    with open(csv_path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_metadata_index(project_root, coded_dir):
    rows = _load_csv_rows(project_root)

    link_index = {}
    date_index = {}
    for r in rows:
        link = _norm_url(r.get("link", ""))
        if link:
            link_index.setdefault(link, []).append(r)
        date_index.setdefault(r.get("fecha", "").strip(), []).append(r)

    index = {}
    warnings = []

    for path in sorted(Path(coded_dir).glob("*.md")):
        if path.name.startswith("frequency_tally"):
            continue
        raw = path.read_text(encoding="utf-8")

        date_m = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", raw, re.MULTILINE)
        date = date_m.group(1) if date_m else None

        url_m = re.search(r'^source_url:\s*"?([^"\n]+?)"?\s*$', raw, re.MULTILINE)
        url = _norm_url(url_m.group(1)) if url_m else ""

        title_m = re.search(r'^title:\s*"?([^"\n]+?)"?\s*$', raw, re.MULTILINE)
        fm_title = title_m.group(1).strip() if title_m else path.stem

        row, method = None, None

        if url and url in link_index:
            row, method = link_index[url][0], "url"
        elif date and date in date_index:
            candidates = date_index[date]
            if len(candidates) == 1:
                row, method = candidates[0], "date-unique"
            else:
                slug_words = _norm_words(path.stem)
                best, best_score = None, -1
                for cand in candidates:
                    score = len(slug_words & _norm_words(cand.get("evento-discurso", "")))
                    if score > best_score:
                        best, best_score = cand, score
                row, method = best, "date-ambiguous-keyword-match"
                warnings.append((
                    path.name,
                    f"{len(candidates)} CSV rows share date {date}; no link match, "
                    f"matched by filename/event keyword overlap (verify manually)."
                ))
        elif date:
            try:
                d = datetime.strptime(date, "%Y-%m-%d")
                for delta in (-1, 1):
                    nearby = (d + timedelta(days=delta)).strftime("%Y-%m-%d")
                    if nearby in date_index and len(date_index[nearby]) == 1:
                        row, method = date_index[nearby][0], "date-adjacent"
                        warnings.append((
                            path.name,
                            f"frontmatter date {date} not in CSV; matched to adjacent "
                            f"CSV date {nearby} (single unambiguous row). Verify this is "
                            f"the correct speech."
                        ))
                        break
            except ValueError:
                pass

        if row is None:
            warnings.append((
                path.name,
                "no CSV match (no source_url link match, no date match) — using "
                "frontmatter title only; tipo set to 'sin clasificar'. Check the master "
                "CSV for this speech."
            ))
            index[path.name] = {
                "title": fm_title,
                "venue": "Sin clasificar",
                "pais": "",
                "tipo": "sin clasificar",
                "subtipo": "",
                "clima": "",
                "scope": "National",
                "venue_group": "Unclassified",
            }
            continue

        pais = (row.get("pais") or "").strip()
        tipo = (row.get("tipo") or "").strip().lower() or "sin clasificar"
        index[path.name] = {
            "title": (row.get("evento-discurso") or fm_title).strip().title(),
            "venue": (row.get("lugar") or "").strip().title(),
            "pais": pais,
            "tipo": tipo,
            "subtipo": (row.get("subtipo") or "").strip(),
            "clima": (row.get("clima") or "").strip(),
            "scope": "National" if pais.lower() == "argentina" else "International",
            "venue_group": group_for_tipo(tipo),
        }

    return index, warnings


def venue_type_categories(index):
    counts = Counter(v["tipo"] for v in index.values() if v.get("tipo"))
    return [t for t, _ in counts.most_common()]


def venue_group_categories(index):
    """Ordered list of venue groups actually present in the corpus, in the fixed
    canonical order (VENUE_GROUPS_ORDER) rather than by frequency — keeps chart/
    table ordering stable across regenerations regardless of which speeches are
    coded at a given time."""
    present = {v.get("venue_group", "Unclassified") for v in index.values()}
    return [g for g in VENUE_GROUPS_ORDER if g in present]


def color_for_tipo(tipo, ordered_categories):
    try:
        i = ordered_categories.index(tipo)
    except ValueError:
        i = 0
    return VENUE_TYPE_PALETTE[i % len(VENUE_TYPE_PALETTE)]


def print_warnings(warnings):
    if not warnings:
        print("  Metadata match: all coded files matched the master CSV cleanly.")
        return
    print(f"  Metadata match: {len(warnings)} file(s) needed a fallback match:")
    for fname, msg in warnings:
        print(f"    - {fname}: {msg}")
