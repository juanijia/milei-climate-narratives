---
name: discourse-coder
description: >
  Applies qualitative abductive coding to political speech transcripts using the project
  codebook, producing annotated files and updating the codebook with inductive findings.
  Use this skill whenever you are: coding speech files in `data/raw_speeches/`, applying
  the Milei climate narratives analytical framework, performing paragraph-by-paragraph
  thematic analysis, labeling passages with epistemological discrediting, denialism,
  cultural backlash, or other codebook categories, building the coded corpus in
  `data/processed/coded/`, or updating the frequency tally. Also use when the user says
  things like "analyze this speech", "code this transcript", "apply the codebook", "find
  the rhetorical patterns", or "start Phase 3". This skill enforces consistent annotation
  format, inductive category protocol, and frequency tracking so the analysis remains
  reliable and comparable across the entire corpus.
---

# Discourse Coder

You are applying a qualitative abductive coding framework to political speeches, producing
annotated transcripts and a cumulative frequency tally. The goal is systematic, defensible
analysis — not superficial keyword matching.

## Before You Start

1. **Read the codebook first**: Open `analysis/coding_book.md` and read it fully. Every
   coding decision flows from the definitions there. Do not invent codes that aren't in the
   codebook; if you encounter a new pattern, follow the inductive category protocol below.

2. **Read the methodology summary**: `analysis/results/methodology_summary.md` contains
   the theoretical framing. Understanding why these categories exist helps you apply them
   more accurately.

3. **Check which files have already been coded**: Compare `data/raw_speeches/` to
   `data/processed/coded/`. Only code files that haven't been processed yet.

## The Abductive Approach

This is neither purely top-down (deductive) nor purely bottom-up (inductive). You start
with the seed categories defined in the codebook, but you remain alert to patterns in the
data that the categories don't capture. When you find such a pattern, you document it as
a candidate inductive category and evaluate whether it rises to the level of a formal code.

Think of the codebook as a good working hypothesis, not a final answer.

## Coding Format

Work paragraph by paragraph. After each paragraph that contains codeable content, add an
inline annotation immediately below it. Paragraphs with no codeable content pass through
unchanged.

```
[Original paragraph text in Spanish...]

`[CODE: Pillar > Sub-code]` — *Memo: 2–4 sentences explaining why this passage fits the
code. Note the specific rhetorical move being made, not just that the words match the
category label. What effect does this framing have? What does it do in context?*
```

If a single paragraph receives multiple codes, stack them vertically:

```
[Original paragraph text...]

`[CODE: Epistemological_Discrediting > Fallacy_of_Authority]` — *Memo: ...*

`[CODE: Cultural_Backlash > Neo-Marxism]` — *Memo: ...*
```

**Code label format:** Use the exact pillar and sub-code names from the codebook, with
underscores replacing spaces. Examples:
- `[CODE: Epistemological_Discrediting > Knowledge_Problem]`
- `[CODE: Denialism > Natural_Cycles]`
- `[CODE: Cultural_Backlash > Sovereignty_Threat]`
- `[CODE: Dual_Policy_Output > Discursive_Delegitimation]`
- `[CODE: INDUCTIVE > YourCategoryName]` (for new patterns)

## What Makes a Good Coding Memo

The memo is where the analytical work happens. A weak memo just says "this matches the
category". A strong memo explains:
- What specific rhetorical move is being made (e.g., "Milei invokes Hayek's knowledge
  problem to frame climate science as epistemically overreaching")
- Why this fits this code rather than an adjacent one
- What ideological or political work the framing performs
- Any ambiguity or tension worth flagging for the researcher

Write memos in English (the researcher reads English) even though the speech text is Spanish.

## Inductive Category Protocol

When you encounter a recurring theme not covered by the existing codebook:

1. Apply `[CODE: INDUCTIVE > TentativeName]` inline with a memo explaining what you're
   seeing.
2. Continue coding the rest of the speech; note how many times the pattern appears.
3. At the end of the speech, review all `INDUCTIVE` codes. If the pattern appeared more
   than twice, or if it seems analytically significant even if rare, it warrants formalization.
4. Add the new category to `analysis/coding_book.md` under "Phase 2: Inductive":
   - **Name**: Short, descriptive, in PascalCase
   - **Definition**: 2–3 sentences explaining what the pattern is, how to recognize it,
     and what makes it distinct from existing categories
   - **Example**: Quote the passage that led you to create the category (in Spanish)

Inductive categories are one of the most valuable outputs of this phase. Be alert and
generous — it's better to flag a tentative pattern than to miss a genuine finding.

## Frequency Tracking

After coding each speech, update `data/processed/frequency_tally.json`. This file tracks
how many times each code appears across the corpus.

If the file doesn't exist yet, create it with this structure:

```json
{
  "Epistemological_Discrediting": {
    "Knowledge_Problem": 0,
    "No_Market_Failures": 0,
    "Fallacy_of_Authority": 0,
    "Government_Failure": 0
  },
  "Denialism": {
    "Natural_Cycles": 0,
    "Manipulated_Models": 0
  },
  "Cultural_Backlash": {
    "Woke_Bundling": 0,
    "Neo-Marxism": 0,
    "Sovereignty_Threat": 0
  },
  "Dual_Policy_Output": {
    "Discursive_Delegitimation": 0,
    "State_Capability_Erosion": 0
  },
  "Inductive": {}
}
```

Increment each code count by 1 for each coded passage (not each word — one passage = one
count even if the paragraph is long). Add new inductive categories to the `"Inductive"` object
as they are created.

## Output File

Save the coded version of each speech to:
```
data/processed/coded/<same_filename_as_raw>.md
```

Do not modify the raw file in `data/raw_speeches/`. The coded file should contain the
original frontmatter plus the annotated body.

## Per-Speech Summary

At the end of each coded file, append this section:

```markdown
---

## Coding Summary

- **Dominant codes:** [list the top 2–3 codes by frequency in this speech]
- **New inductive categories added:** [list names, or "none"]
- **Notable rhetorical moves:** [1–2 observations about patterns specific to this speech
  — things that stand out beyond what the codes capture]
- **Flagged for follow-up:** [any passages where the coding decision was uncertain, or
  where the researcher should take a closer look; or "none"]
```

This summary is read by the researcher before diving into the full annotated text. Make it
substantive — it should convey the analytical gist of the speech in a few lines.

## Processing Multiple Files

When coding a batch of files:
- Process them in chronological order (oldest first) — this helps you track how rhetoric
  evolves over time
- Keep track of cross-speech patterns: when the same rhetorical move appears in multiple
  speeches, that convergence is significant and worth noting in memos
- After every 3–5 files, update the frequency tally to keep it current

## A Note on Subjectivity

Coding is an interpretive act, not a mechanical one. Two thoughtful analysts might code
the same passage differently. That's expected and OK. What matters is that your decisions
are:
- Grounded in the codebook definitions
- Explained in your memos (so the researcher can evaluate your reasoning)
- Consistent across the corpus (similar passages should receive similar codes)

When you're uncertain, err on the side of flagging the passage for review rather than
either forcing a code or skipping it. The "Flagged for follow-up" field in the summary
exists precisely for this.
