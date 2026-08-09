# Coding Book v4 — Proposed Changes
**Version:** 4.0 (draft proposal)  
**Date:** July 2026  
**Based on:** Peer review feedback from Germán and Juani on v3 coded corpus (`qda_v3_coded_corpus_v3_feedback.xlsx`)  
**Previous version:** `analysis/coding_book_v3.md`

---

## How to read this document

This is a **change proposal**, not the final codebook. Each section explains what changes relative to v3, what stays the same, and why — grounded in the reviewer comments. A clean v4 codebook (`coding_book_v4.md`) should be produced once the team approves these changes.

The feedback came in two forms:
- **Passage-level** (columns L/N in Coded Passages sheet): Germán and Juani reviewed 97 annotations and flagged specific coding decisions
- **Category-level** (Analysis of Categories sheet): Both reviewers proposed structural changes to the sub-code schema

---

## Cross-cutting finding: overcoding

Before getting to dimension-specific changes, the most consistent signal across both reviewers is **overcoding** — too many codes per passage. Examples:

- IDs #14+15: Market_Primacy + Delegitimization_of_Regulation on the same passage → Germán: *"podría unificarse"*
- IDs #22+23: Two Delegitimization_of_Regulation codes on adjacent sentences → Germán: *"podría unificarse"*
- IDs #42+43: Woke_Bundling + Neo_Marxism on the same passage → Juani: *"no, overcoding"*
- IDs #48+49: Woke_Bundling + Neo_Marxism → Juani: *"not sure, overcoding"*
- ID #27: Civilizational_Defense on a passage already coded as D1.1 → Juani: *"atención al overcoding"*

**Proposed v4 rule (add to analyst instructions):**

> **One primary code per passage.** Stack a second code only if it captures a *genuinely distinct* rhetorical move that the primary code misses — not merely because the passage touches a related theme. Test: if removing the additional code, does the passage still yield the same core analytical insight? If yes, drop the second code.

This rule will reduce annotation count in v4 relative to v3 — that is expected and analytically defensible.

---

## D1.1 — Delegitimization of State Intervention and Sustainability Governance

### What stays the same
`Market_Primacy`, `Anti_State_Anti_Bureaucratic`, and `Anti_Casta` are validated by both reviewers across all instances. No changes to these codes.

---

### Change 1: Merge `Delegitimization_of_Regulation` + `Deregulation_Benefits`

**Proposed new name:** `Delegitimization_of_Regulation` (absorbing the positive framing)

**Reason:** Both reviewers converge on this independently.
- Juani (ID #13): *"'Benefits of deregulation' is practically the same as 'delegitimization of regulation', maybe we can combine the two"*
- Juani (ID #17): *"also 'Delegitimization of regulation', we should merge both sub-dimensions"*
- Analysis of Categories sheet: *"to bundle benefits of deregulation with delegitimization of regulation"*

**Why it makes analytical sense:** Both sub-codes are two faces of the same rhetorical move — the negative case (regulation is illegitimate) and the positive case (deregulation is good) are structurally inseparable in Milei's discourse. He almost never makes one argument without implying the other. Keeping them separate created artificial frequency splits (IDs #74+75: German suggests merging both under Market_Primacy anyway).

**Updated definition:** Passages arguing that environmental or sustainability regulation is illegitimate interference in private activity or market dynamics, *or* that removing such regulation produces positive economic and social outcomes. The two faces of a single delegitimization move.

---

### Change 2: Remove `Sustainability_as_Ideological_or_Harmful`

**Proposed action:** Retire this sub-code. Recode affected passages to whichever of the following better fits:
- `Rejection_of_Multilateral_Governance` — if the passage targets the 2030 Agenda, WEF, or international climate bodies
- `Delegitimization_of_Regulation` — if the passage frames specific policies as harmful or misguided
- `Neo_Marxism` / `Woke_Bundling` — if the passage frames the sustainability agenda as ideologically motivated

**Reason:** `Sustainability_as_Ideological_or_Harmful` is the code with the most interpretive ambiguity in the corpus. The Analysis of Categories sheet removes it entirely from the "New" column without explanation — which signals both reviewers see it as redundant. In practice, every instance coded SaIH can be more precisely captured by one of the three codes above. The code does not add analytical precision; it adds noise.

**Note on recoding:** The v3 coded files have ~6 passages under this code. Before running v4 scripts, each should be manually recoded to the more specific code.

---

### Change 3: Broaden `Rejection_of_Multilateral_Governance`

**Current definition:** *rejection of international sustainability agreements, the 2030 Agenda, multilateral climate bodies...*

**Proposed broadening:** Remove the "sustainability" qualifier. Capture rejection of multilateral governance *in general* — UN reform, WEF authority, supranational bodies — when Milei frames these as illegitimate regardless of whether they are explicitly linked to climate governance.

**Reason:** Analysis of Categories sheet comment on this code: *"To consider a broad definition of rejection of multilateral governance in general not only environmental."* This is confirmed by Juani's comments on IDs #35 and #36: passages where Milei proposes a "freedom" agenda *through* multilateral institutions (not just against them) still reflect a delegitimizing rhetorical move — reframing the normative basis of multilateral cooperation.

**Boundary clarification:** The code should apply whenever Milei frames multilateral governance as epistemically or normatively illegitimate, even if the specific speech context is not about climate. The *use* of this rhetorical infrastructure for climate obstruction is established by the broader corpus, not by individual passages.

---

## D1.2 — Delegitimization of Public Science and Expertise

### Change 4: Merge `Attack_on_Universities` + `Attack_on_Public_Research_Institutions`

**Proposed new name:** `Attack_on_Universities_and_Research_Institutions`

**Reason:** Analysis of Categories: *"To bundle research institutions and universities — each time it is found: Delegitimization of scientific and professional institutions."* The two institutions are attacked through the same rhetorical mechanism (ideological capture, rent-seeking, inefficiency) and the distinction was not analytically productive in v3.

---

### Change 5: Merge `Attack_on_Experts_and_Technocrats` + `Rejection_of_Expert_Mediation`

**Proposed action:** Retire `Rejection_of_Expert_Mediation`. Absorb its content into `Attack_on_Experts_and_Technocrats`.

**Reason:** Analysis of Categories: *"Bundled with rejection of expert mediation (rarely found)."* ID #40: Germán flags `Rejection_of_Expert_Mediation` and says *"UNIFICAR CON ATTACKS ON EXPERTS AND TECHNOCRATIC ELITES."* In practice `Rejection_of_Expert_Mediation` was applied only twice in the corpus and always alongside `Attack_on_Experts_and_Technocrats`.

**Updated definition:** Delegitimization of expert authority — scientists, economists, policy specialists — as a political class that imposes knowledge on society rather than serving it, including arguments that expert bodies should not mediate policymaking. The "attack" and the "mediation rejection" are the same move stated differently.

---

### Change 6: Promote `Selective_Empiricism` to deductive sub-code of D1.2

**Current status:** Inductive category

**Proposed status:** Deductive sub-code under D1.2

**Reason:**
- Analysis of Categories sheet: adds `Selective_Empiricism` explicitly to the D1.2 "New" column, alongside the other deductive codes
- Juani (ID #8): *"could be a sub-category within 'Science and expertise', could be called: Selective scientific empiricism"*
- Juani (ID #47): *"to me selective empiricism/evidence is the most important sub-dimension here"*
- Germán (ID #47): flags it as duplicative for that specific passage — but the broader category is validated across the corpus

**Updated definition:** A rhetorical pattern in which Milei deploys the language of empirical authority exclusively for pro-market claims while simultaneously characterizing opposing institutional knowledge (including climate science) as ideologically captured and invalid. The dual move — appropriating empiricism for one side, denying it to the other — is the diagnostic feature. Distinct from `Pseudo_Science_or_Ideological_Science` (which labels science as ideological) because here Milei *claims the empirical ground* for his own position.

*Recognize by:* "La evidencia empírica es incuestionable" (about capitalism) followed immediately by dismissal of institutional science; invoking "science and data are on our side" while characterizing IPCC or sustainability science as ideological.

**Note:** With this promotion, the inductive section retains only `Temporal_Appropriation` and `Reported_Denial` — both of which face significant problems (see below).

---

## D1.3 — Cultural Backlash

### Change 7: Rename `Neo_Marxism` → `Anti_Socialism_Anti_Collectivism`

**Current name:** `Neo_Marxism`

**Proposed name:** `Anti_Socialism_Anti_Collectivism`

**Reason:**
- Analysis of Categories: *"Anti-socialism or anti-neo-marxism"* in the "New" column; comment: *"Look for a definition of this concept (cultural backlash / cultural battle)"*
- Juani flags this repeatedly: IDs #5, #9, #18, #41 — all suggest "anti-socialism" as a more precise label
- The current label "Neo_Marxism" is Milei's own polemical term; the analytical label should describe the rhetorical function, not replicate the target's framing

**Proposed definition update:** Framing environmentalism, the green agenda, or sustainability governance as expressions of socialism, collectivism, or Marxist politics — not as genuine environmental responses. The rhetorical move: sustainability governance is a *vehicle* for socialist state expansion ("watermelon politics"). Note that Milei uses "neo-marxismo" as a near-synonym for this cluster; the analytical label is `Anti_Socialism_Anti_Collectivism` to distinguish the researcher's code from Milei's own vocabulary.

**Also update D1.3 dimension name/description:** The current dimension name ("Woke / Cultural Backlash") is functional but both reviewers consistently use the phrase "cultural battle" (*batalla cultural*) when discussing these passages — which is also Milei's own framing. Consider renaming the sub-dimension to reflect this: *"Cultural Backlash / Civilizational Battle"* with a note that this maps to Milei's own *batalla cultural* frame.

---

### What stays the same in D1.3

`Woke_Bundling` and `Civilizational_Defense` are validated throughout. No definitional changes proposed.

**Boundary clarification between Neo_Marxism (now Anti_Socialism) and Civilizational_Defense:**
- Both reviewers flag IDs #27, #52, #67, #73 as having sub-dimension placement ambiguity within D1.3.
- Working rule: use `Civilizational_Defense` when the stakes are explicitly *existential* for Western civilization; use `Anti_Socialism_Anti_Collectivism` when the passage frames a specific policy or movement as socialist/collectivist. Many passages fit either — pick the dominant register and apply the overcoding rule.

---

## Inductive Categories

### Drop `Reported_Denial`

**Proposed action:** Remove this category entirely.

**Reason:** Germán (ID #4): *"N/A — no es dicho por él mismo en este momento, es más bien una referencia de dichos previos en entrevistas."* This is definitive: `Reported_Denial` codes speech *about* Milei (an opponent's paraphrase), not Milei's own discourse. Coding it was methodologically inconsistent from the start — the unit of analysis is Milei's primary discourse, not meta-commentary about it. The single instance in the corpus (ID #4) should be removed from the coded data.

---

### Restrict `Temporal_Appropriation` significantly

**Current status:** Inductive category with 3 coded instances

**Proposed action:** Retain the category conceptually but raise the application threshold substantially. In the v3 review, Germán rejected all 3 coded instances:
- ID #61: *"I will change it to D1.1 Anti-State/Anti-Bureaucratic or D1.2 Attack on Experts"*
- ID #66: *"NO. Eliminar."*
- ID #97: *"NO. ELIMINAR."*

**Why keep it at all:** The category captures a genuinely distinctive rhetorical move (co-opting sustainability's intergenerational vocabulary against itself), and its analytic value was endorsed in the v3 final report. But the application threshold in v3 was too loose — passages where Milei simply mentions the future or invokes generational rhetoric were coded as Temporal_Appropriation when the co-optation of sustainability's specific vocabulary was not actually present.

**Revised application rule:** Apply `Temporal_Appropriation` only when *both* conditions are met:
1. Milei uses vocabulary that is recognizably from sustainability discourse (futurity, intergenerational responsibility, protecting future generations, "el futuro")
2. He redirects that vocabulary explicitly *against* a sustainability governance mechanism (not just against the state in general)

Under this threshold, the v3 instances at IDs #61, #66, and #97 do not qualify. The analysis team should re-examine the full v3 corpus to identify whether any passage meets both conditions before carrying this category into v4 coding.

---

## Summary Table of All Changes

| Code | Status in v3 | Status in v4 | Rationale |
|---|---|---|---|
| `Market_Primacy` | D1.1 | **Unchanged** | Validated by both reviewers |
| `Anti_State_Anti_Bureaucratic` | D1.1 | **Unchanged** | Validated |
| `Anti_Casta` | D1.1 | **Unchanged** | Validated |
| `Delegitimization_of_Regulation` | D1.1 | **Expanded** — absorbs Deregulation_Benefits | Merge of two overlapping codes |
| `Deregulation_Benefits` | D1.1 | **Retired** | Merged into Delegitimization_of_Regulation |
| `Sustainability_as_Ideological_or_Harmful` | D1.1 | **Retired** | Redundant; recode affected passages |
| `Rejection_of_Multilateral_Governance` | D1.1 | **Broadened** — remove "environmental" qualifier | Reviewer consensus; broader scope |
| `Attack_on_Universities` | D1.2 | **Merged** into Attack_on_Universities_and_Research_Institutions | Bundled per reviewer consensus |
| `Attack_on_Public_Research_Institutions` | D1.2 | **Merged** | Same mechanism |
| `Attack_on_Experts_and_Technocrats` | D1.2 | **Expanded** — absorbs Rejection_of_Expert_Mediation | Validated; absorbs rarely-used code |
| `Rejection_of_Expert_Mediation` | D1.2 | **Retired** | Merged; rarely applied independently |
| `Climate_Skepticism_or_Dismissal` | D1.2 | **Unchanged** | Validated |
| `Pseudo_Science_or_Ideological_Science` | D1.2 | **Unchanged** | Validated (with note on D1.3 boundary) |
| `Selective_Empiricism` | INDUCTIVE | **Promoted** to D1.2 deductive sub-code | Reviewer consensus; analytically distinct |
| `Neo_Marxism` | D1.3 | **Renamed** → `Anti_Socialism_Anti_Collectivism` | More precise label; reduces mirroring of Milei's own vocabulary |
| `Woke_Bundling` | D1.3 | **Unchanged** | Validated |
| `Civilizational_Defense` | D1.3 | **Unchanged** | Validated |
| `Temporal_Appropriation` | INDUCTIVE | **Retained but restricted** — higher application threshold | All 3 v3 instances rejected by Germán |
| `Reported_Denial` | INDUCTIVE | **Dropped** | Not primary Milei discourse |

---

## Effect on Skills and Methodology

### `skills/discourse-coder-v3/SKILL.md` → update to v4

- Update sub-code lists in the coding guidance to reflect the merged and renamed codes
- Add the overcoding rule explicitly
- Update the annotation format if code names change (e.g., `[CODE: D1.2 > Selective_Empiricism]` is now deductive, not INDUCTIVE)
- Update `Closest D1 code` references for the promoted `Selective_Empiricism`

### `skills/qda-outputs/scripts/generate_xlsx.py` and `generate_html.py`

- Update the sub-code key mapping to use new names (`Anti_Socialism_Anti_Collectivism`, merged `Delegitimization_of_Regulation`, etc.)
- Remove retired codes from frequency table rows
- Update dimension color assignments if needed

### `analysis/results/methodology_summary.md`

- Add a section documenting the v3→v4 changes and their empirical justification (the peer review process)
- Update the sub-code count per dimension (from 7+6+3 → approximately 6+4+3)
- Note the overcoding protocol as a methodological addition

---

## Passages requiring recoding before v4 scripts run

These v3 annotations should be manually corrected in the coded speech files:

| ID | Current code | Recommended v4 code | Notes |
|---|---|---|---|
| #4 | IND > Reported_Denial | **Remove** | Not primary Milei discourse |
| #39 | D1.2 > Attack_on_Universities | D1.2 > Pseudo_Science (or keep under new Universities+Research code) | Germán: "pseudo-science or ideological science" |
| #40 | D1.2 > Rejection_of_Expert_Mediation | Merge with #39 under Attack_on_Experts | Germán: "UNIFICAR" |
| #43 | D1.3 > Neo_Marxism (stacked on #42) | **Remove** | Juani: overcoding |
| #49 | D1.3 > Neo_Marxism (stacked on #48) | **Remove** | Juani: overcoding |
| #61 | IND > Temporal_Appropriation | D1.1 > Anti_State_Anti_Bureaucratic | Germán recodes |
| #66 | IND > Temporal_Appropriation | **Remove** | Germán: eliminate |
| #80 | D1.1 > Deregulation_Benefits | **Remove** (or merge into adjacent passage) | Germán: lo eliminaría |
| #82 | D1.1 > Anti_State_Anti_Bureaucratic | **Remove** | Germán: lo eliminaría |
| #94 | D1.1 > Market_Primacy | **Remove** | Germán: lo eliminaría |
| #97 | IND > Temporal_Appropriation | **Remove** | Germán: ELIMINAR |
| #87 | D1.3 > Woke_Bundling | **Remove** or recode as generic D1.3 | Germán: "A lo sumo cultural battle" |
| #88 | D1.3 > Civilizational_Defense | **Remove** or recode as generic D1.3 | Germán: "muy rebuscado" |
| All SaIH | D1.1 > Sustainability_as_Ideological_or_Harmful | Recode to appropriate specific code | Category retired |

**Germán's two proposed additions (rows marked "SEE"):** Two passages from the corpus currently uncoded that Germán flags as D1.1 candidates. These should be reviewed and coded in v4 if they meet the codebook criteria:
1. *"Para tener una idea, desde la década del 70..."* — candidate for `Market_Primacy`
2. *"Y por qué fallaron todos nuestros intentos de salir..."* — candidate for `Market_Primacy` or `Delegitimization_of_Regulation`

---

## Open questions for team discussion

1. **D1.3 dimension name:** Should "Woke / Cultural Backlash" be renamed to "Cultural Backlash / Civilizational Battle" to better reflect the *batalla cultural* frame Milei himself uses? This improves analytical alignment but creates a naming tension (using the subject's own framing).

2. **`Sustainability_as_Ideological_or_Harmful` recoding:** Which passages currently coded SaIH are better captured by `Rejection_of_Multilateral_Governance` vs. `Neo_Marxism` / `Anti_Socialism_Anti_Collectivism`? The team should review the ~6 affected passages jointly before committing to recode decisions.

3. **`Temporal_Appropriation` survival:** Given that all 3 v3 instances were rejected by Germán, should the category be fully dropped from v4, or retained as a watchlist category for future speeches? The analytical concept is sound; the application was too loose. Decision: keep as inductive watchlist with the new stricter rule, do not apply it retroactively.

4. **Overcoding rule calibration:** The proposed "one primary code per passage" rule will lower overall annotation count. The team should agree on a target threshold for stacking: is 2 codes per passage ever acceptable? The v3 report notes that stacked codes reveal "rhetorical bundles" — that analytical value is worth preserving for a subset of passages.
