---
name: sync-coded-passages
description: >
  Pushes manual edits made in the 'Coded Passages' sheet of qda_v4_coded_corpus_261011.xlsx back into
  the coded .md files, then refreshes the frequency tally, the code-counts CSV and the HTML
  explorer. Use whenever the user says "I edited the Excel", "sync the coded passages",
  "update the md/csv from the xlsx", "I changed/added/removed a code", or after any manual
  correction of codes or memos. The xlsx is the single source of truth.
---

# sync-coded-passages

The xlsx `Coded Passages` sheet (`analysis/results/v4/qda_v4_coded_corpus_261011.xlsx`, the file shared with collaborators) is the master. Its extra note columns (N–Q: german, eli, juani, Highlights) and pivot table are ignored. Older variants are in `analysis/results/v4/OLD/`.
Everything else (coded `.md`, `frequency_tally_v4.json`, `milei_corpus_v4_code_counts.csv`,
`qda_explorer_v4.html`) is derived. Never edit derived files by hand.

## What the user edits in the sheet (one row = one code on one passage)
| Col | Header | Rule |
|---|---|---|
| B | Dimension | `D1.1`, `D1.2` or `D1.3` |
| C | Sub-dimension | same text as E |
| D | Dimension (Full) | must start with the code in B (e.g. `D1.3 — Cultural Backlash`) |
| E | Sub-code (Full) | exact display name of a v4 sub-code (e.g. `Woke Bundling`) |
| G | Analytical Memo | non-empty; no `[CODE:` text |
| F | Quoted Passage | **never edit** — it identifies the row |
Other columns (A, H–M) are ignored (speech/date/venue come from the master corpus database).
- **Add a code to a passage:** copy an existing row of that same passage, change B, C, D, E, G.
- **Remove a code:** delete its row.  **Change a code/memo:** edit B–E / G.
- A *new codebook code* is not covered: add it to `coding_book_v4.md`, `corpus_data.VALID_CODES` and `generate_xlsx.SUBCODE_DISPLAY` first (ask the researchers).

## Exact strings to type (columns B / D / C = E)
| B | D (Dimension Full) | C and E (same text) |
|---|---|---|
| D1.1 | D1.1 — State Intervention & Governance | Market Primacy · Anti-State / Anti-Bureaucratic · Anti-Casta (Elite Frame) · Delegitimization of Regulation · Sustainability as Ideological or Harmful · Rejection of Multilateral Governance |
| D1.2 | D1.2 — Public Science & Expertise | Attack on Universities & Research Institutions · Attack on Experts & Technocrats · Climate Skepticism or Dismissal · Pseudo-Science / Ideological Science · Selective Empiricism |
| D1.3 | D1.3 — Cultural Backlash | Woke Bundling · Anti-Socialism / Anti-Collectivism · Civilizational Defense |
(The dash in column D is an em dash "—".) Do not insert/delete columns before N, rename the sheet `Coded Passages`, or move the header off row 2. Changing the *text of the quoted passage* (column F) is not supported by the sync: ask Claude to edit the .md and the sheet together.

## What a change affects
- Memo only: `.md`, explorer HTML. No counts change.
- Recode within a dimension: sub-code counts (tally, CSV columns, rankings, co-occurrence, clusters, composition tables); dimension totals and `Codes_Total` unchanged.
- Recode across dimensions, add or delete a code: also dimension totals, `Codes_Total`, densities, venue-group mix, zero-code speech counts.
- After any count change: re-run `quant_analysis.ipynb` (Run All) and update numbers in the memo, `final_analysis_report_v4.md` and the paper; refresh the pivot table sheet in Excel/Sheets.

## Steps (run from project root)
1. Confirm the user has saved and closed the xlsx.
2. Dry run: `python skills/qda-outputs/scripts/sync_xlsx_to_md.py`. Show the user the diff (`-` removed, `+` added). If it prints ERRORS, nothing was written: explain each and have the user fix the sheet (or the .md for a brand-new passage), then repeat.
3. Only after the user confirms the diff: `python skills/qda-outputs/scripts/sync_xlsx_to_md.py --apply`. It rewrites the `[CODE: …]` lines (backups `*.md.bak`), verifies a round-trip re-parse equals the sheet (must print `Round-trip check: OK`), then runs `update_frequency_tally.py`, `build_code_counts_csv.py` and `generate_html.py`.
4. Report: number of changed lines/files, new total codes (CSV `Codes_Total`), and remind that `quant_analysis/` files and numbers in the report/paper are NOT refreshed automatically (re-run the quant notebook and update text if counts changed).
5. `generate_xlsx.py` refuses to overwrite the master; never point `--out` at it. Leave the `*.md.bak` files; tell the user they can delete them once satisfied.
