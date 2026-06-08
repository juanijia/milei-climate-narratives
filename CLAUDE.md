# CLAUDE.md — Milei Climate Narratives Research Project

This file is the primary reference for any AI agent working on this project. Read it fully before taking any action.

---

## Project Overview

**Research goal:** Analyze Javier Milei's speeches and public discourses to map how his rhetoric constructs narratives that obstruct climate policy in Argentina. The analysis uses an **abductive (inductive-deductive) approach**: starting from theoretically derived seed categories and allowing novel patterns to emerge from the data.

**Academic context:** This is a qualitative political discourse analysis embedded in the broader literature on right-wing climate obstruction, particularly in the Global South. Key references are in `docs/references/`. The research abstract is in `docs/abstract/Abstract.docx`.

**Principal researcher:** Juan Ignacio Arroyo (j.ignacioarroyo@gmail.com)

---

## Directory Structure

```
milei-climate-narratives/
├── CLAUDE.md                   ← You are here
├── implementation_plan.md      ← Original project plan
├── docs/
│   ├── abstract/               ← Abstract.docx (research goals & framing)
│   ├── methodology/            ← Methodology PDFs (discourse analysis, lecture slides, diagrams)
│   └── references/             ← Academic PDFs on climate obstruction in Argentina & Latin America
├── data/
│   ├── sources/                ← Notes.xlsx (URLs and metadata for speeches/interviews)
│   ├── raw_speeches/           ← Scraped speech texts as .md files (output of Phase 2)
│   └── processed/              ← Cleaned & coded speech files (output of Phase 3)
│       └── coded/              ← Annotated versions with coding labels applied
├── analysis/
│   ├── coding_book.md          ← THE CODEBOOK — defines all analytical categories
│   └── results/
│       ├── methodology_summary.md   ← Phase 1 output (complete)
│       └── final_analysis_report.md ← Phase 3 output (to be created)
├── workflows/                  ← Agent instruction files (read before starting each phase)
│   ├── 1_methodologist.md
│   ├── 2_data_collector.md
│   └── 3_narrative_analyst.md
└── agent/
    └── skills/                 ← Project-specific agent skills
```

---

## Current Project Status

| Phase | Agent | Status |
|-------|-------|--------|
| Phase 1 — Methodology & Codebook | Methodologist | ✅ Complete |
| Phase 2 — Data Collection | Data Collector | 🔲 Not started |
| Phase 3 — Narrative Analysis | Narrative Analyst | 🔲 Waiting on Phase 2 |

`data/raw_speeches/` and `data/processed/` are currently empty. Phase 2 must run first.

## Skills
This project uses skills located at `agent/skills/`

User-level skills (available in all sessions):
- caveman - use to save token consumption by compressing communication mode.
- skill-creator - use when creating or improving skills

Data collector agent uses the following skills:
- speech-collector skill located at `skills/speech-collector/SKILL.md` used to scrap text from URLs and save them as structured Markdown files.
- youtube-transcript skill located at `skills/youtube-transcript/SKILL.md` used to extract transcripts from youtube videos.

Narrative analyst agent uses the following skills:
- discourse-coder-v3 skill located at `skills/discourse-coder-v3/SKILL.md` — the current coding skill for Phase 3. Applies Dimension 1 (Discursive Delegitimization) exclusively to speech data. Always use this version, not discourse-coder or discourse-coder-v2.

---

## The Three Agent Workflows

### Agent 1 — The Methodologist (Phase 1) — COMPLETE

**Workflow file:** `workflows/1_methodologist.md`

**What it did:**
- Read all PDFs in `docs/methodology/` and `docs/references/`
- Reviewed the research abstract in `docs/abstract/Abstract.docx`
- Extracted four analytical pillars from the conceptual diagram and wrote them into `analysis/coding_book.md`.
- Wrote a methodology summary to `analysis/results/methodology_summary.md`

**Output:** `analysis/coding_book.md` and `analysis/results/methodology_summary.md` are ready.

---

### Agent 2 — The Data Collector (Phase 2) — TO BE RUN NEXT

**Workflow file:** `workflows/2_data_collector.md`

**Primary task:** Populate `data/raw_speeches/` with Milei's climate-related speeches and discourses.

**Key steps:**
1. Open `data/sources/Notes.xlsx` and read all URLs and metadata
2. Use those URLs as a starting point; conduct additional web searches to find more speeches, interviews, and discourses on climate topics
3. Visit each URL using web browsing tools and extract the primary speech/article text
4. For any YouTube video links, extract the transcript
5. Save each item as a Markdown file named `YYYY-MM-DD-brief-description.md` inside `data/raw_speeches/`
6. Strip all boilerplate (navigation menus, ads, related article links) — keep only the actual discourse content
7. Maintain a running `data/raw_speeches/collection_log.md` recording source URL, date, title, and collection status for each file

**Language note:** Milei's speeches are primarily in Spanish. Save them in their original language. Do NOT translate. Add an English summary as a frontmatter comment at the top of each file if helpful.

**File naming convention:**
```
data/raw_speeches/YYYY-MM-DD-keyword-slug.md
```
Example: `2024-09-23-milei-un-general-assembly.md`

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

---

### Agent 3 — The Narrative Analyst (Phase 3) — REQUIRES PHASE 2

**Workflow file:** `workflows/3_narrative_analyst.md`

**Primary task:** Apply the coding book to each speech and synthesize findings.

**Critical input:** Read `analysis/coding_book.md` before touching any speech files. This document defines all analytical categories — both deductive (seed) and inductive (emergent).

**Key steps:**
1. For each file in `data/raw_speeches/`, perform paragraph-by-paragraph thematic coding
2. Label each relevant passage with one or more category codes from the codebook (e.g., `[EPISTEMOLOGICAL_DISCREDITING: Knowledge Problem]`)
3. Write a brief memo (2-4 sentences) explaining why a passage fits a given code
4. If a passage reveals a genuinely new pattern not covered by existing codes, add it to `analysis/coding_book.md` under the "Phase 2: Inductive" section with a name and definition
5. Save the coded version of each speech to `data/processed/coded/` using the same filename as the raw version
6. Track coding frequency in a running tally
7. Generate `analysis/results/final_analysis_report.md` — see structure below

**Final report structure:**
```markdown
# Final Analysis Report: Milei's Climate Narratives

## Executive Summary
## Corpus Overview (N speeches, date range, source types)
## Findings by Deductive Category
### Epistemological Discrediting
### Denialism
### Cultural Backlash
### Dual Policy Output Tracker
## Emergent Inductive Categories
## Rhetorical Strategy Patterns
## Key Quotes and Exemplary Passages
## Conclusions and Next Steps
```

---

## The Codebook — Summary

Full codebook: `analysis/coding_book.md`

**Deductive categories (pre-defined):**

| Pillar | Sub-codes |
|--------|-----------|
| Epistemological Discrediting | Knowledge Problem, No Market Failures, Fallacy of Authority, Government Failure |
| Denialism | Natural Cycles, Manipulated Models |
| Cultural Backlash | Woke Bundling, Neo-Marxism, Sovereignty Threat |
| Dual Policy Output (tracker) | Discursive Delegitimation, State Capability Erosion |

**Inductive categories:** Populated during Phase 3 as new patterns emerge.

---

## Key Academic Concepts (Context for Agents)

- **Abductive coding:** Neither purely top-down (deductive) nor purely bottom-up (inductive). Start with seed categories, remain open to revising or expanding them based on what the data shows.
- **Discourse analysis:** The unit of analysis is language — not just what Milei says, but *how* he says it, what rhetorical moves he makes, and what social/political effects those moves have.
- **Climate obstruction:** The focus is on how rhetoric actively undermines climate policy, not just expresses skepticism. Track both discursive moves and their links to concrete policy actions (budget cuts to CONICET, withdrawal from agreements, etc.).
- **La casta:** Milei's central political frame positioning the political establishment as an extractive class. Watch for how climate institutions get folded into this narrative.
- **Neo-Marxism framing:** In Milei's rhetoric, environmentalism is frequently coded as a disguised socialist project. Code this under Cultural Backlash > Neo-Marxism.

---

## File and Naming Conventions

- All agent-generated files go into the directories specified above — never in the project root
- Speech files: `YYYY-MM-DD-slug.md` in `data/raw_speeches/`
- Coded files: same name in `data/processed/coded/`
- All log files use the suffix `_log.md`
- Intermediate notes or drafts: prefix with `_draft_` (these can be deleted later)
- Do not rename or move files in `docs/` or `analysis/coding_book.md` without the researcher's approval

---

## Important Constraints

- **Language:** Preserve all speech content in the original Spanish. Do not translate primary sources.
- **Copyright:** Do not reproduce full copyrighted academic articles. Quote only short passages when needed for coding memos.
- **Source integrity:** Record every source URL in `collection_log.md`. If a URL is broken or inaccessible, log it with status `FAILED` and move on.
- **Codebook authority:** `analysis/coding_book.md` is the single source of truth for coding decisions. Do not invent codes without adding them to the codebook first.
- **Scope:** Focus exclusively on discourses related to climate change, environmental policy, sustainability, and the 2030 Agenda. Do not code general economic or political speeches unless they contain relevant climate-adjacent rhetoric.
