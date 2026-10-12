#!/usr/bin/env python3
"""
build_code_counts_csv.py
Regenerates analysis/results/v4/milei_corpus_v4_code_counts.csv from the coded .md
files (via corpus_data.build_corpus) + the master corpus database. Previously this
CSV had no generator and drifted (538 vs the true 613 codes).

Row -> file matching: reuses the existing CSV's `matched_coded_file` column (stable,
already researcher-verified); only rows lacking a match fall back to date + filename.
The master database itself is read-only here and never modified.

Usage (project root):  python skills/qda-outputs/scripts/build_code_counts_csv.py [--dry-run]
"""
import argparse, sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
from corpus_metadata import build_metadata_index, group_for_tipo
from corpus_data import build_corpus, VALID_CODES

ROOT = Path(__file__).parent.parent.parent.parent
CODED_DIR = ROOT / "analysis/coded_speeches/v4"
MASTER = ROOT / "data/sources/milei_discursos_index_2023-2026_updated260718.csv.csv"
OUT = ROOT / "analysis/results/v4/milei_corpus_v4_code_counts.csv"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    meta, _ = build_metadata_index(ROOT, CODED_DIR)
    files, _ = build_corpus(CODED_DIR, meta)
    per_file = {}
    for f in files:
        c = {}
        for r in f["flat_entries"]:
            k = f"{r['dim']}_{r['sub_key']}"
            c[k] = c.get(k, 0) + 1
        per_file[f["filename"]] = c

    master = pd.read_csv(MASTER)
    old = pd.read_csv(OUT) if OUT.exists() else None
    match = dict(zip(old["id"], old["matched_coded_file"])) if old is not None else {}
    master["matched_coded_file"] = master["id"].map(match)
    for i, row in master[master["matched_coded_file"].isna()].iterrows():
        cand = [n for n in per_file if n.startswith(str(row["fecha"]))]
        master.at[i, "matched_coded_file"] = cand[0] if len(cand) == 1 else None
    miss = master["matched_coded_file"].isna().sum()
    if miss: print(f"WARNING: {miss} master rows without a matched coded file")

    # Derived grouping columns (the master database itself is never modified):
    # venue_group from corpus_metadata.TIPO_GROUP (same mapping as the xlsx 'Venue Group'),
    # scope = National if pais == argentina else International.
    master.insert(master.columns.get_loc("subtipo") + 1, "venue_group", master["tipo"].map(group_for_tipo))
    master.insert(master.columns.get_loc("venue_group") + 1, "scope",
                  master["pais"].str.lower().map(lambda p: "National" if p == "argentina" else "International"))
    unc = (master["venue_group"] == "Unclassified").sum()
    if unc: print(f"WARNING: {unc} rows with Unclassified venue_group: {master.loc[master.venue_group=='Unclassified','tipo'].unique()}")

    cols = []
    for dim in ("D1.1", "D1.2", "D1.3"):
        for s in VALID_CODES[dim]:
            col = f"{dim}_{s}"; cols.append(col)
            master[col] = master["matched_coded_file"].map(lambda fn: per_file.get(fn, {}).get(col, 0))
        master[f"{dim}_Total"] = master[[f"{dim}_{s}" for s in VALID_CODES[dim]]].sum(axis=1)
    master["Inductive_Total"] = master["matched_coded_file"].map(
        lambda fn: sum(v for k, v in per_file.get(fn, {}).items() if k.startswith("IND_")))
    master["Codes_Total"] = master[["D1.1_Total", "D1.2_Total", "D1.3_Total", "Inductive_Total"]].sum(axis=1)

    used = set(master["matched_coded_file"].dropna())
    orphan = {n: sum(c.values()) for n, c in per_file.items() if n not in used and sum(c.values())}
    if orphan: print("WARNING: coded files with codes but no master row (NOT counted in CSV):", orphan)
    total_md = sum(sum(c.values()) for c in per_file.values())
    print(f"CSV Codes_Total = {master['Codes_Total'].sum()}  |  all .md codes = {total_md}")
    print(master.groupby("venue_group").agg(speeches=("id", "count"), codes=("Codes_Total", "sum")).to_string())
    if a.dry_run: return
    master.to_csv(OUT, index=False)
    print("Saved:", OUT)

if __name__ == "__main__":
    main()
