---
description: Phase 3 workflow for performing narrative and thematic analysis — v4.
---
# The Narrative Analyst Agent Workflow (v4)

**Goal:** Apply the v4 abductive coding framework to all speech files in `data/raw_speeches/`, save coded outputs to `analysis/coded_speeches/v4/`, then generate the three deliverables via the qda-outputs skill.

**Status (2026-07-19):** The v3→v4 recoding manifest has already been applied to the first 9 speeches (see `analysis/coded_speeches/v4/frequency_tally_v4.json` for the list). The remaining ~183 speeches in the full corpus have not been coded yet and are the current focus. Work through them in **batches of 5**, oldest-first.

## The master corpus database

`data/sources/milei_discursos_index_2023-2026_updated260718.csv.csv` is the authoritative tracker for the full corpus (192 rows — every Milei speech/discourse Dec 2023–Apr 2026, not only climate-relevant ones). Columns:

| Column | Meaning |
|---|---|
| `id` | stable row id |
| `fecha`, `anio` | date, year |
| `lugar`, `pais` | venue, country |
| `evento-discurso` | event/speech title |
| `tipo`, `subtipo` | broad category / narrower subcategory (23 `tipo` values, see CLAUDE.md) |
| `clima` | climate-relevance heuristic: `✔` high, `~` possible (needs reading), blank = unlikely |
| `link` | source URL (casarosada.gob.ar in most cases) |
| `coded` | **`ok` once the speech has a v4-coded file in `analysis/coded_speeches/v4/`; blank otherwise** |

**Before starting a batch:** filter the CSV for `coded` blank, prioritizing `clima = ✔` and `clima = ~` rows first (the corpus was built to over-include possible climate relevance; blank-`clima` rows are lowest priority and may be skipped entirely if time is limited — flag this decision rather than silently coding everything).

**Matching a CSV row to a raw-speech file:** the CSV has no filename column. Match by date + event keywords, or by URL against `data/raw_speeches/collection_log.md` (which maps each source URL to its saved filename). Dates can be off by a day between the CSV (casarosada listing date) and the raw file's frontmatter `date` — match on event description when in doubt.

**After coding each speech:** set that row's `coded` column to `ok` in the CSV (this is the running progress record other agents and the researchers will check).

## Steps

1. **Read the v4 skill**: Open `skills/discourse-coder-v4/SKILL.md` and follow it fully. All coding instructions, annotation format, and output rules are defined there.

2. **Read the v4 codebook**: `analysis/coding_book_v4.md` — do this before touching any speech file. Each deductive sub-code now includes 3 worked examples; use them to calibrate borderline decisions.

3. **Read the v4 methodology summary**: `analysis/methodology_summary_v4.md` — contains the recoding manifest (v3→v4 changes) and the rationale for each change. (Historical — already applied to the first 9 speeches; read for context, not action.)

4. **Confirm no higher version exists**: Check `skills/` and `analysis/` for a `discourse-coder-v5` / `coding_book_v5.md` before starting. If one exists, use it instead and flag the discrepancy to the researchers — do not silently keep coding under v4.

5. **Select the next batch of 5**: Using the master CSV (`coded` blank, `clima` ✔/~ first), pick the next 5 uncoded speeches in chronological order and confirm each has a raw file in `data/raw_speeches/`.

6. **Code the batch**: Perform first-pass v4 coding on each of the 5 files using `skills/discourse-coder-v4/SKILL.md`. Save to `analysis/coded_speeches/v4/<same_filename>.md`.

7. **Update tracking after the batch**: Run `python skills/qda-outputs/scripts/update_frequency_tally.py` to regenerate `analysis/coded_speeches/v4/frequency_tally_v4.json` directly from the coded files (it is no longer hand-edited — see the Frequency Tracking section of `skills/discourse-coder-v4/SKILL.md`), and mark the corresponding rows `coded = ok` in the master CSV. Then run `build_code_counts_csv.py` to refresh `milei_corpus_v4_code_counts.csv`. Once a workbook exists, later manual corrections are made in the xlsx and pushed back with `sync_xlsx_to_md.py` (see CLAUDE.md, "Single Source of Truth").

8. **Repeat** for the next batch of 5 until the corpus is exhausted.

9. **Generate outputs**: Once the full corpus is coded, use the **qda-outputs** skill to produce:
   - `analysis/results/v4/qda_v4_coded_corpus_261011.xlsx` (master; see CLAUDE.md "Single Source of Truth")
   - `analysis/results/v4/qda_explorer_v4.html`
   - `analysis/results/v4/final_analysis_report_v4.md`
