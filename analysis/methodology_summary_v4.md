# Methodology Summary v4: Milei's Climate Narratives

**Date:** July 2026  
**Version:** 4.0  
**Previous version:** `analysis/methodology_summary_v3.md`

---

## Overview

Version 4 refines the analytical framework following a systematic peer review of the v3 coded corpus by Juani and Germán (June 2026). The two-dimensional theoretical architecture and the data-source separation established in v3 are preserved unchanged. The changes in v4 are exclusively at the **sub-code level**: merging redundant codes, renaming one sub-code to improve analytical precision, promoting one inductive category to deductive status, and retiring two inductive categories. A cross-cutting overcoding rule is formalized for the first time.

The v3 corpus itself is **not re-coded in v4** — the v3 coded files remain as the authoritative v3 record. V4 applies to new coding passes on additional speeches. The v3 passages affected by sub-code changes are documented in the recoding manifest below, to be applied when generating the v4 Excel and HTML outputs.

---

## The V4 Analytical Framework

### Architecture (unchanged from v3)

The two-corpus, two-dimension structure established in v3 is carried forward without modification:

**Corpus A — Presidential Speeches**  
Coded with **Dimension 1 — Discursive Delegitimization** only. Unit of analysis: the rhetorical passage.

**Corpus B — Formal Documentation**  
Coded with **Dimension 2 — State Capability Erosion** only. Unit of analysis: the formal institutional act.

The dual mechanism — rhetoric delegitimizes; formal action dismantles — is demonstrated by triangulating the two corpora independently. Dimension 2 is not affected by any v4 changes.

---

### Dimension 1 — Discursive Delegitimization (v4 sub-code schema)

#### D1.1 — Delegitimization of State Intervention and Sustainability Governance

| Sub-code | Status in v4 | Change from v3 |
|---|---|---|
| `Market_Primacy` | Active | Unchanged |
| `Anti_State_Anti_Bureaucratic` | Active | Unchanged |
| `Anti_Casta` | Active | Unchanged |
| `Delegitimization_of_Regulation` | Active | **Expanded** — absorbs former `Deregulation_Benefits` |
| `Deregulation_Benefits` | Retired | **Merged** into `Delegitimization_of_Regulation` |
| `Sustainability_as_Ideological_or_Harmful` | Active | **Restored** — retained in v4 after review |
| `Rejection_of_Multilateral_Governance` | Active | **Broadened** — scope extended beyond environmental governance |

**D1.1 sub-code count: 6** (down from 7 in v3, due to merger)

#### D1.2 — Delegitimization of Public Science and Expertise

| Sub-code | Status in v4 | Change from v3 |
|---|---|---|
| `Attack_on_Universities_and_Research_Institutions` | Active | **New name** — merges `Attack_on_Universities` + `Attack_on_Public_Research_Institutions` |
| `Attack_on_Universities` | Retired | Merged |
| `Attack_on_Public_Research_Institutions` | Retired | Merged |
| `Attack_on_Experts_and_Technocrats` | Active | **Expanded** — absorbs `Rejection_of_Expert_Mediation` |
| `Rejection_of_Expert_Mediation` | Retired | Merged |
| `Climate_Skepticism_or_Dismissal` | Active | Unchanged |
| `Pseudo_Science_or_Ideological_Science` | Active | Unchanged |
| `Selective_Empiricism` | Active (deductive) | **Promoted** from inductive |

**D1.2 sub-code count: 5** (down from 6 in v3, due to mergers; net +0 after promotion of Selective_Empiricism)

#### D1.3 — Cultural Backlash

| Sub-code | Status in v4 | Change from v3 |
|---|---|---|
| `Woke_Bundling` | Active | Unchanged |
| `Anti_Socialism_Anti_Collectivism` | Active | **Renamed** from `Neo_Marxism` |
| `Civilizational_Defense` | Active | Unchanged |

**D1.3 sub-code count: 3** (unchanged)

#### Inductive categories

| Category | Status in v4 | Change from v3 |
|---|---|---|
| `Selective_Empiricism` | Promoted to D1.2 deductive | Removed from inductive section |
| `Temporal_Appropriation` | **Eliminated** | Removed; retained on watchlist only |
| `Reported_Denial` | **Retired** | Removed entirely |

---

## Detailed Rationale for Each Change

### 1. Merge `Deregulation_Benefits` into `Delegitimization_of_Regulation`

**Why:** Both reviewers identified these as two faces of the same rhetorical move — Milei almost never makes the negative case (regulation is illegitimate) without implying the positive case (deregulation is beneficial), and vice versa. Keeping them separate created artificial frequency splits without adding analytical precision. The merged code captures the full argument structure.

**Effect on corpus:** 9 passages previously coded `Deregulation_Benefits` (#13, #17, #54, #69, #75, #76, #84, #85, #89) are renamed to `Delegitimization_of_Regulation`. Passage #80 is removed (see overcoding section below).

---

### 2. Restore `Sustainability_as_Ideological_or_Harmful`

**Why:** The v4 proposal document recommended retiring this code on the grounds of redundancy. After review, it is restored. The code captures a distinct rhetorical register — framing the *policy response* to climate as misguided or harmful — that is not fully covered by either `Rejection_of_Multilateral_Governance` (which targets governance architecture) or `Anti_Socialism_Anti_Collectivism` (which targets ideological affiliation). Passages like "prejuicios ambientalistas absurdos" and "malos resultados" clearly fit this code and do not map cleanly to either alternative.

**Effect on corpus:** No changes required — v3 passages coded SaIH remain as coded.

---

### 3. Broaden `Rejection_of_Multilateral_Governance`

**Why:** Reviewer comment on the Analysis of Categories sheet: *"To consider a broad definition of rejection of multilateral governance in general not only environmental."* Milei's rejection of multilateral governance operates at a foundational level — sovereignty, national self-determination, freedom from supranational constraint — that encompasses but is not limited to environmental governance. Restricting the code to environmental governance missed passages where the institutional rejection is analytically relevant for the article's argument even when the specific content is broader.

**Effect on corpus:** Definition update only. No passage renames required; applies to new coding going forward.

---

### 4. Merge `Attack_on_Universities` + `Attack_on_Public_Research_Institutions`

**Why:** Analysis of Categories sheet: *"To bundle research institutions and universities — each time it is found: Delegitimization of scientific and professional institutions."* Both sub-codes are activated by the same rhetorical mechanism (institutional capture, rent-seeking, ideological contamination) and were applied interchangeably in v3 practice. Bundling them sharpens the code without losing information.

**Effect on corpus:** 3 passages coded `Attack_on_Universities` (#39, #50, #78) renamed to `Attack_on_Universities_and_Research_Institutions`. No `Attack_on_Public_Research_Institutions` instances appear in the v3 corpus.

---

### 5. Merge `Rejection_of_Expert_Mediation` into `Attack_on_Experts_and_Technocrats`

**Why:** Analysis of Categories sheet: *"Bundled with rejection of expert mediation (rarely found)."* Passage #40: reviewer confirmed merge. The institutional role critique ("experts should not mediate policy") and the personal/class delegitimization ("these experts are ideological parasites") are analytically unified — Milei always moves from one to the other in the same passage.

**Effect on corpus:** 1 passage (#40) renamed from `Rejection_of_Expert_Mediation` to `Attack_on_Experts_and_Technocrats`.

---

### 6. Rename `Neo_Marxism` → `Anti_Socialism_Anti_Collectivism`

**Why:** Both reviewers consistently reached for "anti-socialism" or "anti-collectivism" language when reviewing D1.3 passages. The original label `Neo_Marxism` mirrors Milei's own polemical vocabulary — analytically, the code captures a function (framing environmental governance as a vehicle for socialist state expansion), not a doctrinal category. The new label is more analytically neutral and broader, capturing collectivism framings that do not explicitly invoke Marxism.

**Effect on corpus:** 5 passages (#18, #41, #56, #96, and any others coded `Neo_Marxism`) renamed to `Anti_Socialism_Anti_Collectivism`. Passages #43 and #49 are removed (overcoding — see below).

---

### 7. Promote `Selective_Empiricism` to D1.2 deductive sub-code

**Why:** Analysis of Categories sheet explicitly adds `Selective_Empiricism` to the D1.2 "New" column alongside the other deductive codes. One reviewer: *"could be a sub-category within 'Science and expertise'"*; the other: *"to me, selective empiricism/evidence is the most important sub-dimension here."* The pattern — appropriating empirical authority for pro-market claims while denying it to climate science — is consistent and analytically distinctive enough to stand as a permanent deductive code.

**Effect on corpus:** 2 passages (#8, #47) reclassified from `INDUCTIVE > Selective_Empiricism` to `D1.2 > Selective_Empiricism`. The INDUCTIVE tag is removed.

---

### 8. Eliminate `Temporal_Appropriation`

**Why:** All three v3 instances were rejected by peer reviewer: #61 (*"I will change it to D1.1 or D1.2"*), #66 (*"NO. Eliminar."*), #97 (*"NO. ELIMINAR."*). The application threshold in v3 was too low — passages where Milei invokes the future or generational language without specifically co-opting sustainability's intergenerational vocabulary were incorrectly coded. The category is eliminated from active use; it is retained on the watchlist with a stricter two-condition application rule in case the pattern appears unambiguously in future speeches.

**Effect on corpus:**  
- #61: reclassified to `D1.1 > Anti_State_Anti_Bureaucratic`  
- #66, #97: removed entirely

---

### 9. Retire `Reported_Denial`

**Why:** Reviewer (#4): *"N/A — no es dicho por él mismo en este momento, es más bien una referencia de dichos previos en entrevistas."* The category codes an opponent's reported-speech account of Milei's position, not Milei's own primary discourse. The unit of analysis for Dimension 1 is Milei's own speech; third-party accounts of it are outside scope.

**Effect on corpus:** 1 passage (#4, Bregman's paraphrase in the 2023 Presidential Debate) removed.

---

### 10. Overcoding rule (new in v4)

**Why:** The most consistent cross-cutting signal from both reviewers — flagged on at least 12 passages — is stacking codes on the same passage when one primary code is sufficient.

**Formal rule (added to analyst instructions):** Apply one primary code per passage. Stack a second code only if it captures a *genuinely distinct* rhetorical move that the primary code misses. Test: if the additional code were removed, would the passage still yield the same core analytical insight? If yes, drop the additional code.

**Effect on corpus — specific removals per reviewer:**

| ID | Code removed | Reason |
|---|---|---|
| #43 | `Neo_Marxism` (stacked on #42 `Woke_Bundling`) | Overcoding — same passage |
| #49 | `Neo_Marxism` (stacked on #48 `Woke_Bundling`) | Overcoding — same passage |
| #80 | `Deregulation_Benefits` | Too thin; remove per reviewer |
| #82 | `Anti_State_Anti_Bureaucratic` | Not directly climate-relevant per reviewer |
| #87 | `Woke_Bundling` | Too generic; not clearly climate-adjacent |
| #88 | `Civilizational_Defense` | Speculative application per reviewer |
| #94 | `Market_Primacy` | Not relevant per reviewer |

---

## Complete V3 → V4 Recoding Manifest

The following 30 changes should be applied to the v3 corpus data before generating v4 outputs. Changes are listed by passage ID.

### Renames (code name changes only — passage and memo unchanged)

| ID | Current code | V4 code |
|---|---|---|
| #8 | `INDUCTIVE > Selective_Empiricism` | `D1.2 > Selective_Empiricism` |
| #13 | `D1.1 > Deregulation_Benefits` | `D1.1 > Delegitimization_of_Regulation` |
| #17 | `D1.1 > Deregulation_Benefits` | `D1.1 > Delegitimization_of_Regulation` |
| #18 | `D1.3 > Neo_Marxism` | `D1.3 > Anti_Socialism_Anti_Collectivism` |
| #39 | `D1.2 > Attack_on_Universities` | `D1.2 > Attack_on_Universities_and_Research_Institutions` |
| #40 | `D1.2 > Rejection_of_Expert_Mediation` | `D1.2 > Attack_on_Experts_and_Technocrats` |
| #41 | `D1.3 > Neo_Marxism` | `D1.3 > Anti_Socialism_Anti_Collectivism` |
| #47 | `INDUCTIVE > Selective_Empiricism` | `D1.2 > Selective_Empiricism` |
| #50 | `D1.2 > Attack_on_Universities` | `D1.2 > Attack_on_Universities_and_Research_Institutions` |
| #54 | `D1.1 > Deregulation_Benefits` | `D1.1 > Delegitimization_of_Regulation` |
| #56 | `D1.3 > Neo_Marxism` | `D1.3 > Anti_Socialism_Anti_Collectivism` |
| #61 | `INDUCTIVE > Temporal_Appropriation` | `D1.1 > Anti_State_Anti_Bureaucratic` |
| #69 | `D1.1 > Deregulation_Benefits` | `D1.1 > Delegitimization_of_Regulation` |
| #75 | `D1.1 > Deregulation_Benefits` | `D1.1 > Delegitimization_of_Regulation` |
| #76 | `D1.1 > Deregulation_Benefits` | `D1.1 > Delegitimization_of_Regulation` |
| #78 | `D1.2 > Attack_on_Universities` | `D1.2 > Attack_on_Universities_and_Research_Institutions` |
| #84 | `D1.1 > Deregulation_Benefits` | `D1.1 > Delegitimization_of_Regulation` |
| #85 | `D1.1 > Deregulation_Benefits` | `D1.1 > Delegitimization_of_Regulation` |
| #89 | `D1.1 > Deregulation_Benefits` | `D1.1 > Delegitimization_of_Regulation` |
| #96 | `D1.3 > Neo_Marxism` | `D1.3 > Anti_Socialism_Anti_Collectivism` |

### Recodes (dimension or sub-code change)

| ID | Current code | V4 code | Source |
|---|---|---|---|
| #61 | `INDUCTIVE > Temporal_Appropriation` | `D1.1 > Anti_State_Anti_Bureaucratic` | Reviewer |

### Removals (passage deleted from corpus)

| ID | Current code | Reason |
|---|---|---|
| #4 | `INDUCTIVE > Reported_Denial` | Not primary Milei discourse |
| #43 | `D1.3 > Neo_Marxism` | Overcoding on same passage as #42 |
| #49 | `D1.3 > Neo_Marxism` | Overcoding on same passage as #48 |
| #66 | `INDUCTIVE > Temporal_Appropriation` | Category eliminated |
| #80 | `D1.1 > Deregulation_Benefits` | Removed per reviewer |
| #82 | `D1.1 > Anti_State_Anti_Bureaucratic` | Removed per reviewer |
| #87 | `D1.3 > Woke_Bundling` | Removed per reviewer |
| #88 | `D1.3 > Civilizational_Defense` | Removed per reviewer |
| #94 | `D1.1 > Market_Primacy` | Removed per reviewer |
| #97 | `INDUCTIVE > Temporal_Appropriation` | Category eliminated |

### Proposed additions (Germán's 'SEE' proposals — require team review)

| Proposed ID | Passage | Suggested code |
|---|---|---|
| #SEE-1 | *"Para tener una idea, desde la década del 70 hasta acá el mundo bajó la pobreza del 40% al 9%..."* | `D1.1 > Market_Primacy` |
| #SEE-2 | *"Y por qué fallaron todos nuestros intentos de salir. La respuesta es simple: porque nunca fuimos suficientemente libres"* | `D1.1 > Market_Primacy` or `D1.1 > Delegitimization_of_Regulation` |

---

## Expected Effect on Corpus Counts

Applying the v4 recoding manifest to the v3 corpus (98 annotations) produces an estimated **v4 baseline corpus of ~88 annotations** before any new speeches are coded:

- 98 v3 annotations  
- −10 removals (IDs #4, #43, #49, #66, #80, #82, #87, #88, #94, #97)  
- +0 to +2 proposed additions (pending team review)  
- = ~88–90 annotations

Dimension distribution will shift slightly due to the `Selective_Empiricism` reclassification (from INDUCTIVE to D1.2), which increases the D1.2 count by 2.

---

## Applying the Codebook to the Full Corpus

The v4 codebook and skill are applied going forward to the **full corpus of Milei speeches and discourses as President**, not only the pre-selected climate-flagged subset used to build v1–v3. The corpus is tracked in the master database, `data/sources/milei_discursos_index_2023-2026_updated260718.csv.csv` — 193 rows covering every recorded speech/discourse from 10 December 2023 to 30 April 2026. Coding proceeds in batches of 5 (see `workflows/3_narrative_analyst.md`), prioritizing rows flagged `clima = ✔` or `~` in the database; as of this writing, 9 speeches have been coded under v4 and the remaining ~184 are outstanding.

The two tables below summarize the full corpus by `pais` (country of the venue) and `tipo` (broad event category), as recorded in the master database. These are corpus-composition tables, not codebook-frequency tables — they describe *what was said and where*, not yet *how it was coded*.

### Corpus by country (`pais`, 14 values)

| País | N | % |
|---|---|---|
| argentina | 129 | 66.8% |
| ee.uu. | 21 | 10.9% |
| israel | 10 | 5.2% |
| españa | 8 | 4.1% |
| suiza | 5 | 2.6% |
| paraguay | 5 | 2.6% |
| brasil | 4 | 2.1% |
| uruguay | 3 | 1.6% |
| italia | 2 | 1.0% |
| hungria | 2 | 1.0% |
| el salvador | 1 | 0.5% |
| alemania | 1 | 0.5% |
| rep. checa | 1 | 0.5% |
| chile | 1 | 0.5% |
| **Total** | **193** | **100.0%** |

Two-thirds of the corpus (129/193) is delivered domestically; the largest foreign-venue concentration is the United States (21, largely CPAC, Mar-a-Lago, and Washington/New York institutional appearances), followed by Israel (10, mostly bilateral and commemorative), and Spain (8, Madrid-centered ideological and forum events). The remaining 10 countries each account for 5 or fewer speeches.

### Corpus by event category (`tipo`, 23 values)

| Tipo | N | % |
|---|---|---|
| acto institucional | 26 | 13.5% |
| foro economico | 21 | 10.9% |
| evento ideologico/politico | 21 | 10.9% |
| premio / reconocimiento | 14 | 7.3% |
| bilateral / diplomatico | 13 | 6.7% |
| fundacion / think tank | 13 | 6.7% |
| cumbre internacional | 12 | 6.2% |
| bolsa / camara de comercio | 12 | 6.2% |
| cadena nacional | 10 | 5.2% |
| empresa | 10 | 5.2% |
| sectorial | 7 | 3.6% |
| acto conmemorativo/patrio | 6 | 3.1% |
| acto conmemorativo | 5 | 2.6% |
| consejo empresarial | 5 | 2.6% |
| clase magistral / universidad | 5 | 2.6% |
| foro economico / empresarial | 4 | 2.1% |
| comunitario / religioso | 3 | 1.6% |
| debate presidencial | 1 | 0.5% |
| organismo internacional | 1 | 0.5% |
| evento empresarial | 1 | 0.5% |
| acto institucional / bilateral | 1 | 0.5% |
| evento economico / cultural | 1 | 0.5% |
| foro economico / financiero | 1 | 0.5% |
| **Total** | **193** | **100.0%** |

The three largest categories — acto institucional, foro economico, and evento ideologico/politico — together account for over a third of the corpus (68/193, 35.3%) and correspond to the venues where D1.1 (state/market framing) and D1.3 (cultural backlash) content has concentrated so far in the v4-coded batch (WEF Davos, CPAC, apertura de sesiones ordinarias). The long tail of single-instance categories (debate presidencial, organismo internacional, etc.) reflects genuinely singular events rather than a coding artifact — each was manually assigned by the researchers during the CSV cleanup.

---

## Key Analytical Questions for V4

The questions from v3 are carried forward, with one update:

1. **Distribution across D1 sub-dimensions:** How does Milei's rhetoric distribute across D1.1, D1.2, and D1.3 with the revised sub-code schema? Does the D1.1 dominance hold after the `Deregulation_Benefits` merger?

2. **Rhetorical evolution over time:** Does the balance across D1.1/D1.2/D1.3 shift across the corpus (2023–2026)? Does the removal of overcoded passages alter the trajectory finding from v3?

3. **`Sustainability_as_Ideological_or_Harmful` function:** With the code restored, does it cluster in specific venues (Apertura speeches) or time periods? How does it relate to `Rejection_of_Multilateral_Governance`?

4. **`Selective_Empiricism` as deductive code:** Now that `Selective_Empiricism` is a formal D1.2 sub-code, does its frequency change significantly in new coding passes? Is it better understood as a D1.2 code or does it operate across D1.1 and D1.2?

5. **Triangulation with D2:** Once the formal documentation corpus is coded with D2, how does the rhetoric in Corpus A map onto the formal actions in Corpus B? Do high-intensity D1.1 speeches precede or accompany D2.3 formal actions? (unchanged from v3)

---

## V4 Output Structure

| Output | Path |
|---|---|
| V4 Coding book | `analysis/coding_book_v4.md` |
| V4 Methodology summary | `analysis/methodology_summary_v4.md` (this document) |
| V4 Coded speeches | `analysis/coded_speeches/v4/` |
| V4 Frequency tally | `analysis/coded_speeches/v4/frequency_tally_v4.json` |
| V4 Final report | `analysis/results/v4/final_analysis_report_v4.md` |

Prior versions (v1, v2, v3) remain untouched in their respective directories.
