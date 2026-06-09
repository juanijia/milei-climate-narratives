---
name: qda-outputs
description: >
  Generates all post-coding deliverables from the v3 coded speech corpus: a QDA Excel
  workbook (coded passages + frequency tables), an interactive HTML corpus explorer
  (two reading modes, analytics charts, co-occurrence heatmap), and the final analysis
  report with rhetorical findings and research insights. Use this skill immediately after
  discourse-coder-v3 finishes coding — whenever the user says "generate the outputs",
  "create the Excel and HTML", "produce the final report", "generate QDA results",
  "wrap up Phase 3", "update the corpus file", or "I finished coding, now what?".
  This skill owns all three deliverables; do not generate them ad-hoc outside of it.
---

# QDA Outputs Generator

Produces three deliverables from the v3 coded corpus in `analysis/coded_speeches/v3/`:

| # | Deliverable | Path |
|---|---|---|
| 1 | QDA Excel workbook | `analysis/results/qda_v3_coded_corpus.xlsx` |
| 2 | Interactive HTML explorer | `analysis/results/qda_explorer_v3.html` |
| 3 | Final analysis report | `analysis/results/v3/final_analysis_report_v3.md` |

Run steps 1 and 2 via the bundled scripts (fast, deterministic). Write step 3 yourself
using the template and analytical guidance below.

---

## Prerequisites

Before running, confirm:
- `analysis/coded_speeches/v3/` contains at least one coded `.md` file
- `analysis/coded_speeches/v3/frequency_tally_v3.json` exists and is up to date
- `analysis/coding_book_v3.md` exists (needed for report context)
- `openpyxl` is available: `pip install openpyxl --break-system-packages -q`

Create the output directory if needed:
```bash
mkdir -p analysis/results/v3
```

---

## Step 1 — Generate the Excel Workbook

```bash
cd <project_root>
python skills/qda-outputs/scripts/generate_xlsx.py
```

The script reads every `[CODE: ...]` annotation from the coded speech files, maps each
one to a row, and builds four sheets:

- **Coded Passages** — one row per code annotation (passage, memo, speech metadata)
- **Freq — By Dimension** — COUNTIFS cross-tab: D1.1 / D1.2 / D1.3 / IND × each speech
- **Freq — By Sub-code** — COUNTIFS cross-tab: every sub-code × each speech
- **Speech Overview** — per-speech totals with D1/IND counts

All frequency sheets use live `COUNTIFS` formulas that auto-update if you add rows to
Coded Passages. Check the console output for the row count and any parse warnings.

---

## Step 2 — Generate the HTML Explorer

```bash
cd <project_root>
python skills/qda-outputs/scripts/generate_html.py
```

The script parses all coded speech files into full segment lists (plain paragraphs +
coded passages) and generates a self-contained HTML file with three tabs:

- **Corpus Browser** — reads each speech with two modes:
  - *Excerpts*: shows only coded passages, highlighted by dimension colour
  - *Full Speech*: complete text with coded passages highlighted inline
  - Dimension filter chips (D1.1 / D1.2 / D1.3 / IND) work in both modes
  - Clicking a passage opens its analytical memo in the side panel
- **Pattern Analysis** — frequency ranking bar chart, speech × sub-code heatmap,
  code co-occurrence grid (top 12 pairs)
- **Visualizations** — dimension summary KPIs, frequency bar chart, D1 sub-dimension
  breakdown per speech, code timeline, stacked bar per speech

The file is fully self-contained (no server needed — open directly in a browser).

---

## Step 3 — Write the Final Analysis Report

Write `analysis/results/v3/final_analysis_report_v3.md` using the template below.
This is the analytical centrepiece; take it seriously and write it as a research document,
not a summary. Draw on: the frequency tally JSON, the per-speech coding summaries appended
to each coded file, and the analytical observations recorded in those summaries.

### Report Template

```markdown
# Final Analysis Report v3: Milei's Climate Narratives
**Version:** 3.0 | **Date:** YYYY-MM-DD | **Coded by:** Claude (discourse-coder-v3)

---

## Executive Summary

[3–4 sentences. What is the overarching finding? What is the dominant rhetorical
mechanism? What does the corpus reveal about Milei's climate obstruction strategy?
Write this last, after completing the other sections.]

---

## Corpus Overview

- **Speeches coded:** N
- **Date range:** YYYY-MM-DD – YYYY-MM-DD
- **Total coded passages:** N
- **Total code annotations:** N (passages can carry multiple codes)
- **Venues:** [list]
- **V3 methodological change:** D2 (State Capability Erosion) codes removed from
  speech corpus; passages previously coded D2 re-coded as D1 where applicable.

---

## Dimension 1 — Discursive Delegitimization: Key Findings

Open with the aggregate D1 distribution (D1.1 / D1.2 / D1.3 as % of total D1 codes),
then give each sub-dimension its own subsection. Each subsection should: state the count
and % share, identify the dominant sub-codes, explain what rhetorical work they perform
in context, and cite 1–2 exemplary passages with brief analytical commentary.

### D1.1 — Delegitimization of State Intervention and Sustainability Governance
[Dominant sub-dimension. Discuss: which sub-codes lead (Rejection_of_Multilateral_
Governance is typically #1); how the market-failure-is-impossible argument forecloses
climate regulation at the theoretical level; how the anti-casta and anti-bureaucratic
frames personalize the institutional target; cross-speech patterns.]

### D1.2 — Delegitimization of Public Science and Expertise
[Explain what the relatively lower frequency (compared to D1.1) reveals: Milei's
obstruction targets state authority more than climate science per se — a distinctively
libertarian, not alt-right, pattern. Discuss the epistemic authority inversion
(Selective_Empiricism), the institutional capture narrative (Pseudo_Science), and the
expert-as-technocrat framing.]

### D1.3 — Woke / Cultural Backlash
[Explain the function of D1.3 as a meta-narrative that pre-loads every specific
argument with civilizational stakes. Discuss how Woke_Bundling contaminates climate
governance by association. Note the consistent Civilizational_Defense across all
international speeches (Davos + UN).]

---

## Inductive Categories

For each inductive category in the tally (Selective_Empiricism, Temporal_Appropriation,
Reported_Denial, any new ones):
- Definition and how it was recognized
- Frequency and which speeches it appears in
- Why existing D1 codes don't cover it
- Whether its frequency warrants promotion to a permanent deductive sub-code

**Temporal_Appropriation deserves extended treatment:** This is the most analytically
interesting inductive category. Explain how it works (co-opting sustainability's own
intergenerational vocabulary and directing it against sustainability governance), where
it appears, and what it reveals about Milei's rhetorical sophistication.

---

## Rhetorical Evolution Across the Corpus (2023–2026)

This section should read as a narrative arc, not a list. Track how the rhetoric develops:

- **2023 (Debate Presidencial):** Condensed, ad hominem, climate denial explicit
- **2024 (WEF Davos, UN 79th):** Theoretically elaborated; market-failure argument
  fully developed; counter-coalition bid; international audience recalibration
- **2025 (WEF Davos, UN 80th):** Five-cycles denial; civilizational framing peaks;
  Temporal_Appropriation emerges; institutional reform blueprint proposed
- **2026 (WEF Davos):** Values-order argument (ethics → efficiency → utility);
  rhetoric shifts from warning to victory narrative as political winds shift

Key analytical question: Is there a trajectory from D1.3 culture-war framing (candidate
register) toward D1.1 economic-foundational arguments (governing president register)?
Answer it with data from the frequency tally.

---

## Co-occurrence Patterns and Rhetorical Bundles

Identify the top code pairs that appear together in the same passage. Explain what each
bundling achieves rhetorically (e.g., D1.3 > Neo_Marxism + D1.3 > Woke_Bundling = the
climate-is-socialism argument in one move). Co-occurrence data is available in the HTML
explorer's Pattern Analysis tab.

---

## Key Quotes and Exemplary Passages

Select 6–8 passages that best illustrate the key rhetorical mechanisms. For each:
- Quote the passage (in original Spanish, with English translation in brackets)
- State the code(s) applied
- 3–5 sentences of analytical commentary explaining the rhetorical strategy

Prioritise passages that do more than one thing at once (stacked codes), that appear in
unexpected contexts, or that demonstrate evolution in the rhetoric.

---

## Notes for Triangulation with Dimension 2 (Corpus B)

D2 (State Capability Erosion) applies to formal documentation — decrees, budget records,
reorganization orders — not speeches. This report documents the discursive layer.
Note which D1 findings most urgently require triangulation with D2 evidence:
- Which institutional frameworks does Milei rhetorically delegitimize in these speeches?
- What formal policy actions (D2) would confirm or extend the D1 pattern?
- Which speeches contain the most direct rhetorical preludes to institutional action?

---

## Conclusions and Next Steps

Summarize the 3–4 core findings as numbered claims, each backed by specific evidence
from the analysis. End with concrete next steps: which new speeches to code (Apertura
de Sesiones Ordinarias, for example), what D2 documents to collect, and whether any
inductive categories are ready for formalization.
```

---

## Analytical Anchors

These observations from the v3 coding should inform your report — verify against the
actual tally, confirm or update as needed:

**On the dominant mechanism:**
D1.1 (State/Governance) accounts for roughly 55% of D1 codes. The single most frequent
sub-code is `Rejection_of_Multilateral_Governance`. This tells us Milei's primary
obstruction target is state authority over sustainability governance, not climate science
per se — a distinctively libertarian pattern vs. the populist alt-right pattern that
leads with climate denial.

**On the science/expertise axis:**
D1.2 at ~18% is notable for being *lower* than D1.3 (Cultural Backlash, ~26%). The
`Selective_Empiricism` inductive category bridges D1.1 and D1.2: Milei appropriates
empirical authority for his own economic claims while denying it to climate institutions.

**On Temporal_Appropriation:**
The most analytically distinctive inductive find. Milei hijacks sustainability's core
moral vocabulary — intergenerational responsibility, protecting the future — and redirects
it against sustainability governance itself ("quienes incendian el futuro"). It turns the
opponent's strongest rhetorical asset into a weapon against them.

**On international forum speeches:**
The UN and Davos speeches carry a disproportionate share of `Rejection_of_Multilateral_
Governance` codes, which makes sense structurally — they are delivered *at* the targeted
institutions. The rhetoric is calibrated for those audiences: the UN speech deploys
South-South framing (climate policy harms poor countries) absent from the Davos speeches.

**On the 2023 → 2026 arc:**
The 2023 debate speech is the only one with outright climate denial (`Climate_Skepticism_
or_Dismissal`). By 2026, explicit denial has given way to philosophical argumentation
(the Hoppe property-rights proof, the Huerta de Soto dynamic efficiency theorem). The
rhetoric becomes *less* anti-science and *more* anti-state as Milei transitions from
candidate to president — a shift worth theorizing in the report.

---

## Output Paths

| File | Path |
|---|---|
| Excel workbook | `analysis/results/qda_v3_coded_corpus.xlsx` |
| HTML explorer | `analysis/results/qda_explorer_v3.html` |
| Final report | `analysis/results/v3/final_analysis_report_v3.md` |

All three should be committed together. The Excel and HTML are regenerated automatically
from the coded corpus whenever the corpus changes; the report is the interpretive layer
and is written/revised manually.
