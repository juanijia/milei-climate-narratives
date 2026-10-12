---
name: discourse-coder-v4
description: >
  Applies the v4 qualitative abductive coding framework to presidential speech transcripts,
  using the v4 codebook (analysis/coding_book_v4.md) and saving outputs to
  analysis/coded_speeches/v4/. Use this skill — not discourse-coder, v2, or v3 — whenever
  you are performing the v4 coding pass: coding speech files in data/raw_speeches/,
  applying Dimension 1 (Discursive Delegitimization) exclusively to speech data,
  performing paragraph-by-paragraph thematic analysis, labeling passages with D1 codes,
  building the v4 coded corpus in analysis/coded_speeches/v4/, or updating the v4 frequency
  tally. Key v4 changes from v3: overcoding rule enforced (one primary code per passage);
  Deregulation_Benefits merged into Delegitimization_of_Regulation; Neo_Marxism renamed to
  Anti_Socialism_Anti_Collectivism; Attack_on_Universities merged with Attack_on_Public_
  Research_Institutions; Rejection_of_Expert_Mediation absorbed into Attack_on_Experts_and_
  Technocrats; Selective_Empiricism promoted to deductive D1.2 code; Temporal_Appropriation
  and Reported_Denial retired. Also use when the user says "run v4 coding", "apply the v4
  codebook", "start the fourth coding pass", or "Phase 3 v4".
---

# Discourse Coder — Version 4

You are applying the **v4 qualitative abductive coding framework** to presidential speeches,
producing annotated transcripts and a cumulative frequency tally. The v4 framework applies
**Dimension 1 (Discursive Delegitimization) exclusively to speech data**. Dimension 2 (State
Capability Erosion) is reserved for formal documentation and must not be applied to speeches.

## Before You Start

1. **Read the v4 codebook**: Open `analysis/coding_book_v4.md` and read it fully before
   touching any speech file. All coding decisions flow from the definitions there.

2. **Read the v4 methodology summary**: `analysis/methodology_summary_v4.md` documents
   the v3→v4 changes and the recoding manifest for the v3 corpus.

3. **Check which files need coding**: Compare `data/raw_speeches/` to
   `analysis/coded_speeches/v4/`. Only code files not yet present in v4.

4. **Do not modify prior version outputs**: Files in `analysis/coded_speeches/v1/`,
   `v2/`, and `v3/` must remain untouched.

---

## The Core V4 Rules

### Rule 1: D1 Only for Speeches

When Milei's speech references, justifies, or announces an institutional change, code the
passage under the appropriate D1 sub-code — not a D2 code.

**Typical mappings:**
- Speech announcing exit from the 2030 Agenda → `D1.1 > Rejection_of_Multilateral_Governance`
- Speech calling for reduction of supranational organizations → `D1.1 > Rejection_of_Multilateral_Governance`
- Speech justifying agency restructuring → `D1.1 > Anti_State_Anti_Bureaucratic`
- Speech framing regulations as harmful → `D1.1 > Delegitimization_of_Regulation`

### Rule 2: One Primary Code Per Passage (Overcoding Rule — new in v4)

Apply **one primary code per passage**. Stack a second code only if it captures a
*genuinely distinct* rhetorical move that the primary code misses.

**Test before stacking:** If the additional code were removed, would the passage still
yield the same core analytical insight? If yes → drop the additional code.

**Common overcoding patterns to avoid:**
- `Woke_Bundling` + `Anti_Socialism_Anti_Collectivism` on the same passage (pick the dominant register)
- `Delegitimization_of_Regulation` + `Market_Primacy` on the same passage (market primacy is the foundational claim; regulation critique follows from it — code the dominant move)
- `Civilizational_Defense` + any D1.1 code when the passage is primarily D1.3 in register

### Rule 2b: Scope — General Anti-State/Anti-Casta/Anti-Regulation Rhetoric Does Not Require an Explicit Climate Mention (added 2026-07-19)

The `clima` column in the master corpus database is a **speech-selection** filter (which speeches to pick next), not a **passage-level** coding filter. Once a speech is selected, do not withhold `Anti_Casta`, `Anti_State_Anti_Bureaucratic`, `Delegitimization_of_Regulation`, `Market_Primacy`, `Attack_on_Experts_and_Technocrats`, `Attack_on_Universities_and_Research_Institutions`, or `Anti_Socialism_Anti_Collectivism` from a passage just because that passage doesn't name climate, environment, or the 2030 Agenda. These codes capture the general discursive infrastructure (anti-state, anti-regulation, anti-"casta", anti-collectivist rhetoric) that later gets applied specifically to climate governance — code it wherever it appears, per `coding_book_v4.md`'s instruction 2b.

**Ask:** "does this passage delegitimize the state, bureaucracy, regulation, the political class, expertise, or collectivism as such?" — not "does this passage mention climate?" If yes to the first, code it.

**Still out of scope:** passages with no delegitimization move of any kind — purely ceremonial, biographical, or diplomatic content (condolences, historical commemoration, bilateral pleasantries). Those get zero codes because there's no rhetorical move to identify, not because they lack a climate label. This was the documented failure mode in the first full-corpus batch (2023-12-10 through 2024-01-26) — see `analysis/_draft_v4_batch2_consistency_audit.md` — where general anti-casta/anti-state content was wrongly left uncoded on the mistaken assumption that the `clima` filter applied at the passage level.

### Rule 3: Retired Categories — Do Not Apply

- **`Temporal_Appropriation`** — eliminated. Do not apply. See watchlist in coding_book_v4.md for conditions under which it could be re-raised inductively.
- **`Reported_Denial`** — retired. Code only primary Milei discourse, not opponents' paraphrases of his positions.
- **`Deregulation_Benefits`** — merged into `Delegitimization_of_Regulation`. Use the merged code for both the positive and negative face of the deregulation argument.
- **`Rejection_of_Expert_Mediation`** — absorbed into `Attack_on_Experts_and_Technocrats`.
- **`Attack_on_Universities`** and **`Attack_on_Public_Research_Institutions`** — merged into `Attack_on_Universities_and_Research_Institutions`.
- **`Neo_Marxism`** — renamed to `Anti_Socialism_Anti_Collectivism`.

---

## Coding Format

Work paragraph by paragraph. After each paragraph that contains codeable content, add an
inline annotation immediately below it. Paragraphs with no codeable content pass through
unchanged.

```
[Original paragraph text in Spanish or English...]

`[CODE: D1.1 > Rejection_of_Multilateral_Governance]` — *Memo: 2–4 sentences explaining
why this passage fits the code. Note the specific rhetorical move, what ideological work
the framing performs, and why this sub-code rather than an adjacent one.*
```

### Rule 4: Never Omit, Truncate, or Paraphrase the Source Text (added 2026-08-06)

"Paragraphs with no codeable content pass through unchanged" means what it says: every
paragraph of the raw speech — coded or not — must appear in the output **verbatim and in
full**, including passages that are near-duplicates or verbatim repeats of material coded
in an earlier speech. Do not replace an uncoded passage with an editorial summary in
brackets (e.g. `[... left uncoded: X, Y, Z ...]`), and do not truncate a paragraph
mid-sentence with `[...]` even when only part of it is directly relevant to the code
being applied.

**Why this rule exists:** a 2026-07-19 coding pass applied this shortcut on long,
repetitive speeches (the corpus's Davos/CPAC/forum circuit reuses the same set-piece
arguments across venues), reasoning that near-duplicate content didn't need to be
reproduced. This deleted up to 95% of some speeches' text from the coded output —
150 of 197 files were affected — destroying the ability to do manual qualitative review
against the coded file directly. See `analysis/_draft_v4_excerpt_omission_audit.md` for
the full incident writeup and the reconstruction that recovered it from
`data/raw_speeches/`. Duplication across speeches is a genuine analytical observation —
it belongs in the Coding Summary's "Overcoding decisions" or "Notable rhetorical moves"
field as a *note*, never as grounds to delete or shorten the passage itself.

**Also avoid:** reordering passages out of the sequence they appear in in the raw
transcript for thematic presentation (e.g. grouping non-adjacent sentences under a single
theme). If a speech is structured around a recurring device (like an enumerated list),
code each instance in the order it actually occurs — don't collate matching passages
together across the transcript.

If a single paragraph genuinely receives two codes (both conditions met — rare):

```
[Original paragraph text...]

`[CODE: D1.1 > Sustainability_as_Ideological_or_Harmful]` — *Memo: ...*

`[CODE: D1.3 > Anti_Socialism_Anti_Collectivism]` — *Memo: ...*
```

**Before stacking two codes, apply the overcoding test.**

---

## V4 Code Reference

**D1.1 — Delegitimization of State Intervention and Sustainability Governance:**
- `[CODE: D1.1 > Market_Primacy]`
- `[CODE: D1.1 > Anti_State_Anti_Bureaucratic]`
- `[CODE: D1.1 > Anti_Casta]`
- `[CODE: D1.1 > Delegitimization_of_Regulation]` *(covers both delegitimization and deregulation-benefits arguments)*
- `[CODE: D1.1 > Sustainability_as_Ideological_or_Harmful]`
- `[CODE: D1.1 > Rejection_of_Multilateral_Governance]` *(broader scope — not limited to environmental governance)*

**D1.2 — Delegitimization of Public Science and Expertise:**
- `[CODE: D1.2 > Attack_on_Universities_and_Research_Institutions]`
- `[CODE: D1.2 > Attack_on_Experts_and_Technocrats]` *(includes rejection of expert mediation in governance)*
- `[CODE: D1.2 > Climate_Skepticism_or_Dismissal]`
- `[CODE: D1.2 > Pseudo_Science_or_Ideological_Science]`
- `[CODE: D1.2 > Selective_Empiricism]` *(deductive in v4 — no INDUCTIVE prefix)*

**D1.3 — Cultural Backlash:**
- `[CODE: D1.3 > Woke_Bundling]`
- `[CODE: D1.3 > Anti_Socialism_Anti_Collectivism]` *(renamed from Neo_Marxism)*
- `[CODE: D1.3 > Civilizational_Defense]`

**Inductive (new patterns only):**
- `[CODE: INDUCTIVE > TentativeName | closest: D1.x > Sub_code]`

---

## What Makes a Good Coding Memo

A weak memo says "this matches the category." A strong memo explains:
- What specific rhetorical move is being made
- Why this sub-code rather than an adjacent one
- What ideological work the framing performs
- Any ambiguity or overcoding tension resolved

Write memos in English even when the speech is in Spanish.

---

## Inductive Category Protocol

When you encounter a recurring theme not covered by existing v4 codes:

1. Apply `[CODE: INDUCTIVE > TentativeName | closest: D1.x > Sub_code]` with a memo
   explaining the pattern and why existing codes don't cover it.
2. Continue coding; note how many times the pattern appears across the speech.
3. At the end of the speech, review all INDUCTIVE codes. If the pattern appeared more
   than twice or is analytically distinctive, formalize it.
4. Add the new category to `analysis/coding_book_v4.md` under "Phase 2: Inductive" with:
   - Name (PascalCase), definition, example, closest D1 code

**On Temporal_Appropriation specifically:** If you encounter a passage that meets *both*
conditions — (1) uses vocabulary recognizably from sustainability discourse (intergenerational
responsibility, futurity, "protecting future generations") AND (2) redirects that vocabulary
explicitly against a sustainability governance mechanism — apply it as
`[CODE: INDUCTIVE > Temporal_Appropriation | closest: D1.1 > Rejection_of_Multilateral_Governance]`
and flag for team review. Do not apply it to passages that merely mention the future or
invoke generational language without the specific vocabulary co-optation.

---

## Frequency Tracking

`analysis/coded_speeches/v4/frequency_tally_v4.json` is no longer hand-edited. After
coding each speech (or each batch), regenerate it from the coded `.md` files by running:

```bash
cd <project_root>
python skills/qda-outputs/scripts/update_frequency_tally.py
```

This recomputes every dimension/sub-code count and `files_coded` list directly from
whatever `[CODE: ...]` annotations are actually present in `analysis/coded_speeches/v4/`
— via the same canonical parser (`corpus_data.py`) the Excel and HTML outputs use — so
the tally can never silently drift out of sync with the coded files the way a
hand-maintained count could (this happened once already: a manually-set count for
`Anti_Casta` and `Anti_Socialism_Anti_Collectivism` was each off by 1 relative to the
actual corpus, caught only when this script was introduced). The script prints a diff
against the previously saved counts — a nonzero diff after a coding batch is expected;
a nonzero diff when you didn't expect any coding changes means something is wrong and
is worth investigating before moving on.

The only two fields that survive across a regeneration are `_metadata.coding_date` and
`_metadata.note` (the hand-authored narrative history of the corpus — batch rationale,
recoding decisions, methodology changes). Update those deliberately with `--set-date`
and `--set-note` when you have something new to record; do not edit the JSON directly.

---

## Output Files

Save coded outputs to:
```
analysis/coded_speeches/v4/<same_filename_as_raw>.md
```

The coded file must contain the original frontmatter (with `coded_version: v4` added) plus
the annotated body.

---

## Per-Speech Summary

At the end of each coded file, append:

```markdown
---

## Coding Summary (v4)

- **Dominant codes:** [top 2–3 codes by frequency in this speech]
- **Sub-dimension balance:** [rough split across D1.1 / D1.2 / D1.3]
- **New inductive categories added:** [list names, or "none"]
- **Notable rhetorical moves:** [1–2 observations beyond what the codes capture]
- **Overcoding decisions:** [any passages where a second code was considered and rejected, and why]
- **V3 recoding notes:** [if this file was updated from v3, list the changes applied from the recoding manifest; otherwise "N/A — first-pass coding"]
- **Flagged for follow-up:** [uncertain coding decisions; or "none"]
```

---

## Processing Multiple Files

- Process in chronological order (oldest first) to track rhetorical evolution
- Apply the recoding manifest (documented in `analysis/methodology_summary_v4.md`) when
  converting v3 files to v4 — do not recode from scratch; copy and apply changes
- Run `update_frequency_tally.py` (see Frequency Tracking above) after every 3–5 files

---

## Key Analytical Questions for V4

1. **Does D1.1 dominance hold after overcoding correction?** The v3 corpus had 58% D1.1.
   With overcoded passages removed, does this ratio shift?

2. **Does `Sustainability_as_Ideological_or_Harmful` cluster by venue?** Now restored in v4,
   does it appear more in Apertura speeches or international forums?

3. **`Selective_Empiricism` as deductive:** With the formal deductive status, does frequency
   change in new coding passes? Is it bridging D1.1 and D1.2 as expected?

4. **Rhetoric evolution 2023–2026:** Does the trajectory from cultural-war framing (D1.3)
   toward economic-foundational arguments (D1.1) hold after the v4 corpus clean-up?

---

## After Coding: Generate Outputs

Once the full corpus is coded and `frequency_tally_v4.json` is up to date, use the
**qda-outputs** skill to generate the Excel workbook, HTML explorer, and final report.
The skill runs `skills/qda-outputs/scripts/generate_xlsx.py` and
`skills/qda-outputs/scripts/generate_html.py` against the v4 corpus, then writes the
final analysis report.

## Definition updates (2026-10-11)

Full definitions are in `analysis/coding_book_v4.md`. `Anti_Socialism_Anti_Collectivism` and `Civilizational_Defense` no longer require a climate or environmental reference in the passage (Option A scope). `Pseudo_Science_or_Ideological_Science` covers claims that any body of knowledge, or the institutions producing it (including economics, think tanks, the Club of Rome), is ideologically captured or epistemically unsound; it targets knowledge production, not a specific finding and not people as a class. `Attack_on_Experts_and_Technocrats` targets people or professional authority as a class (credentials, competence, honesty, motives, track record). A purely economic disagreement or a taunt aimed at an argument is not an expert attack and should not be coded as one.
