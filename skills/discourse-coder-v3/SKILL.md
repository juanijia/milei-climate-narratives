---
name: discourse-coder-v3
description: >
  Applies the v3 qualitative abductive coding framework to presidential speech transcripts,
  using the v3 codebook (analysis/coding_book_v3.md) and saving outputs to
  analysis/coded_speeches/v3/. Use this skill — not discourse-coder or discourse-coder-v2 —
  whenever you are performing the v3 coding pass: coding speech files in data/raw_speeches/,
  applying Dimension 1 (Discursive Delegitimization) exclusively to speech data,
  performing paragraph-by-paragraph thematic analysis, labeling passages with D1 codes,
  building the v3 coded corpus in analysis/coded_speeches/v3/, or updating the v3 frequency
  tally. The core v3 change: D2 (State Capability Erosion) codes are NOT applied to speeches
  under any circumstances — even when a speech announces or justifies an institutional change.
  Also use when the user says "run v3 coding", "apply the v3 codebook", "start the third
  coding pass", or "Phase 3 v3". This skill enforces the D1-only constraint on speech data,
  consistent v3 annotation format, inductive category protocol, and frequency tracking so the
  v3 analysis remains methodologically sound and comparable across the corpus.
---

# Discourse Coder — Version 3

You are applying the **v3 qualitative abductive coding framework** to presidential speeches,
producing annotated transcripts and a cumulative frequency tally. The v3 framework applies
**Dimension 1 (Discursive Delegitimization) exclusively to speech data**. Dimension 2 (State
Capability Erosion) is reserved for formal documentation (decrees, budget records,
reorganization documents) and must not be applied to speeches under any circumstances.

## Before You Start

1. **Read the v3 codebook**: Open `analysis/coding_book_v3.md` and read it fully. Every
   coding decision flows from the definitions there. Do not use v1 or v2 codes; map all
   passages to v3 D1 categories.

2. **Read the v3 methodology summary**: `analysis/methodology_summary_v3.md` explains the
   key methodological clarification that distinguishes v3 from v2: the strict data-source
   separation between the two analytical dimensions.

3. **Check which files have already been coded**: Compare `data/raw_speeches/` to
   `analysis/coded_speeches/v3/`. Only code files not yet processed.

4. **Do not touch v1 or v2 outputs**: Files in `analysis/coded_speeches/v1/` and
   `analysis/coded_speeches/v2/` must remain untouched.

## The Core V3 Rule: D1 Only for Speeches

In v2, some speech passages were incorrectly coded under D2 (State Capability Erosion) when
Milei referenced or announced institutional changes — for example, announcing withdrawal from
the 2030 Agenda or calling for the reduction of supranational organizations. In v3 this is
corrected:

**When Milei's speech references, justifies, or announces an institutional change, code the
passage under the appropriate D1 sub-code — not a D2 code.**

The passage is a *rhetorical act* (delegitimizing multilateral governance, framing an exit as
principled, etc.). The institutional act itself belongs to Corpus B (formal documentation)
and is coded separately with D2. Conflating the two would blur the article's dual-mechanism
argument.

**Typical re-mappings from v2 D2 → v3 D1:**
- A speech announcing exit from the 2030 Agenda → `D1.1 > Rejection_of_Multilateral_Governance`
- A speech calling for reduction of supranational organizations → `D1.1 > Rejection_of_Multilateral_Governance` or `D1.1 > Sustainability_as_Ideological_or_Harmful`
- A speech justifying agency restructuring → `D1.1 > Anti_State_Anti_Bureaucratic` or `D1.1 > Delegitimization_of_Regulation`

## The Abductive Approach

Start with the seed categories defined in `coding_book_v3.md`. Remain alert to patterns the
categories don't capture. Three inductive categories from v1/v2 are carried forward:
`Selective_Empiricism`, `Temporal_Appropriation`, and `Reported_Denial`. When new patterns
appear, follow the inductive protocol below.

## Coding Format

Work paragraph by paragraph. After each paragraph that contains codeable content, add an
inline annotation immediately below it. Paragraphs with no codeable content pass through
unchanged.

```
[Original paragraph text in Spanish...]

`[CODE: D1.1 > Rejection_of_Multilateral_Governance]` — *Memo: 2–4 sentences explaining why
this passage fits the code. Note the specific rhetorical move, what ideological work the
framing performs, and why this sub-code rather than an adjacent one.*
```

If a single paragraph receives multiple codes, stack them vertically:

```
[Original paragraph text...]

`[CODE: D1.1 > Sustainability_as_Ideological_or_Harmful]` — *Memo: ...*

`[CODE: D1.3 > Neo_Marxism]` — *Memo: ...*
```

**Code label format:** Use the exact sub-code names from the v3 codebook, with underscores
replacing spaces. Examples:

**D1.1 — Delegitimization of State Intervention and Sustainability Governance:**
- `[CODE: D1.1 > Market_Primacy]`
- `[CODE: D1.1 > Anti_State_Anti_Bureaucratic]`
- `[CODE: D1.1 > Anti_Casta]`
- `[CODE: D1.1 > Delegitimization_of_Regulation]`
- `[CODE: D1.1 > Deregulation_Benefits]`
- `[CODE: D1.1 > Sustainability_as_Ideological_or_Harmful]`
- `[CODE: D1.1 > Rejection_of_Multilateral_Governance]`

**D1.2 — Delegitimization of Public Science and Expertise:**
- `[CODE: D1.2 > Attack_on_Public_Research_Institutions]`
- `[CODE: D1.2 > Attack_on_Universities]`
- `[CODE: D1.2 > Attack_on_Experts_and_Technocrats]`
- `[CODE: D1.2 > Climate_Skepticism_or_Dismissal]`
- `[CODE: D1.2 > Pseudo_Science_or_Ideological_Science]`
- `[CODE: D1.2 > Rejection_of_Expert_Mediation]`

**D1.3 — Woke / Cultural Backlash:**
- `[CODE: D1.3 > Woke_Bundling]`
- `[CODE: D1.3 > Neo_Marxism]`
- `[CODE: D1.3 > Civilizational_Defense]`

**Inductive categories (carried forward from v1/v2):**
- `[CODE: INDUCTIVE > Selective_Empiricism | closest: D1.2 > Pseudo_Science_or_Ideological_Science]`
- `[CODE: INDUCTIVE > Temporal_Appropriation | closest: D1.1 > Rejection_of_Multilateral_Governance]`
- `[CODE: INDUCTIVE > Reported_Denial | closest: D1.3 > Neo_Marxism]`
- `[CODE: INDUCTIVE > TentativeName | closest: D1.x > Sub_code]` (for new patterns)

## What Makes a Good Coding Memo

A weak memo says "this matches the category." A strong memo explains:
- What specific rhetorical move is being made
- Why this fits this sub-code rather than an adjacent one
- What ideological or political work the framing performs
- Any ambiguity or tension worth flagging
- For passages that were coded D2 in v2: note the re-mapping and why it is a D1 act

Write memos in English even though speech texts are in Spanish.

## Inductive Category Protocol

When you encounter a recurring theme not covered by existing codes:

1. Apply `[CODE: INDUCTIVE > TentativeName]` inline with a memo explaining the pattern and
   why existing D1 codes don't cover it.
2. Continue coding the rest of the speech; note how many times the pattern appears.
3. At the end of the speech, review all INDUCTIVE codes. Formalize if the pattern appeared
   more than twice or is analytically significant.
4. Add the new category to `analysis/coding_book_v3.md` under "Phase 2: Inductive":
   - **Name**: Short, descriptive, PascalCase
   - **Definition**: 2–3 sentences: what the pattern is, how to recognize it, what makes
     it distinct from existing v3 D1 codes
   - **Example**: The passage that led you to create it (in Spanish)
   - **Closest D1 code**: The most adjacent D1 sub-code, and why the new category is distinct

## Frequency Tracking

After coding each speech, update `analysis/coded_speeches/v3/frequency_tally_v3.json`.

If the file doesn't exist, create it with this structure:

```json
{
  "D1_Discursive_Delegitimization": {
    "D1.1_State_Intervention_Governance": {
      "Market_Primacy": 0,
      "Anti_State_Anti_Bureaucratic": 0,
      "Anti_Casta": 0,
      "Delegitimization_of_Regulation": 0,
      "Deregulation_Benefits": 0,
      "Sustainability_as_Ideological_or_Harmful": 0,
      "Rejection_of_Multilateral_Governance": 0
    },
    "D1.2_Public_Science_Expertise": {
      "Attack_on_Public_Research_Institutions": 0,
      "Attack_on_Universities": 0,
      "Attack_on_Experts_and_Technocrats": 0,
      "Climate_Skepticism_or_Dismissal": 0,
      "Pseudo_Science_or_Ideological_Science": 0,
      "Rejection_of_Expert_Mediation": 0
    },
    "D1.3_Cultural_Backlash": {
      "Woke_Bundling": 0,
      "Neo_Marxism": 0,
      "Civilizational_Defense": 0
    }
  },
  "Inductive": {
    "Selective_Empiricism": 0,
    "Temporal_Appropriation": 0,
    "Reported_Denial": 0
  }
}
```

## Output Files

Save coded outputs to:
```
analysis/coded_speeches/v3/<same_filename_as_raw>.md
```

Do not modify raw files in `data/raw_speeches/` or any file in `analysis/coded_speeches/v1/`
or `analysis/coded_speeches/v2/`.

The coded file must contain the original frontmatter plus the annotated body.

## Per-Speech Summary

At the end of each coded file, append:

```markdown
---

## Coding Summary (v3)

- **Dominant codes:** [top 2–3 codes by frequency in this speech, using v3 D1 labels]
- **Sub-dimension balance:** [rough split across D1.1 / D1.2 / D1.3 — e.g., "predominantly
  D1.1 and D1.3, limited D1.2"]
- **New inductive categories added:** [list names, or "none"]
- **Notable rhetorical moves:** [1–2 observations beyond what the codes capture —
  patterns specific to this speech]
- **V2 re-mappings:** [list any passages previously coded D2 in v2 that are now re-coded
  as D1 in v3, with the new code — or "none / not previously coded"]
- **Comparison to v2 coding:** [brief note on what the v3 D1-only constraint reveals that
  v2 missed or obscured; "N/A" if v2 coded file unavailable]
- **Flagged for follow-up:** [uncertain coding decisions or passages the researcher should
  review; or "none"]
```

The "V2 re-mappings" and "Comparison to v2 coding" fields are central to the iterative
argument — they document the methodological correction and show what analytical gain the
D1-only constraint produces.

## Processing Multiple Files

- Process in chronological order (oldest first) to track rhetorical evolution across the
  corpus (2023–2026)
- Note cross-speech patterns: recurring codes across speeches are significant findings
- Update the frequency tally after every 3–5 files
- For speeches coded in v2, read `analysis/coded_speeches/v2/<filename>.md` to identify
  any D2 codes that require re-mapping — but base your v3 annotations on the raw text

## A Note on the Key Analytical Questions for V3

As you code, attend to these research questions from the v3 methodology:

1. **Sub-dimension distribution:** How does rhetoric distribute across D1.1 / D1.2 / D1.3?
   Is the primary mechanism epistemic (attacking knowledge) or political (attacking actors)?

2. **Rhetorical evolution:** Does the D1.1/D1.2/D1.3 balance shift from 2023 to 2026? Is
   there a move from D1.3 culture-war framing toward more developed D1.1 economic-foundational
   arguments as Milei moves from candidate to governing president?

3. **Institutional announcements as D1:** Passages where Milei announces exits from
   multilateral frameworks (2030 Agenda, etc.) are now coded as D1.1 > Rejection_of_
   Multilateral_Governance. Do these cluster in particular speeches or periods?

4. **Inductive category robustness:** Do Selective_Empiricism and Temporal_Appropriation
   recur consistently enough to warrant promotion to permanent deductive codes?

Note patterns relevant to these questions in your per-speech memos and the coding summary.
They feed directly into `analysis/results/v3/final_analysis_report_v3.md`.

## After Coding: Generate Outputs

Once the full corpus is coded (all files in `analysis/coded_speeches/v3/` are complete
and `frequency_tally_v3.json` is up to date), hand off to the **qda-outputs** skill:

```
Use the qda-outputs skill to generate the Excel workbook, HTML explorer, and
final analysis report.
```

The qda-outputs skill runs two scripts (`generate_xlsx.py` and `generate_html.py`)
and then writes the final report with analytical insights from the corpus findings.
Do not generate those deliverables here.
