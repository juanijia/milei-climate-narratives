#!/usr/bin/env python3
"""
apply_recoding_manifest.py

Applies the v3→v4 recoding manifest to all coded speech files:
  - Copies v3 files to analysis/coded_speeches/v4/
  - Renames code keys in [CODE: ...] annotations
  - Removes retired annotations (by passage content fingerprint)
  - Updates frontmatter coded_version field

Run from project root:
    python skills/qda-outputs/scripts/apply_recoding_manifest.py
"""

import re, shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
V3_DIR = PROJECT_ROOT / "analysis" / "coded_speeches" / "v3"
V4_DIR = PROJECT_ROOT / "analysis" / "coded_speeches" / "v4"
V4_DIR.mkdir(parents=True, exist_ok=True)

# ── Renames: old code key → new code key ─────────────────────────────────────
# Applied to [CODE: DIM > Key] annotations.
# Format: (old_dim, old_sub) → (new_dim, new_sub)
# Use None for new_sub to REMOVE the annotation entirely.

RENAMES = {
    # Merged codes — same dim, new name
    ("D1.1", "Deregulation_Benefits"):              ("D1.1", "Delegitimization_of_Regulation"),
    ("D1.2", "Attack_on_Universities"):             ("D1.2", "Attack_on_Universities_and_Research_Institutions"),
    ("D1.2", "Attack_on_Public_Research_Institutions"): ("D1.2", "Attack_on_Universities_and_Research_Institutions"),
    ("D1.2", "Rejection_of_Expert_Mediation"):      ("D1.2", "Attack_on_Experts_and_Technocrats"),
    ("D1.3", "Neo_Marxism"):                        ("D1.3", "Anti_Socialism_Anti_Collectivism"),
    # Promoted inductive → deductive
    ("INDUCTIVE", "Selective_Empiricism"):          ("D1.2", "Selective_Empiricism"),
    # Recode
    # #61: Temporal_Appropriation → Anti_State_Anti_Bureaucratic — handled below
}

# ── Passage fingerprints for REMOVALS ────────────────────────────────────────
# We identify passages to remove by a unique substring from their text.
# When a [CODE: ...] annotation is attached to one of these passages, REMOVE it.
# (Only the specific code on that passage, not the passage text itself.)

PASSAGE_REMOVALS = [
    # ID #4 — Reported_Denial (Bregman's paraphrase)
    {
        "passage_substr": "la destrucción del Planeta es una de las muestras más claras",
        "dim": "INDUCTIVE", "sub": "Reported_Denial"
    },
    # ID #43 — Neo_Marxism stacked on Woke_Bundling (Davos 2025, "man against nature")
    {
        "passage_substr": "Otro de los conflictos que los socialistas plantean es el del hombre contra la n",
        "dim": "D1.3", "sub": "Neo_Marxism"
    },
    # ID #49 — Neo_Marxism stacked on Woke_Bundling (Davos 2025, "same groups promoters")
    {
        "passage_substr": "It is no coincidence that these same groups are the main promoters of the bloody",
        "dim": "D1.3", "sub": "Neo_Marxism"
    },
    # ID #66 — Temporal_Appropriation (UN 80th)
    {
        "passage_substr": "A este cóctel de incentivos cruzados se le suma que, a diferencia de los primero",
        "dim": "INDUCTIVE", "sub": "Temporal_Appropriation"
    },
    # ID #80 — Deregulation_Benefits (Apertura 142)
    {
        "passage_substr": "Por último, también firmamos un mega Decreto de Necesidad y Urgencia para, por p",
        "dim": "D1.1", "sub": "Deregulation_Benefits"
    },
    # ID #82 — Anti_State_Anti_Bureaucratic (Apertura 143, "eliminamos cajas")
    {
        "passage_substr": "Eliminamos cajas de militancia como el INCAA, el INADI, el Ministerio de la Muje",
        "dim": "D1.1", "sub": "Anti_State_Anti_Bureaucratic"
    },
    # ID #87 — Woke_Bundling (Apertura 143, "igualdad ante la ley")
    {
        "passage_substr": "tenemos que recuperar el imperio de la igualdad ante la ley, terminando con este",
        "dim": "D1.3", "sub": "Woke_Bundling"
    },
    # ID #88 — Civilizational_Defense (Apertura 144, "valores/ética/economia")
    {
        "passage_substr": "en nuestra visión existe un claro orden de mérito. En primer lugar, están la éti",
        "dim": "D1.3", "sub": "Civilizational_Defense"
    },
    # ID #94 — Market_Primacy (Apertura 144, "minerales críticos")
    {
        "passage_substr": "Tenemos los minerales críticos que necesita Occidente, tenemos la energía: gas,",
        "dim": "D1.1", "sub": "Market_Primacy"
    },
    # ID #97 — Temporal_Appropriation (Apertura 144)
    {
        "passage_substr": "Es para dejar de ser una Nación inmadura, que dilapida el futuro para repartir b",
        "dim": "INDUCTIVE", "sub": "Temporal_Appropriation"
    },
]

# ID #61 special case: Temporal_Appropriation → Anti_State_Anti_Bureaucratic
ID61_PASSAGE_SUBSTR = "Así, los Estados contemporáneos han entrado en una dinámica donde el interés del"
ID61_OLD = ("INDUCTIVE", "Temporal_Appropriation")
ID61_NEW = ("D1.1", "Anti_State_Anti_Bureaucratic")


def passage_matches(passage_text, substr):
    return substr[:60].lower() in passage_text.lower()


def apply_manifest(text, filename):
    """
    Process a coded speech file text and return the v4 version.
    """
    changes = []

    # Update frontmatter
    text = re.sub(r'^coded_version:\s*v3', 'coded_version: v4', text, flags=re.MULTILINE)
    text = re.sub(r'^coded_date:.*$', 'coded_date: 2026-07-13', text, flags=re.MULTILINE)

    # Update coding summary version label
    text = text.replace('## Coding Summary (v3)', '## Coding Summary (v4)')

    # Split into lines for processing
    lines = text.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Detect [CODE: ...] annotation line
        code_match = re.match(r'(`\[CODE:\s*)([^\]]+)(\]`\s*[—–\-]+.*)', stripped)
        if code_match:
            tag_content = code_match.group(2)  # e.g. "D1.1 > Deregulation_Benefits" or "INDUCTIVE > Temporal_Appropriation | ..."

            # Parse dim and sub from tag
            dim_sub_match = re.match(r'([A-Z0-9\.]+)\s*>\s*([A-Za-z_]+)', tag_content)
            if dim_sub_match:
                dim_raw = dim_sub_match.group(1)
                sub_raw = dim_sub_match.group(2)
                dim = dim_raw  # keep as-is for lookup

                # Find the passage text by looking backwards in result
                passage_context = ' '.join(
                    l.strip() for l in result[-15:]
                    if l.strip() and not l.strip().startswith('`[CODE')
                    and not l.strip().startswith('---')
                    and not l.strip().startswith('#')
                )

                # --- Check REMOVALS ---
                remove_this = False
                for removal in PASSAGE_REMOVALS:
                    if (removal['dim'] == dim and removal['sub'] == sub_raw and
                            passage_matches(passage_context, removal['passage_substr'])):
                        remove_this = True
                        changes.append(f"REMOVED [{dim} > {sub_raw}] (passage: {removal['passage_substr'][:40]}...)")
                        break

                # --- Check ID #61 special recode ---
                if (not remove_this and dim == ID61_OLD[0] and sub_raw == ID61_OLD[1] and
                        passage_matches(passage_context, ID61_PASSAGE_SUBSTR)):
                    new_dim, new_sub = ID61_NEW
                    new_tag = tag_content.replace(f"{dim} > {sub_raw}", f"{new_dim} > {new_sub}")
                    line = stripped.replace(tag_content, new_tag)
                    line = '`[CODE: ' + line.split('`[CODE: ', 1)[1]
                    changes.append(f"RECODED [{dim} > {sub_raw}] → [{new_dim} > {new_sub}]")
                    result.append(line)
                    i += 1
                    continue

                if remove_this:
                    # Skip this annotation line
                    i += 1
                    continue

                # --- Apply RENAMES ---
                rename_key = (dim, sub_raw)
                if rename_key in RENAMES:
                    new_dim, new_sub = RENAMES[rename_key]
                    new_tag_part = f"{new_dim} > {new_sub}"
                    old_tag_part = f"{dim} > {sub_raw}"
                    new_line_content = tag_content.replace(old_tag_part, new_tag_part, 1)
                    line = stripped.replace(tag_content, new_line_content, 1)
                    line = '`[CODE: ' + line.split('`[CODE: ', 1)[1]
                    changes.append(f"RENAMED [{dim} > {sub_raw}] → [{new_dim} > {new_sub}]")

        result.append(line)
        i += 1

    return '\n'.join(result), changes


def main():
    v3_files = sorted(V3_DIR.glob("*.md"))
    v3_files = [f for f in v3_files if not f.name.startswith("frequency_tally")]

    total_changes = []

    for v3_path in v3_files:
        v4_path = V4_DIR / v3_path.name
        text = v3_path.read_text(encoding='utf-8')

        v4_text, changes = apply_manifest(text, v3_path.name)

        v4_path.write_text(v4_text, encoding='utf-8')

        print(f"\n{v3_path.name}:")
        if changes:
            for c in changes:
                print(f"  {c}")
        else:
            print("  (no changes — copied as-is)")

        total_changes.extend(changes)

    print(f"\n{'='*60}")
    print(f"Files processed: {len(v3_files)}")
    print(f"Total changes applied: {len(total_changes)}")
    print(f"Output directory: {V4_DIR}")


if __name__ == '__main__':
    main()
