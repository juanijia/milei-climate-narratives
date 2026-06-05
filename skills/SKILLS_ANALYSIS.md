# Skills Analysis for Agent Workflows

This document identifies the skills that would meaningfully improve each agent's work, distinguishing between skills that already exist and those that should be built.

---

## Phase 1 — Methodologist Agent

**Status: Complete.** No new skills strictly needed. However, for future reruns or updates:

### ✅ Use existing: `pdf`
The Methodologist reads multiple PDFs from `docs/methodology/` and `docs/references/`. The `pdf` skill provides structured PDF text extraction and is directly applicable. The Methodologist should invoke it when opening any `.pdf` file.

### ✅ Use existing: `docx`
The abstract is stored as `docs/abstract/Abstract.docx`. The `docx` skill handles Word document reading and should be used to extract the abstract text cleanly.

---

## Phase 2 — Data Collector Agent

This is the most tool-intensive phase. Three skills are critical.

### ✅ Use existing: `xlsx`
The primary source list lives in `data/sources/Notes.xlsx`. The agent must open this file, read the URLs and metadata, and use that list as the starting point for collection. The `xlsx` skill handles reading Excel files correctly.

**When to invoke:** At step 1, before any web browsing begins.

---

### 🔨 Build new: `speech-collector`

**Why it's needed:**
The Data Collector's most complex task is visiting many URLs, extracting clean speech text (stripping boilerplate HTML), and saving consistently formatted Markdown files. Without a skill, the agent will reinvent this process for every run and produce inconsistent output formats. A dedicated skill ensures:
- Consistent frontmatter structure in every saved `.md` file
- Reliable boilerplate-stripping logic
- Correct file naming convention (`YYYY-MM-DD-slug.md`)
- Automatic logging to `collection_log.md`

**Proposed SKILL.md outline:**

```markdown
---
name: speech-collector
description: >
  Scrapes political speeches, interviews, and news articles from URLs and saves
  them as structured Markdown files ready for qualitative coding. Use for any
  task involving: collecting speech texts, scraping article content, building a
  corpus of political discourse, extracting text from news sites for research.
---

# Speech Collector

Systematically visits URLs, extracts the primary discourse content, and saves
clean Markdown files with structured frontmatter.

## Output format
Each file saved to `data/raw_speeches/YYYY-MM-DD-slug.md` with this frontmatter:
[see CLAUDE.md for template]

## Boilerplate removal rules
Strip: navigation menus, related articles, social share buttons, cookie banners,
author bios unrelated to the speech, timestamps/bylines (move to frontmatter).
Keep: all spoken/written content attributed to Milei, interviewer questions if
it's a Q&A format (label as [INTERVIEWER:]), contextual journalist descriptions
of delivery or setting.

## Logging
After each URL, append one row to collection_log.md:
| Date | Title | URL | Status | Filename |

## Failure handling
If a URL returns 404 or is paywalled: log status as FAILED/PAYWALLED and move on.
Do not retry more than once.
```

**Effort to build:** Low-medium. Mostly prompt engineering; can reuse the web browsing tools already available.

---

### 🔨 Build new: `youtube-transcript`

**Why it's needed:**
The source list includes YouTube video links, and the Data Collector workflow explicitly requires transcript extraction. YouTube transcripts have a specific extraction method (either via YouTube's own CC system or third-party tools) that differs entirely from HTML scraping. A dedicated skill prevents the agent from wasting time on incorrect approaches.

**Proposed SKILL.md outline:**

```markdown
---
name: youtube-transcript
description: >
  Extracts transcripts from YouTube video URLs for use in qualitative research.
  Use whenever a YouTube link needs to be converted to readable text for coding
  or analysis. Handles both auto-generated and manual captions.
---

# YouTube Transcript Extractor

## Approach (in order of preference)
1. Use `yt-dlp --write-auto-subs --sub-lang es --skip-download <url>` to download
   subtitle file, then parse the .vtt or .srt output into clean text
2. If yt-dlp unavailable: navigate to the video URL with browser tools, activate
   captions, and extract text from the caption overlay
3. If no captions available: note in frontmatter as `youtube_transcript: false`
   and describe the video content from the title/description only

## Output
Clean running text (no timestamps), saved as part of the standard speech .md file.
Prepend: `[SOURCE: YouTube transcript — auto-generated captions]` if captions were
auto-generated, `[SOURCE: YouTube transcript — manual captions]` if manual.

## Installation check
Run `yt-dlp --version` first. If not installed: `pip install yt-dlp --break-system-packages`
```

**Effort to build:** Low. yt-dlp is a well-documented CLI tool; the skill mostly needs to standardize how the agent calls it and formats the output.

---

## Phase 3 — Narrative Analyst Agent

This phase requires deep analytical consistency across many documents. One high-value skill.

### 🔨 Build new: `discourse-coder`

**Why it's needed:**
The Narrative Analyst applies a complex, multi-level coding scheme to dozens of speeches. Without a skill, the agent will:
- Produce inconsistent code label formats across files
- Forget to update the codebook when new inductive categories emerge
- Generate memos of uneven depth
- Lose track of frequency counts

A `discourse-coder` skill enforces the analytical workflow and output format, making the results more reliable and comparable across the corpus.

**Proposed SKILL.md outline:**

```markdown
---
name: discourse-coder
description: >
  Applies qualitative coding to political speech transcripts using an abductive
  codebook (deductive seed categories + inductive emergence). Use for any task
  involving: discourse analysis, thematic coding, narrative analysis, qualitative
  content analysis of speeches or interviews.
---

# Discourse Coder

Reads the `analysis/coding_book.md` and applies it paragraph-by-paragraph to
speech files, producing annotated versions and updating the codebook with
inductive findings.

## Coding format
Inline annotation at end of each coded paragraph:

> [Paragraph text...]
> `[CODE: Pillar > Sub-code]` — *Memo: Brief justification (2-4 sentences).*

Multiple codes on the same paragraph are stacked vertically.

## Inductive category protocol
If a passage contains a recurring theme not in the codebook:
1. Note it with `[CODE: INDUCTIVE > TentativeName]`
2. After finishing the speech, decide if the pattern is strong enough to add
3. If yes, write a formal definition and add it to `analysis/coding_book.md`
   under "Phase 2: Inductive"

## Frequency tracker
Maintain a running JSON file at `data/processed/frequency_tally.json`:
{
  "Epistemological_Discrediting": {"Knowledge_Problem": 0, ...},
  "Denialism": {...},
  ...
  "Inductive": {}
}
Increment counts after each coded speech.

## Output file
Save to `data/processed/coded/<same_filename_as_raw>.md`

## Per-speech summary
Append a short analytical memo at the end of each coded file:
## Coding Summary
- **Dominant codes:** [list top 3]
- **New inductive categories added:** [list or "none"]
- **Notable rhetorical moves:** [1-2 observations]
- **Flagged for follow-up:** [any passages needing researcher review]
```

**Effort to build:** Medium. Requires careful prompt engineering to enforce consistency, but no external tools beyond file read/write.

---

## Skills Priority Matrix

| Skill | Phase | Type | Priority | Effort |
|-------|-------|------|----------|--------|
| `pdf` (existing) | 1 | Existing | High | None |
| `docx` (existing) | 1 | Existing | Medium | None |
| `xlsx` (existing) | 2 | Existing | High | None |
| `speech-collector` | 2 | Build | **Critical** | Low-Medium |
| `youtube-transcript` | 2 | Build | High | Low |
| `discourse-coder` | 3 | Build | **Critical** | Medium |

---

## Recommended Build Order

1. **`speech-collector`** — Build this before starting Phase 2. It is the core tool the Data Collector agent will use on every URL.
2. **`youtube-transcript`** — Build alongside or immediately after `speech-collector`. Many sources will be YouTube videos.
3. **`discourse-coder`** — Build this before starting Phase 3. The quality of the final analysis depends heavily on consistent coding.

To build any of these skills, use the `skill-creator` skill available in `agent/skills/skill-creator/`.
