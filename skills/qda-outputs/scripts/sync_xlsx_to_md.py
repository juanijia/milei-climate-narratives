#!/usr/bin/env python3
"""
sync_xlsx_to_md.py  —  make the Excel 'Coded Passages' sheet the editable master.

Workflow: edit codes/memos in qda_v4_coded_corpus_261011.xlsx > 'Coded Passages', save, then
    python skills/qda-outputs/scripts/sync_xlsx_to_md.py            # DRY RUN: prints a diff, writes nothing
    python skills/qda-outputs/scripts/sync_xlsx_to_md.py --apply    # writes .md files, then refreshes tally + CSV

What you may edit in the sheet (columns B, C, D, E, G; all else ignored except F):
  B  Dimension (D1.1/D1.2/D1.3)   C  Sub-dimension  and  E  Sub-code (Full): same text, must match
  D  Dimension (Full), must start with the code in B     G  Analytical Memo
  F  Quoted Passage — identifies the row; do NOT edit it
Supported: change a code, change a memo, delete a row (removes that code), add a row by
copying an existing row of the SAME passage and changing B/E/G.
NOT supported (reported as errors, nothing is written): editing passage text, adding a
passage that is not already in the .md file (add it in the .md by hand, then rerun).

Safety: all-or-nothing (any error => no file is touched); only the `[CODE: ...]` lines
under a passage are rewritten, unchanged lines are kept byte-for-byte; after writing,
the .md files are re-parsed and must reproduce the sheet exactly or the script reports FAIL.
"""
import argparse, re, subprocess, sys, shutil
from collections import defaultdict
from pathlib import Path
import openpyxl
sys.path.insert(0, str(Path(__file__).parent))
import generate_xlsx as gx
from corpus_metadata import build_metadata_index
from corpus_data import (build_corpus, parse_speech_segments, validate_code,
                         _CODE_LINE_RE, _parse_code_tag)

ROOT = Path(__file__).parent.parent.parent.parent
CODED_DIR = ROOT / "analysis/coded_speeches/v4"
XLSX = ROOT / "analysis/results/v4/qda_v4_coded_corpus_261011.xlsx"   # MASTER workbook (edit this one)
REV = {v: k for k, v in gx.SUBCODE_DISPLAY.items() if "legacy" not in v}
norm = lambda s: re.sub(r"\s+", " ", s or "").strip()

def read_sheet(path):
    ws = openpyxl.load_workbook(path, data_only=True)["Coded Passages"]
    errs, rows = [], defaultdict(list)       # (speech, passage) -> [(dim, sub, memo)]
    for n, r in enumerate(ws.iter_rows(min_row=3, values_only=True), start=3):
        if r[0] is None and not r[5]:
            continue
        dim, disp, memo = norm(r[1]), norm(r[4]), norm(r[6])
        sub = REV.get(disp)
        if sub is None or sub not in gx.VALID_CODES.get(dim, []):
            errs.append(f"row {n}: invalid dim/sub-code '{dim} / {disp}'"); continue
        if norm(r[2]) != disp:
            errs.append(f"row {n}: column C (Sub-dimension) '{norm(r[2])}' must equal column E (Sub-code) '{disp}' — set both")
        if not norm(r[3]).startswith(dim):
            errs.append(f"row {n}: column D (Dimension Full) '{norm(r[3])}' does not match column B '{dim}'")
        if not memo:
            errs.append(f"row {n}: empty memo"); continue
        if "[CODE:" in memo:
            errs.append(f"row {n}: memo contains '[CODE:' (breaks the .md format)")
        rows[(norm(r[7]), norm(r[5]))].append((dim, sub, memo))
    return rows, errs

def plan(rows):
    meta, _ = build_metadata_index(ROOT, CODED_DIR)
    files, _ = build_corpus(CODED_DIR, meta)
    errs, changes, edits = [], [], {}
    unmatched = {k: list(v) for k, v in rows.items()}
    for f in files:
        path = CODED_DIR / f["filename"]
        segs = [s for s in f["segments"] if s["type"] == "coded"]
        lines = path.read_text(encoding="utf-8").split("\n")
        # locate code-line blocks (consecutive code lines, blanks allowed between)
        blocks, cur, last = [], [], None
        for i, ln in enumerate(lines):
            if _CODE_LINE_RE.match(ln.strip()):
                if cur and i - cur[-1] > 4: blocks.append(cur); cur = []
                cur.append(i)
            elif cur and ln.strip() and not ln.startswith("---") and not ln.strip().startswith(("#", "*[")):
                blocks.append(cur); cur = []
        if cur: blocks.append(cur)
        if len(blocks) != len(segs):
            errs.append(f"{f['filename']}: cannot align {len(blocks)} code blocks with {len(segs)} coded passages; edit by hand"); continue
        seen = defaultdict(int)
        for seg, blk in zip(segs, blocks):
            key = (f["speech"], norm(seg["text"]))
            occ = seen[key]; seen[key] += 1
            old = [(c["dim"], c["sub"], norm(c["memo"])) for c in seg["codes"]]
            if key not in rows:
                new = []        # passage absent from sheet => all its codes deleted
            else:
                new = unmatched[key] if occ == 0 else []
                if occ and key in unmatched:   # duplicate identical passage in one speech: share by order
                    new = old
            if key in unmatched and occ == 0: unmatched.pop(key)
            if new == old: continue
            old_lines = {(_parse_code_tag(_CODE_LINE_RE.match(lines[i].strip()).group(1)) + (norm(_CODE_LINE_RE.match(lines[i].strip()).group(2).strip().strip('*').strip()),)): lines[i] for i in blk}
            out = []
            for d, s, m in new:
                out.append(old_lines.get((d, s, m)) or f"`[CODE: {d} > {s}]` — *Memo: {m}*")
            edits.setdefault(path, []).append((blk, out))
            for o in old:
                if o not in new: changes.append(f"{f['filename']}\n   - {o[0]} > {o[1]}: {o[2][:70]}")
            for n_ in new:
                if n_ not in old: changes.append(f"{f['filename']}\n   + {n_[0]} > {n_[1]}: {n_[2][:70]}")
    for (sp, p), v in unmatched.items():
        errs.append(f"passage not found in any .md (edited text or new passage?): [{sp}] {p[:70]}…")
    return errs, changes, edits

def apply(edits):
    for path, blks in edits.items():
        shutil.copy2(path, path.with_suffix(".md.bak"))
        lines = path.read_text(encoding="utf-8").split("\n")
        for blk, out in sorted(blks, key=lambda b: -b[0][0]):
            first, lastl = blk[0], blk[-1]
            lines[first:lastl + 1] = out + ([""] if not out else [])
            # keep one blank line between code lines as in the original style
        txt = "\n".join(lines)
        txt = re.sub(r"(`\[CODE:[^\n]*)\n(?=`\[CODE:)", r"\1\n\n", txt)
        path.write_text(txt, encoding="utf-8")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true")
    ap.add_argument("--xlsx", default=str(XLSX)); a = ap.parse_args()
    rows, errs = read_sheet(a.xlsx)
    e2, changes, edits = plan(rows); errs += e2
    print(f"Sheet rows read: {sum(len(v) for v in rows.values())}")
    print(f"Changes to apply to .md files: {len(changes)} line(s) in {len(edits)} file(s)")
    for c in changes: print(" ", c)
    if errs:
        print(f"\nERRORS ({len(errs)}) — nothing written:"); [print("  !", e) for e in errs]; sys.exit(1)
    if not a.apply:
        print("\nDry run only. Re-run with --apply to write."); return
    apply(edits)
    meta, _ = build_metadata_index(ROOT, CODED_DIR); files, w = build_corpus(CODED_DIR, meta)
    got = defaultdict(list)
    for f in files:
        for r in f["flat_entries"]: got[(f["speech"], norm(r["passage"]))].append((r["dim"], r["sub_key"], norm(r["memo"])))
    ok = {k: sorted(v) for k, v in got.items()} == {k: sorted(v) for k, v in rows.items()} and not w
    print("Round-trip check:", "OK" if ok else "FAIL — restore from the .md.bak files")
    if not ok: sys.exit(2)
    for s in ("update_frequency_tally.py", "build_code_counts_csv.py", "generate_html.py"):
        subprocess.run([sys.executable, str(Path(__file__).parent / s)], check=True)
    print("\nDone. .md.bak backups kept next to edited files (delete when satisfied).")
    print("Still to do manually: re-run the quant notebook and update report/paper numbers if counts changed.")

if __name__ == "__main__":
    main()
