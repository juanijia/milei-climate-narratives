# AGENTS.md — Milei Climate Narratives Research Project

This file is the primary reference for any AI agent working on this project. Read it fully before taking any action.

---

## Project Overview

**Research goal:** Analyze Javier Milei's speeches and public discourses to map how his rhetoric constructs narratives that obstruct climate policy in Argentina. The analysis uses an **abductive (inductive-deductive) approach**: starting from theoretically derived seed categories and allowing novel patterns to emerge from the data.

**Academic context:** This is a qualitative political discourse analysis embedded in the broader literature on right-wing climate obstruction, particularly in the Global South. Key references are in `docs/references/`. The research abstract is in `docs/abstract/Abstract.md` and the paper draft is in `docs/Draft/draft_20260718.md` (a manually maintained Word version, `Borrador Manuscrito.docx`, also lives there).

**Researchers:** Germán Bersalli, Elizabeth Mohle, Juan Ignacio Arroyo.

---

## Directory Structure

```
milei-climate-narratives/
├── AGENTS.md                        ← You are here
├── implementation_plan.md           ← Original project plan (manually kept in sync with reality)
├── docs/
│   ├── abstract/                    ← Abstract.md (research goals & framing)
│   ├── Draft/                       ← draft_20260718.md, Borrador Manuscrito.docx (paper draft)
│   ├── methodology/                 ← Methodology PDFs (discourse analysis, lecture slides, diagrams)
│   └── references/                  ← Academic PDFs on climate obstruction in Argentina & Latin America
├── data/
│   ├── sources/
│   │   ├── milei_discursos_index_2023-2026_updated260718.csv.csv
│   │   │                            ← MASTER CORPUS DATABASE — see "The Master Corpus Database" below
│   │   ├── milei_discursos_index_2023-2026.md / .csv   ← earlier auto-generated index (superseded by the file above)
│   │   ├── Notes.xlsx                ← original seed list of URLs (superseded, kept for provenance)
│   │   └── candidate_sources_log.md
│   ├── raw_speeches/                ← Full scraped corpus as .md files (Phase 2 output — complete, 192 files)
│   │   └── collection_log.md        ← maps each source URL to its saved filename
│   └── processed/                   ← NOT USED. Coded outputs go to analysis/coded_speeches/, not here.
├── analysis/
│   ├── coding_book.md / _v2.md / _v3.md / _v4.md / _v4_proposal.md
│   │                                ← versioned codebooks — CURRENT VERSION: v4 (`coding_book_v4.md`)
│   ├── methodology_summary.md / _v2.md / _v3.md / _v4.md
│   │                                ← versioned methodology notes and change logs, one per codebook version
│   ├── coded_speeches/              ← coded speech outputs (NOT data/processed/coded/ — see note above)
│   │   ├── v1/ … v4/                ← one folder per coding pass; each has its own frequency_tally_v#.json
│   │   └── v4/                      ← COMPLETE — all 193 speech events coded (196 files incl. 3 non-counted duplicate transcripts)
│   └── results/
│       ├── v3/final_analysis_report_v3.md
│       ├── v4/                      ← qda_v4_coded_corpus.xlsx, qda_explorer_v4.html, final_analysis_report_v4.md, milei_corpus_v4_code_counts.csv — ALL COMPLETE (2026-07-19)
│       └── qda_explorer_v2.html, qda_v2_coded_corpus_v2.xlsx, qda_v3_coded_corpus*.xlsx  ← earlier-version outputs, kept for provenance
├── workflows/                       ← Agent instruction files (read before starting each phase)
│   ├── 1_methodologist.md
│   ├── 2_data_collector.md
│   └── 3_narrative_analyst.md       ← always check this reflects the current codebook version before running Phase 3
└── skills/                          ← Project-specific agent skills (NOT agent/skills/)
    ├── discourse-coder/ , -v2/ , -v3/ , -v4/    ← versioned coding skills — CURRENT: discourse-coder-v4
    ├── qda-outputs/                 ← generates the xlsx/html/report deliverables from a coded corpus
    ├── speech-collector/, youtube-transcript/
    ├── skill-creator/, caveman/
    └── SKILLS_ANALYSIS.md
```

---

## Current Project Status

| Phase | Agent | Status |
|-------|-------|--------|
| Phase 1 — Methodology & Codebook | Methodologist | ✅ Complete (now on codebook v4) |
| Phase 2 — Data Collection | Data Collector | ✅ Complete — 192/192 speeches collected in `data/raw_speeches/`, indexed in the master corpus database |
| Phase 3 — Narrative Analysis | Narrative Analyst | ✅ Complete — coding book **v4**, all 193 speech events coded, all 193 master-CSV rows `coded=ok`, `qda-outputs` deliverables generated (2026-07-19) |

**Next step:** Phase 3 is done. Remaining work is (a) formal D2 (State Capability Erosion) documentation collection — see `final_analysis_report_v4.md`'s "Notes for Triangulation with Dimension 2" for the priority list, anchored on the 2025-11-13 periglaciares/glacier-law passage — and (b) incorporating `final_analysis_report_v4.md`'s findings into the paper draft (`docs/Draft/draft_20260718.md`). If new Milei speeches are delivered going forward, code them into `analysis/coded_speeches/v4/` following the same protocol and re-run `qda-outputs` to refresh the three deliverables.

### Always check for the latest version before starting Phase 3 work

The coding framework has gone through 4 iterations (v1–v4), each with its own codebook (`analysis/coding_book_v#.md`), skill (`skills/discourse-coder-v#/`), methodology summary, and output folder (`analysis/coded_speeches/v#/`). **Before coding anything:**

1. Check `skills/` for the highest-numbered `discourse-coder-v#` folder and `analysis/` for the highest-numbered `coding_book_v#.md`. Use only the highest version — do not mix versions.
2. Check `workflows/3_narrative_analyst.md` — its header states which version it targets. If it lags behind the highest available codebook/skill version, flag the mismatch to the researchers rather than guessing which is authoritative.
3. Check `analysis/coded_speeches/v#/frequency_tally_v#.json` for that version's `files_coded` list, and cross-reference with the `coded` column in the master corpus database (below), to see what's already done.
4. Never modify outputs in a lower-numbered `analysis/coded_speeches/v#/` folder — those are frozen historical passes.

---

## The Master Corpus Database

`data/sources/milei_discursos_index_2023-2026_updated260718.csv.csv` is the **authoritative tracker for the full corpus** — all 192 Milei speeches/discourses as President (Dec 2023–Apr 2026), not only the climate-relevant ones. It supersedes `milei_discursos_index_2023-2026.md`/`.csv` and `Notes.xlsx`, which are kept only for provenance. Manually curated by the researchers; do not regenerate it from the older files.

**Columns:**

| Column | Meaning |
|---|---|
| `id` | stable row id |
| `# (outdated)` | legacy row number from the earlier index — ignore |
| `fecha`, `anio` | date (YYYY-MM-DD), year |
| `lugar`, `pais` | venue, country (all lowercase, no special characters) |
| `evento-discurso` | event/speech title |
| `tipo`, `subtipo` | broad category (23 values) / narrower subcategory — see list below |
| `clima` | climate-relevance heuristic: `✔` high, `~` possible (needs reading to confirm), blank = unlikely |
| `link` | source URL (mostly casarosada.gob.ar) |
| `coded` | `ok` once the speech has a corresponding file in `analysis/coded_speeches/v4/`; all 193 rows are `ok` as of 2026-07-19 |

**`tipo` values** (23, decreasing frequency): acto institucional, foro economico, evento ideologico/politico, premio / reconocimiento, fundacion / think tank, bilateral / diplomatico, cumbre internacional, bolsa / camara de comercio, empresa, cadena nacional, sectorial, acto conmemorativo/patrio, consejo empresarial, clase magistral / universidad, acto conmemorativo, foro economico / empresarial, comunitario / religioso, organismo internacional, foro economico / financiero, evento empresarial, evento economico / cultural, debate presidencial, acto institucional / bilateral.

**`pais` values** (14, decreasing frequency): argentina, ee.uu., israel, españa, suiza, paraguay, brasil, uruguay, italia, hungria, rep. checa, el salvador, chile, alemania.

**Using it during Phase 3:**
- Filter for `coded` blank to find what remains; prioritize `clima = ✔`, then `~`. Blank-`clima` rows are lowest priority for a climate-obstruction analysis and may be deferred or skipped — flag that decision rather than silently coding everything.
- The CSV has **no filename column**. Match a row to its raw-speech file by date + event keywords, or via `data/raw_speeches/collection_log.md` (source URL → filename). The CSV's `fecha` (casarosada listing date) can differ by a day from the raw file's frontmatter `date` — match on the event description when in doubt.
- After coding a speech, set its row's `coded` value to `ok`. This is the shared progress record — keep it current so the next agent (or researcher) can see what's left without re-deriving it.

---

## Skills

This project uses skills located at `skills/` (not `agent/skills/`).

User-level skills (available in all sessions):
- `caveman` — compress communication mode to save tokens.
- `skill-creator` — use when creating or improving skills.

Data collector agent uses:
- `speech-collector` (`skills/speech-collector/SKILL.md`) — scrape text from URLs into structured Markdown files.
- `youtube-transcript` (`skills/youtube-transcript/SKILL.md`) — extract transcripts from YouTube videos.

Narrative analyst agent uses:
- `discourse-coder-v4` (`skills/discourse-coder-v4/SKILL.md`) — the current coding skill for Phase 3. Applies Dimension 1 (Discursive Delegitimization) exclusively to speech data. Always use the highest-numbered version present (see "Always check for the latest version" above) — do not use `discourse-coder`, `-v2`, or `-v3` for new coding work.
- `qda-outputs` (`skills/qda-outputs/SKILL.md`) — once a corpus version is fully coded, generates the Excel workbook, HTML explorer, and feeds the final analysis report.

---

## The Three Agent Workflows

### Agent 1 — The Methodologist (Phase 1) — COMPLETE

**Workflow file:** `workflows/1_methodologist.md`

**What it did:**
- Read all PDFs in `docs/methodology/` and `docs/references/`
- Reviewed the research abstract in `docs/abstract/Abstract.md`
- Extracted the analytical pillars into `analysis/coding_book.md`, since revised through three peer-reviewed iterations to `analysis/coding_book_v4.md`
- Wrote methodology summaries (`analysis/methodology_summary.md` through `_v4.md`)

**Output:** `analysis/coding_book_v4.md` (current) and its methodology summary are ready.

---

### Agent 2 — The Data Collector (Phase 2) — COMPLETE

**Workflow file:** `workflows/2_data_collector.md`

**What it did:** Populated `data/raw_speeches/` with all 192 speeches/discourses in the master corpus database (Dec 2023–Apr 2026), each with full verbatim transcription, sourced primarily from Casa Rosada's official "Discursos" registry. Logged every source in `data/raw_speeches/collection_log.md`.

**File naming convention:**
```
data/raw_speeches/YYYY-MM-DD-keyword-slug.md
```
Example: `2024-09-24-milei-un-general-assembly.md`

**Frontmatter template for each speech file:**
```markdown
---
title: "[Speech or article title]"
date: YYYY-MM-DD
source_url: "https://..."
source_type: speech | interview | tweet_thread | article | youtube
language: es
youtube_transcript: true | false
summary_en: "[Brief 1-2 sentence summary in English]"
---

[Full speech/article text in original language]
```

**Language note:** Milei's speeches are primarily in Spanish. Kept in their original language — not translated.

---

### Agent 3 — The Narrative Analyst (Phase 3) — COMPLETE (v4, 193/193 coded)

**Workflow file:** `workflows/3_narrative_analyst.md` — read this in full before coding; it has the current batch process and the master-database bookkeeping steps.

**Critical inputs (read before touching any speech file):**
- `analysis/coding_book_v4.md` — defines all D1 analytical categories, each now with 3 worked examples per sub-code
- `skills/discourse-coder-v4/SKILL.md` — annotation format, overcoding rule, output rules
- `data/sources/milei_discursos_index_2023-2026_updated260718.csv.csv` — which speeches remain to be coded

**Key steps (summary — full detail in the workflow file):**
1. Confirm v4 is still the latest codebook/skill version.
2. Pick the next batch of 5 uncoded speeches from the master database (climate-relevant first, chronological order).
3. Code each with `skills/discourse-coder-v4/SKILL.md`, saving to `analysis/coded_speeches/v4/<same_filename>.md`.
4. Update `analysis/coded_speeches/v4/frequency_tally_v4.json` and mark the corresponding CSV rows `coded = ok`.
5. Repeat until the corpus is exhausted, then generate `analysis/results/v4/final_analysis_report_v4.md` via the `qda-outputs` skill.

**Status: all 5 steps complete as of 2026-07-19.** All 193 speech events are coded, all master-CSV rows are `coded=ok`, and all three `qda-outputs` deliverables (`qda_v4_coded_corpus.xlsx`, `qda_explorer_v4.html`, `final_analysis_report_v4.md`) have been generated from the complete corpus (538 total D1 code annotations; see the final report's Executive Summary for headline findings). A quantitative per-speech code-count CSV (`analysis/results/v4/milei_corpus_v4_code_counts.csv` — the master corpus database plus one column per sub-code/sub-dimension) was also produced for statistical analysis. Note: `skills/qda-outputs/scripts/generate_xlsx.py` had a latent bug that broke once the corpus exceeded 24 speeches (single-letter Excel column assumption); this was fixed in this pass (now uses `column_index_from_string`) and should not need revisiting.

---

## The Codebook — Summary

Full codebook: `analysis/coding_book_v4.md` (current version — see versioning note above).

**v4 covers Dimension 1 (Discursive Delegitimization) only, applied to speeches.** Dimension 2 (State Capability Erosion) is a separate protocol applied to formal documentation (decrees, budgets), not speeches.

**Deductive categories (v4):**

| Sub-dimension | Sub-codes |
|---|---|
| D1.1 — State Intervention & Sustainability Governance | Market_Primacy, Anti_State_Anti_Bureaucratic, Anti_Casta, Delegitimization_of_Regulation, Sustainability_as_Ideological_or_Harmful, Rejection_of_Multilateral_Governance |
| D1.2 — Public Science & Expertise | Attack_on_Universities_and_Research_Institutions, Attack_on_Experts_and_Technocrats, Climate_Skepticism_or_Dismissal, Pseudo_Science_or_Ideological_Science, Selective_Empiricism |
| D1.3 — Cultural Backlash | Woke_Bundling, Anti_Socialism_Anti_Collectivism, Civilizational_Defense |

**Retired/renamed in v4 — do not apply:** `Temporal_Appropriation` (eliminated, see watchlist in codebook), `Reported_Denial` (retired), `Deregulation_Benefits` (merged into `Delegitimization_of_Regulation`), `Rejection_of_Expert_Mediation` (absorbed into `Attack_on_Experts_and_Technocrats`), `Neo_Marxism` (renamed `Anti_Socialism_Anti_Collectivism`).

**Inductive categories:** none active in the complete v4 corpus (0 instances in the final tally). Two candidate patterns were observed but not formalized (theological/dominion framing; primitivism-as-regulation metaphor) — see `final_analysis_report_v4.md`'s "Inductive Categories" section.

---

## Key Academic Concepts (Context for Agents)

- **Abductive coding:** Neither purely top-down (deductive) nor purely bottom-up (inductive). Start with seed categories, remain open to revising or expanding them based on what the data shows.
- **Discourse analysis:** The unit of analysis is language — not just what Milei says, but *how* he says it, what rhetorical moves he makes, and what social/political effects those moves have.
- **Climate obstruction:** The focus is on how rhetoric actively undermines climate policy, not just expresses skepticism. Track both discursive moves (this project's D1 scope) and, separately, their links to concrete policy actions (D2 scope — formal documentation, not speeches).
- **La casta:** Milei's central political frame positioning the political establishment as an extractive class. Watch for how climate institutions get folded into this narrative (`Anti_Casta`).
- **Anti_Socialism_Anti_Collectivism framing (formerly "Neo-Marxism" in Milei's own vocabulary):** In Milei's rhetoric, environmentalism is frequently coded as a disguised socialist/collectivist project.

---

## File and Naming Conventions

- All agent-generated files go into the directories specified above — never in the project root
- Speech files: `YYYY-MM-DD-slug.md` in `data/raw_speeches/`
- Coded files: same filename, in `analysis/coded_speeches/v<current>/` (not `data/processed/`)
- All log files use the suffix `_log.md`
- Intermediate notes or drafts: prefix with `_draft_` (these can be deleted later)
- Do not rename or move files in `docs/`, `analysis/coding_book_v4.md`, or the master corpus database without the researcher's approval

---

## Important Constraints

- **Language:** Preserve all speech content in the original Spanish. Do not translate primary sources. Coding memos are written in English.
- **Copyright:** Do not reproduce full copyrighted academic articles. Quote only short passages when needed for coding memos.
- **Source integrity:** Every source URL is recorded in `data/raw_speeches/collection_log.md`. If a URL is broken or inaccessible, log it with status `FAILED` and move on.
- **Codebook authority:** `analysis/coding_book_v4.md` (or the highest-numbered version present) is the single source of truth for coding decisions. Do not invent codes without adding them to the codebook first, following the inductive category protocol.
- **Scope (revised 2026-07-19, Option A adopted — see `analysis/_draft_v4_batch2_consistency_audit.md`):** The corpus-level filter (the master database's `clima` column) is a *speech-selection* heuristic only — prioritize `clima = ✔`, then `~`, when picking which speeches to code next. It is **not** a passage-level coding filter. Once a speech is selected for coding, do **not** additionally require an explicit climate/environmental/2030-Agenda mention in a given passage before applying a D1.1/D1.2/D1.3 code. General anti-`casta`, anti-state/anti-bureaucratic, anti-regulation, market-primacy, anti-expert, and anti-collectivist rhetoric is codeable on its own terms wherever it appears — per D1.1's own framing in `coding_book_v4.md` ("weakens the public and epistemic grounds for state action on climate... regardless of whether formal commitments remain in place"), this rhetoric constitutes the discursive infrastructure of climate obstruction even when a passage never names climate or the environment. See `coding_book_v4.md` §"Instructions for the Analyst Agent" for the formal rule and worked boundary example. (Previously this line required climate-adjacent content per-passage; that stricter reading produced a documented under-coding inconsistency in the first non-pre-filtered batch — see the audit file.)

## Imported Claude Cowork project instructions
