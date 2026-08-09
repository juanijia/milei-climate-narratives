#!/usr/bin/env python3
"""
update_frequency_tally.py
Regenerates analysis/coded_speeches/v4/frequency_tally_v4.json directly from the
coded speech .md files, via corpus_data.compute_frequency_tally() — replacing the
old model where this file was hand-edited after every coding batch and could
silently drift out of sync with what the .md files actually contain (the same
failure mode the generate_xlsx.py / generate_html.py parser duplication used to
have, just for counts instead of passages).

Usage (run from project root):
    python skills/qda-outputs/scripts/update_frequency_tally.py
    python skills/qda-outputs/scripts/update_frequency_tally.py --set-note "..."
    python skills/qda-outputs/scripts/update_frequency_tally.py --set-date 2026-07-20

What this preserves across a regeneration:
  - `_metadata.note`: the hand-written narrative history of the corpus (batch
    rationale, recoding decisions, methodology changes, etc.). This is authored
    content, not derived data, so it's carried over from the existing file
    rather than being wiped out. Pass --set-note to update it deliberately.
  - `_metadata.coding_date`: likewise preserved unless --set-date is passed.

Everything else — corpus_size, files_coded, and every dimension/sub-code count —
is fully recomputed from the current .md files every time, so it can never
drift out of sync the way a hand-maintained tally could.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from corpus_metadata import build_metadata_index, print_warnings
from corpus_data import build_corpus, print_code_warnings, compute_frequency_tally

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
CODED_DIR    = PROJECT_ROOT / "analysis" / "coded_speeches" / "v4"
TALLY_PATH   = CODED_DIR / "frequency_tally_v4.json"


def _flatten_counts(tally):
    """Flatten the nested tally into {dim: {sub: count}} for diffing (drops _metadata)."""
    d1 = tally.get("D1_Discursive_Delegitimization", {})
    return {
        "D1.1": d1.get("D1.1_State_Intervention_Governance", {}),
        "D1.2": d1.get("D1.2_Public_Science_Expertise", {}),
        "D1.3": d1.get("D1.3_Cultural_Backlash", {}),
        "IND":  tally.get("Inductive", {}),
    }


def _print_diff(old_tally, new_tally):
    old_flat = _flatten_counts(old_tally) if old_tally else {}
    new_flat = _flatten_counts(new_tally)
    changed = False
    for dim in ("D1.1", "D1.2", "D1.3", "IND"):
        old_subs = old_flat.get(dim, {})
        new_subs = new_flat.get(dim, {})
        for k in sorted(set(old_subs) | set(new_subs)):
            o, n = old_subs.get(k, 0), new_subs.get(k, 0)
            if o != n:
                changed = True
                print(f"  {dim} > {k}: {o} -> {n}")
    if not changed:
        print("  No count changes since the last saved tally.")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--set-date", help="Override _metadata.coding_date (YYYY-MM-DD)")
    parser.add_argument("--set-note", help="Override _metadata.note with new narrative text")
    args = parser.parse_args()

    if not CODED_DIR.exists():
        print(f"ERROR: Coded speeches directory not found: {CODED_DIR}")
        sys.exit(1)

    meta_index, meta_warnings = build_metadata_index(PROJECT_ROOT, CODED_DIR)
    print_warnings(meta_warnings)

    files, code_warnings = build_corpus(CODED_DIR, meta_index)
    print_code_warnings(code_warnings)

    computed = compute_frequency_tally(files, version="v4")

    old_tally = None
    old_meta = {}
    if TALLY_PATH.exists():
        old_tally = json.loads(TALLY_PATH.read_text(encoding="utf-8"))
        old_meta = old_tally.get("_metadata", {})

    coding_date = args.set_date or old_meta.get("coding_date", "")
    note = args.set_note or old_meta.get("note", "")

    # Rebuild _metadata in a fixed, readable key order (matches the pre-existing
    # hand-maintained file's layout) rather than however dict insertion happens to fall.
    ordered_meta = {"version": computed["_metadata"]["version"]}
    if coding_date:
        ordered_meta["coding_date"] = coding_date
    ordered_meta["corpus_size"] = computed["_metadata"]["corpus_size"]
    ordered_meta["coding_dimension"] = computed["_metadata"]["coding_dimension"]
    ordered_meta["files_coded"] = computed["_metadata"]["files_coded"]
    if note:
        ordered_meta["note"] = note

    new_tally = {
        "_metadata": ordered_meta,
        "D1_Discursive_Delegitimization": computed["D1_Discursive_Delegitimization"],
        "Inductive": computed["Inductive"],
    }

    print(f"\nRecomputed tally from {len(files)} coded files.")
    print("Changes vs. the currently saved tally:")
    _print_diff(old_tally, new_tally)

    TALLY_PATH.write_text(
        json.dumps(new_tally, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"\nSaved: {TALLY_PATH}")


if __name__ == "__main__":
    main()
