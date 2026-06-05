---
name: discourse-coder-v2
description: >
  Applies the v2 qualitative abductive coding framework to political speech transcripts,
  using the v2 codebook (analysis/coding_book_v2.md) and saving outputs to data/processed/v2/.
  Use this skill — not discourse-coder — whenever you are performing the second coding pass
  of the corpus: coding speech files in `data/raw_speeches/`, applying the two-dimensional
  v2 framework (discursive delegitimization + state capability erosion), performing
  paragraph-by-paragraph thematic analysis, labeling passages with v2 codes, building the
  v2 coded corpus in `data/processed/v2/coded/`, or updating the v2 frequency tally.
  Also use when the user says things like "run v2 coding", "apply the new codebook",
  "start the second coding pass", or "Phase 3 v2". This skill enforces consistent v2
  annotation format, inductive category protocol, and frequency tracking so the v2 analysis
  remains reliable and comparable across the corpus.
---

# Discourse Coder — Version 2

You are applying the **v2 qualitative abductive coding framework** to political speeches,
producing annotated transcripts and a cumulative frequency tally. The v2 framework has two
theoretical dimensions: (1) discursive delegitimization of sustainability governance and
public expertise, and (2) erosion of state capabilities for sustainability governance.

## Before You Start

1. **Read the v2 codebook**: Open `analysis/coding_book_v2.md` and read it fully. Every
   coding decision flows from the definitions there. Do not use v1 codes; map all passages
   to v2 categories.

2. **Read the v2 methodology summary**: `analysis/results/v2/methodology_summary_v2.md`
   provides the updated theoretical framing for why these dimensions and categories exist.

3. **Check which files have already been coded**: Compare `data/raw_speeches/` to
   `data/processed/v2/coded/`. Only code files that haven't been processed yet.

4. **Do not touch v1 outputs**: v1 coded files in `data/processed/coded/` and
   `data/processed/frequency_tally.json` must remain untouched.

## The Abductive Approach

Start with the seed categories defined in `coding_book_v2.md`. Remain alert to patterns
the categories don't capture. When you find such a pattern, document it as a candidate
inductive category.

Three inductive categories are carried forward from v1 (Selective_Empiricism,
Temporal_Appropriation, Reported_Denial). When these patterns appear, note both the
INDUCTIVE label and the closest v2 Dimension/sub-code. See the codebook for guidance.

## Coding Format

Work paragraph by paragraph. After each paragraph that contains codeable content, add an
inline annotation immediately below it. Paragraphs with no codeable content pass through
unchanged.

```
[Original paragraph text in Spanish...]

`[CODE: Dimension > Sub-code]` — *Memo: 2–4 sentences explaining why this passage fits the
code. Note the specific rhetorical move being made, what ideological work the framing does,
and why this code rather than an adjacent one.*
```

If a single paragraph receives multiple codes, stack them vertically:

```
[Original paragraph text...]

`[CODE: D1.1 > Market_Primacy]` — *Memo: ...*

`[CODE: D1.3 > Neo_Marxism]` — *Memo: ...*
```

**Code label format:** Use the dimension prefix and exact sub-code names from the codebook,
with underscores replacing spaces. Examples:

- `[CODE: D1.1 > Market_Primacy]`
- `[CODE: D1.1 > Rejection_of_Multilateral_Governance]`
- `[CODE: D1.2 > Attack_on_Public_Research_Institutions]`
- `[CODE: D1.2 > Climate_Skepticism_or_Dismissal]`
- `[CODE: D1.3 > Neo_Marxism]`
- `[CODE: D1.3 > Civilizational_Defense]`
- `[CODE: D2.1 > Budget_Cuts_Science]`
- `[CODE: D2.2 > Ministry_Reorganization]`
- `[CODE: D2.3 > Withdrawal_from_International_Initiatives]`
- `[CODE: INDUCTIVE > YourCategoryName]` (for new patterns)

For carried-forward inductive categories from v1:
- `[CODE: INDUCTIVE > Selective_Empiricism | closest: D1.2 > Pseudo_Science_or_Ideological_Science]`
- `[CODE: INDUCTIVE > Temporal_Appropriation | closest: D1.1 > Rejection_of_Multilateral_Governance]`
- `[CODE: INDUCTIVE > Reported_Denial]`

## What Makes a Good Coding Memo

A weak memo just says "this matches the category." A strong memo explains:
- What specific rhetorical move is being made
- Why this fits this sub-code rather than an adjacent one
- What ideological or political work the framing performs
- Any ambiguity or tension worth flagging

Write memos in English even though speech texts are in Spanish.

## Inductive Category Protocol

When you encounter a recurring theme not covered by existing v2 codes:

1. Apply `[CODE: INDUCTIVE > TentativeName]` inline with a memo explaining what you're
   seeing and why existing codes don't cover it.
2. Continue coding the rest of the speech; note how many times the pattern appears.
3. At the end of the speech, review all INDUCTIVE codes. Formalize if the pattern appeared
   more than twice, or if it is analytically significant.
4. Add the new category to `analysis/coding_book_v2.md` under "Phase 2: Inductive":
   - **Name**: Short, descriptive, PascalCase
   - **Definition**: 2–3 sentences: what the pattern is, how to recognize it, what makes
     it distinct from existing v2 codes
   - **Example**: The passage that led you to create it (in Spanish)
   - **Closest v2 code**: The most adjacent v2 sub-code, and why it's still distinct

## Frequency Tracking

After coding each speech, update `data/processed/v2/frequency_tally_v2.json`.

If the file doesn't exist, create it:

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
  "D2_State_Capability_Erosion": {
    "D2.1_Budgetary_Retrenchment": {
      "Budget_Cuts_Science": 0,
      "Budget_Cuts_Environment": 0,
      "Budget_Cuts_Sustainability_Programs": 0,
      "Budget_Cuts_Universities": 0
    },
    "D2.2_Institutional_Downgrading": {
      "Ministry_Reorganization": 0,
      "Agency_Elimination_or_Merger": 0,
      "Regulatory_Institution_Changes": 0,
      "Administrative_Hollowing_Out": 0
    },
    "D2.3_Policy_Dismantling": {
      "Changes_in_Climate_Commitments": 0,
      "Withdrawal_from_International_Initiatives": 0,
      "Policy_Instrument_Changes": 0,
      "Deregulation_Environmental_Protection": 0,
      "Reduced_Implementation_or_Enforcement": 0
    }
  },
  "Inductive": {
    "Selective_Empiricism": 0,
    "Temporal_Appropriation": 0,
    "Reported_Denial": 0
  }
}
```

## Output File

Save coded outputs to:
```
data/processed/v2/coded/<same_filename_as_raw>.md
```

Do not modify raw files in `data/raw_speeches/` or any file in `data/processed/coded/`
(the v1 outputs).

The coded file should contain the original frontmatter plus the annotated body.

## Per-Speech Summary

At the end of each coded file, append:

```markdown
---

## Coding Summary (v2)

- **Dominant codes:** [top 2–3 codes by frequency in this speech, using v2 labels]
- **Dimension balance:** [rough split between D1 and D2 codes — e.g., "predominantly D1.1
  and D1.2, no D2 codes found"]
- **New inductive categories added:** [list names, or "none"]
- **Notable rhetorical moves:** [1–2 observations beyond what the codes capture —
  patterns specific to this speech]
- **Comparison to v1 coding:** [brief note on how the v2 coding illuminates something the
  v1 pass missed, or confirms/complicates a v1 finding; "N/A" if v1 coded file unavailable]
- **Flagged for follow-up:** [uncertain coding decisions or passages the researcher should
  review; or "none"]
```

The "Comparison to v1 coding" field is specifically useful for building the iterative
argument about what the new framework adds analytically.

## Processing Multiple Files

- Process in chronological order (oldest first) to track rhetorical evolution
- Note cross-speech patterns: convergences across speeches are significant findings
- Update the frequency tally after every 3–5 files
- For speeches that were already coded in v1, you may optionally read the v1 coded version
  from `data/processed/coded/` to compare — but base your v2 annotations on the raw text,
  not on v1 decisions

## A Note on Dimensionality

The key analytical move in v2 is the **distinction between D1 and D2**. D1 captures what
Milei says to delegitimize sustainability governance; D2 captures what he says about
dismantling the institutional capacity to govern it. Many speeches will be predominantly
D1 (rhetoric). D2 codes are more likely to appear in speeches where Milei justifies specific
budget decisions, announces restructurings, or references policy changes. Pay attention to
this distribution across the corpus — it is analytically central to the argument about the
dual mechanism of obstruction.
