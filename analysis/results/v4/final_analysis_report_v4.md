# Final Analysis Report v4 — Updated (2026-10-11): Milei's Climate Narratives

**Version:** 4.0 (definition-review pass) | **Date:** 2026-10-11 | **Coded by:** Claude (discourse-coder-v4) with researcher review, under codebook v4 (definitions revised 2026-10-11) | **Supersedes for reporting purposes (earlier versions kept):** `final_analysis_report_v4_20260809.md` and `final_analysis_report_v4_20260719.md` (the 2026-07-19 report, formerly `final_analysis_report_v4.md`)

**Relationship to the article draft:** This report presents the current state of the Corpus A (presidential speeches) analysis described in Section 4 ("Empirical Research Design") of the article draft and is the results base for its Findings section. It uses the same terminology and coding scheme (Dimension 1 — Discursive Delegitimization; sub-dimensions D1.1/D1.2/D1.3; the fourteen sub-codes).

---

## What changed since the 2026-08-09 report

On 2026-10-11, a researcher review of the coded workbook found that three sub-code definitions were written around climate/environmentalism while the passages actually coded under them were broader, and that some passages coded as expert attacks were economic disagreements rather than attacks on experts. The review changed the corpus in two ways, both documented in `analysis/technical_memory.md` and `analysis/methodology_summary_v4.md`:

1. **Three definitions were broadened to match the coding** (`analysis/coding_book_v4.md`):
   - `Anti_Socialism_Anti_Collectivism` and `Civilizational_Defense` no longer require a climate or environmental reference; a climate link is an included case, justified by the Option A scope rule (general anti-collectivist and civilizational rhetoric is the discursive infrastructure later applied to climate governance).
   - `Pseudo_Science_or_Ideological_Science` now covers claims that *any* body of knowledge, or the institutions that produce it, is ideologically captured or epistemically unsound. The target is the knowledge production (theory, method, institution), not a specific finding and not people as a class.
   - A boundary was added: `Attack_on_Experts_and_Technocrats` targets people or professional authority as a class (credentials, competence, honesty, motives, track record); a purely economic disagreement is not an expert attack.
2. **Sixteen passages were removed** (workbook IDs #65, 80, 137, 170, 180, 186, 219, 226, 240, 373, 376, 480, 501, 503, 510, 586): thirteen Attack on Experts, two Pseudo-Science, one Anti-State, one Delegitimization of Regulation. Passage #585 was reviewed and kept by decision.

Effects: **total code instances fall from 613 to 597 (−16, −2.6%)**; Attack on Experts 32 → 20; Pseudo-Science 10 → 8; Anti-State 93 → 92; Delegitimization of Regulation 85 → 84. D1.1 377 → 375, D1.2 66 → 52, D1.3 unchanged at 170. No speech was left without codes by the removals; zero-code speeches remain 23. The corpus's three climate-signature sub-codes are unaffected (still 55).

Other points, stated rather than silently absorbed:
- **A claim in the 2026-08-09 report is corrected.** That report said explicit climate-science denial appeared "in only two speeches" (the 2023 debate and 2025 Davos). The coded data show `Climate_Skepticism_or_Dismissal` (7 codes) in **seven** speeches: the 2023 debate, CPAC 2024, the 2024 book presentation, the 2024 agricultural exhibition, the Fundación Faro dinner (Nov. 2024), Davos 2025 and CPAC Washington 2025. It is still the corpus's second-rarest sub-code, but it is not confined to two speeches.
- **The broadened definitions weaken the explicit climate link of three codes.** They should be reported as capturing the discursive infrastructure of climate rejection under the Option A rule, not climate talk itself. The climate-signature split below gives the climate-explicit view.
- **The quantitative pipeline was refreshed** (`analysis/results/v4/quant_analysis/`, memo dated 2026-10-11, n=597), resolving the August caveat that those outputs predated the correction.
- Sections not tied to the removed passages (flagship quotes, triangulation with D2, inductive categories) are carried over from the 2026-08-09 report. None of the removed passages belongs to a flagship speech.
- Source of truth: all figures were recomputed from the master workbook `qda_v4_coded_corpus_261011.xlsx` and the synced coded `.md` files (parser `skills/qda-outputs/scripts/corpus_data.py`); a sync dry run reports 0 differences.

---

## Executive Summary

Across the complete corpus of 193 speeches and public discourses delivered by Javier Milei as presidential candidate and President of Argentina (8 October 2023 – 29 April 2026), the discursive-delegitimization framework (Dimension 1) identifies 597 codeable passages. The central finding holds: 62.8% of codes target the legitimacy of state intervention and sustainability governance in the abstract (D1.1), 28.5% invoke cultural-backlash framing (D1.3), and only 8.7% attack public science and expertise (D1.2). Milei's climate obstruction is overwhelmingly institutional and economic-theoretical rather than scientific-denialist: explicit climate-science dismissal (`Climate_Skepticism_or_Dismissal`) is the second-rarest sub-code (7 instances, one each in seven speeches), while the anti-state, anti-"casta", and anti-regulatory infrastructure (`Anti_Casta`, 116 instances, is the most frequent sub-code) recurs constantly and is the load-bearing apparatus that climate-specific attacks plug into when they do appear. The three explicit climate-signature sub-codes (55 instances) split between speeches pre-flagged as high climate-relevance (42%) and speeches that were not (58%), direct quantitative support for the "Option A" scope decision. The single densest speech is still the 14 March 2026 Madrid Economic Forum address (21 codes), which contains no explicit climate content. The definition review tightened D1.2 in particular: with economic disputes no longer counted as expert attacks, science-and-expertise attacks are 8.7% of the corpus, and their share falls from 12.0% in 2024 to 4.2% in 2026.

---

## Corpus Overview

- **Speech events analyzed:** 193 (matching the master corpus database; all rows `coded = ok`)
- **Date range:** 2023-10-08 (second presidential debate) – 2026-04-29 (Expo EFI 2026 closing)
- **Speeches with ≥1 D1 code:** 170 of 193 (88%)
- **Genuine zero-code speeches:** 23 of 193 (12%), concentrated in `acto institucional` (5), `acto conmemorativo` (5), `bilateral/diplomatico` (4), and `cumbre internacional` (3)
- **Total coded passages / code annotations:** 597 (mean 3.09/speech, median 2, max 21)
- **Passages carrying two or more stacked codes:** 35 (5.9% of code annotations; 556 distinct passages)
- **Active/formalized inductive categories:** 0
- **Coding dimension:** D1 (Discursive Delegitimization) only, applied to speeches (Corpus A). D2 (State Capability Erosion / Corpus B) is a separate protocol.

**Table 1. Corpus and coding results at a glance**

| Metric | 2026-07-19 | 2026-08-09 | 2026-10-11 (this report) |
| ----- | ----- | ----- | ----- |
| Speech events | 193 | 193 | 193 |
| Speeches with ≥1 code | 160 (83%) | 170 (88%) | 170 (88%) |
| Zero-code speeches | 33 (17%) | 23 (12%) | 23 (12%) |
| Total code instances | 538 | 613 | 597 |
| Stacked-code passages | 34 | 36 | 35 |
| D1.1 share | 61.2% (329) | 61.5% (377) | 62.8% (375) |
| D1.2 share | 11.7% (63) | 10.8% (66) | 8.7% (52) |
| D1.3 share | 27.1% (146) | 27.7% (170) | 28.5% (170) |
| Climate-signature codes | 55 | 55 | 55 (unchanged) |

---

## Dimension 1 — Discursive Delegitimization: Key Findings

**Table 2. Sub-code frequencies, ranked**

| Rank | Sub-code | Sub-dimension | Count | Share of D1 |
| ----- | ----- | ----- | ----- | ----- |
| 1 | Anti_Casta | D1.1 | 116 | 19.4% |
| 2 | Anti_Socialism_Anti_Collectivism | D1.3 | 102 | 17.1% |
| 3 | Anti_State_Anti_Bureaucratic | D1.1 | 92 | 15.4% |
| 4 | Delegitimization_of_Regulation | D1.1 | 84 | 14.1% |
| 5 | Woke_Bundling | D1.3 | 41 | 6.9% |
| 6 | Market_Primacy | D1.1 | 35 | 5.9% |
| 7 | Civilizational_Defense | D1.3 | 27 | 4.5% |
| 8 | Sustainability_as_Ideological_or_Harmful | D1.1 | 24 | 4.0% |
| 8 | Rejection_of_Multilateral_Governance | D1.1 | 24 | 4.0% |
| 10 | Attack_on_Experts_and_Technocrats | D1.2 | 20 | 3.4% |
| 11 | Attack_on_Universities_and_Research_Institutions | D1.2 | 14 | 2.3% |
| 12 | Pseudo_Science_or_Ideological_Science | D1.2 | 8 | 1.3% |
| 13 | Climate_Skepticism_or_Dismissal | D1.2 | 7 | 1.2% |
| 14 | Selective_Empiricism | D1.2 | 3 | 0.5% |

### D1.1 — Delegitimization of State Intervention and Sustainability Governance (62.8%, 375 codes)

The dominant sub-dimension by a wide margin. `Anti_Casta` (116) is the most frequent sub-code in the corpus, ahead of `Anti_Socialism_Anti_Collectivism` (102). The three generic D1.1 sub-codes `Anti_Casta`, `Anti_State_Anti_Bureaucratic` (92) and `Delegitimization_of_Regulation` (84) account for 292 of 597 codes (48.9%). Climate and environmental institutions are never singled out for special condemnation in this register; they are swept into a pre-existing, much larger anti-institutional frame that recurs in nearly every speech genre. `Delegitimization_of_Regulation`'s flagship claim, that "market failures do not exist" ("los fallos de mercado... no existen"), recurs verbatim or near-verbatim across at least five speeches (Davos 2024, 2025, 2026; Apertura 144°, 2026; Madrid Economic Forum, 2026), each time eliminating the standard economic justification for environmental regulation (externalities) at the level of first principles, without engaging climate science.

`Sustainability_as_Ideological_or_Harmful` (24) and `Rejection_of_Multilateral_Governance` (24) carry the corpus's *named* climate-obstruction content: the UN "Zero Emission" critique, the Club of Rome dismissal, the "Agenda Verde"/demographic-collapse claim, and the periglaciares/glacier-law passage. Their counts are unchanged by the review.

### D1.2 — Delegitimization of Public Science and Expertise (8.7%, 52 codes)

The smallest sub-dimension, and smaller after the review (10.8% → 8.7%). It consists of `Attack_on_Experts_and_Technocrats` (20, 38.5% of D1.2), `Attack_on_Universities_and_Research_Institutions` (14, 26.9%), `Pseudo_Science_or_Ideological_Science` (8, 15.4%), `Climate_Skepticism_or_Dismissal` (7, 13.5%) and `Selective_Empiricism` (3, 5.8%). Direct climate-science dismissal accounts for 7 codes, one in each of seven speeches (2023 debate, CPAC 2024, book presentation 2024, agricultural exhibition 2024, Fundación Faro dinner 2024, Davos 2025, CPAC Washington 2025). `Attack_on_Experts_and_Technocrats` mostly targets economists, consultants and forecasters, not climate scientists; after the review it retains attacks on the standing of those groups (credentials, competence, honesty, track record) and no longer includes economic disagreements as such. `Pseudo_Science_or_Ideological_Science` is a small code (8 instances in 7 speeches: Davos 2024 ×2, Premio Juan de Mariana 2024, Tech Forum 2024, Davos 2025, a 2025 book presentation, the Faro year-end dinner 2025, Madrid Economic Forum 2026). Its broadened definition covers claims that economics, think tanks or international bodies produce ideologically captured knowledge, not only climate science.

### D1.3 — Cultural Backlash (28.5%, 170 codes)

Unchanged in count by the review (its share rises only because the corpus total fell). `Anti_Socialism_Anti_Collectivism` (102) is the second most frequent sub-code overall and, under its broadened definition, is applied to anti-collectivist rhetoric whether or not climate is mentioned (in a keyword check, only 13 of 102 passages mention climate or the environment in the passage or its memo). `Woke_Bundling` (41) is the mechanism by which climate governance is contaminated by association with reproductive-rights and gender-ideology framing. `Civilizational_Defense` (27) positions Western civilization as under existential threat; it too is not conditional on a climate reference.

---

## Rhetorical Evolution Across the Corpus (2023–2026)

**Table 3. Density and composition by year**

| Year | Speeches | D1.1 | D1.2 | D1.3 | Total codes | Avg./speech | D1.1 share | D1.2 share | D1.3 share |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 2023 | 5 | 13 | 2 | 3 | 18 | 3.60 | 72.2% | 11.1% | 16.7% |
| 2024 | 88 | 170 | 34 | 79 | 283 | 3.22 | 60.1% | 12.0% | 27.9% |
| 2025 | 71 | 133 | 12 | 56 | 201 | 2.83 | 66.2% | 6.0% | 27.9% |
| 2026 | 29 | 59 | 4 | 32 | 95 | 3.28 | 62.1% | 4.2% | 33.7% |

**Raw code density does not decline steadily across the presidency.** It oscillates between 2.83 and 3.60 codes per speech (2023 is five speeches around the transition), with partial-year 2026 matching 2024. Per 1,000 words (pooled), the quarterly rate falls from 2.39 in 2023Q4 and 1.31 in 2024Q1 to a plateau of roughly 0.5–1.0 thereafter (see `quant_analysis_memo.md`). The July report's "steady decline" claim should not be reused.

**D1.2 recedes as a share of the discourse** (12.0% in 2024, 6.0% in 2025, 4.2% in 2026), and the decline is steeper after the review than in the August report (14.7% → 7.7% → 5.2%), because the removed passages were concentrated in the 2024 expert-attack content. **D1.3 climbs** (16.7% → 27.9% → 27.9% → 33.7%) while D1.1 remains the dominant baseline (60–72% every year). The defensible version of the evolution finding is therefore compositional: a roughly stable volume of rhetoric shifts away from the empirical/scientific register (D1.2) toward the civilizational register (D1.3), while the anti-statist/institutional core (D1.1) stays constant. Milei increasingly grounds regulatory and anti-collectivist arguments in property-rights philosophy (Hoppe, Huerta de Soto) rather than empirical or scientific claims.

**Milestone speeches (unchanged by the review):**

- **14 March 2026, Madrid Economic Forum:** the densest speech in the corpus (21 codes), overtaking Davos 2024 (19). It contains zero climate-specific content: its codes are `Anti_Casta` (named-businessman rent-seeking attacks), `Anti_State_Anti_Bureaucratic`, `Delegitimization_of_Regulation`, `Anti_Socialism_Anti_Collectivism`, `Civilizational_Defense` and one `Pseudo_Science_or_Ideological_Science` instance. It is the clearest single-speech illustration of the generic discursive infrastructure operating at full intensity independent of any climate content.
- **29 April 2026, Expo EFI closing:** 17 codes, the third-densest speech.
- **79th UN General Assembly (24 Sept. 2024):** 13 codes; the densest in climate-signature codes (8).
- **15 November 2024, CPAC Investors** (10 codes) and **10 March 2026, Gala Algemeiner** (7).

---

## Discursive Patterns by Venue and Audience

**Table 4. Code density and composition by event type (top 10 by total codes)**

| Event type (`tipo`) | n | Total codes | Avg./speech | D1.1 share | D1.2 share | D1.3 share |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| Foro económico | 21 | 112 | 5.33 | 60% | 12% | 29% |
| Evento ideológico/político | 21 | 88 | 4.19 | 43% | 8% | 49% |
| Acto institucional | 26 | 59 | 2.27 | 66% | 10% | 24% |
| Fundación / think tank | 13 | 47 | 3.62 | 57% | 13% | 30% |
| Cumbre internacional | 12 | 40 | 3.33 | 80% | 5% | 15% |
| Bolsa / cámara de comercio | 12 | 31 | 2.58 | 68% | 6% | 26% |
| Cadena nacional | 10 | 31 | 3.10 | 81% | 3% | 16% |
| Premio / reconocimiento | 14 | 28 | 2.00 | 46% | 14% | 39% |
| Empresa | 10 | 28 | 2.80 | 79% | 11% | 11% |
| Sectorial | 7 | 22 | 3.14 | 77% | 5% | 18% |

Economic and institutional venues run heavily D1.1 (`cadena nacional` 81%, `cumbre internacional` 80%, `empresa` 79%, `sectorial` 77%). Ideological/political events and awards ceremonies invert toward D1.3 (49% and 39%): cultural-backlash framing is the register reserved for identity-aligned or ceremonial audiences. `Foro económico` (Davos-style keynotes) is the highest-volume category (112 codes). A Kruskal-Wallis test on codes per 1,000 words across `tipo` (n≥5, k=15) is significant (H=29.80, p=0.008); summits are the densest major venue (2.90 /1k, about three times `foro económico`), because their speeches are short.

**Table 5. Code density by country (n ≥ 3 speeches)**

| País | n | Total codes | Avg./speech |
| ----- | ----- | ----- | ----- |
| Suiza (Davos) | 5 | 32 | 6.40 |
| España | 8 | 45 | 5.62 |
| EE.UU. | 21 | 92 | 4.38 |
| Brasil | 4 | 16 | 4.00 |
| Argentina | 129 | 368 | 2.85 |
| Uruguay | 3 | 6 | 2.00 |
| Paraguay | 5 | 9 | 1.80 |
| Israel | 10 | 17 | 1.70 |

Foreign venues carry higher average density than domestic ones (Argentina 2.85/speech, 368 of 597 codes, 61.6%); on a per-word basis the difference is smaller (0.88 vs 1.62 /1k, Mann-Whitney p=0.066, not significant at 0.05).

**Table 6. Venue groups (six analytical groups; `venue_group`)**

| Venue group | Speeches | Codes | Mean codes/speech | Mean /1k | D1.1 / D1.2 / D1.3 (% of codes) |
|---|---|---|---|---|---|
| Economic & Business Forums | 61 | 234 | 3.84 | 0.85 | 65.4 / 9.8 / 24.8 |
| State & Institutional Acts | 37 | 90 | 2.43 | 0.91 | 71.1 / 7.8 / 21.1 |
| Awards, Academic & Think Tanks | 33 | 98 | 2.97 | 0.79 | 59.2 / 11.2 / 29.6 |
| International & Diplomatic | 26 | 62 | 2.38 | 2.03 | 69.4 / 3.2 / 27.4 |
| Ideological & Political Events | 22 | 91 | 4.14 | 1.81 | 42.9 / 9.9 / 47.3 |
| Commemorative & Community | 14 | 22 | 1.57 | 0.93 | 81.8 / 0.0 / 18.2 |

Density does not differ significantly between the six groups (Kruskal-Wallis H=7.53, p=0.18), but the dimension mix does (χ²=29.2, dof=10, p=0.0011, Cramér's V=0.16; descriptive, since code instances within a speech are not independent). Claims about group differences should therefore rest on the dimension mix, not on density. Ideological & Political Events is the only group where D1.3 outweighs D1.1.

---

## Co-occurrence and Rhetorical Bundles

35 passages (5.9% of code annotations) carry two or more stacked codes under the codebook's overcoding rule. The most frequent pairings (count ≥ 2):

**Table 7. Most frequent stacked-code pairs**

| Co-occurring pair | Count | What the bundle achieves |
| ----- | ----- | ----- |
| `Anti_State_Anti_Bureaucratic` + `Delegitimization_of_Regulation` | 3 | Fuses "bureaucrats are parasites" with "regulation is illegitimate" (generic, non-climate) |
| `Rejection_of_Multilateral_Governance` + `Woke_Bundling` | 3 | Institutions (UN, WEF) framed as vehicles for the broader "woke" project |
| `Rejection_of_Multilateral_Governance` + `Sustainability_as_Ideological_or_Harmful` | 3 | Delegitimizes both the institution proposing climate policy and the policy |
| `Sustainability_as_Ideological_or_Harmful` + `Climate_Skepticism_or_Dismissal` | 2 | Pairs "the policy is harmful" with "the science is doubtful" |
| `Climate_Skepticism_or_Dismissal` + `Woke_Bundling` | 2 | Contaminates climate-science denial by association with the "woke" target |
| `Anti_Casta` + `Anti_State_Anti_Bureaucratic` | 2 | Elite-capture and organizational-form critiques applied together |
| `Sustainability_as_Ideological_or_Harmful` + `Woke_Bundling` | 2 | The climate-is-socialism-in-disguise move |
| `Rejection_of_Multilateral_Governance` + `Civilizational_Defense` | 2 | Elevates institutional rejection to defense of Western civilization |
| `Sustainability_as_Ideological_or_Harmful` + `Civilizational_Defense` | 2 | Dominion-theology justification for resource extraction (Bolsa de Córdoba) |
| `Delegitimization_of_Regulation` + `Rejection_of_Multilateral_Governance` | 2 | Ties deregulation arguments to rejection of the international bodies proposing regulation |
| `Delegitimization_of_Regulation` + `Sustainability_as_Ideological_or_Harmful` | 2 | Treats environmental regulation as both illegitimate and harmful |

Dense multi-code bundling remains concentrated around the explicit climate-adjacent content; most of the 597 codes are single, standalone passages. Several co-coded passages (for example the same Davos 2025 and UN 2024 passages carrying two or three codes) are candidates for an overcoding check, which has not yet been run.

**Co-occurrence at speech level** (phi coefficients, from the quant memo): the strongest pairs are `Pseudo_Science_or_Ideological_Science` ↔ `Selective_Empiricism` (0.42) and `Rejection_of_Multilateral_Governance` ↔ `Woke_Bundling` (0.40). A k-means solution on speeches with at least three codes (n=92, silhouette 0.13, weak) separates a small, dense international-sovereigntist mode (n=7, 4.1 /1k, 46% `Rejection_of_Multilateral_Governance`) from a large anti-casta/anti-state baseline (n=53) and an anti-collectivist/culture-war mode (n=26).

---

## Testing the "Discursive Infrastructure" Thesis

The article's Section 4.2 scope rule ("Option A") holds that generalized anti-state, anti-regulatory, and anti-"casta" rhetoric should be coded wherever it appears, because it constitutes the discursive infrastructure that climate-specific attacks later plug into. Using the three sub-codes that most explicitly carry climate content (`Sustainability_as_Ideological_or_Harmful`, `Rejection_of_Multilateral_Governance`, `Climate_Skepticism_or_Dismissal`): of 55 climate-signature instances, 23 (42%) occur in speeches the master database flags as high climate-relevance (`clima = ✔`); 32 (58%) occur in speeches flagged only "possible" (`~`, 26) or unflagged (blank, 6). This split is unchanged by the definition review. Because three definitions were broadened, it also serves as the climate-explicit cross-check: the climate-signature codes are exactly those whose definitions were not broadened. Speeches flagged `✔` are about five times denser in D1 codes than the rest (4.82 vs ~1.0 codes per 1,000 words; Kruskal-Wallis p=0.0002), validating the flag as a speech-selection heuristic.

---

## Key Quotes and Exemplary Passages

The flagship passages identified in the 19 July and 9 August reports are unaffected by the review (none of the removed passages belongs to those speeches): the "el fallo del mercado es un oxímoron" claim (Davos 2024); the Club of Rome/Malthus passage (Luna Park, 2024); the WEF "Zero Emission" attack (UN General Assembly, 2024); the "five cycles" passage (Davos 2025); the periglaciares/glacier-law passage (Corrientes, 2025), the corpus's most important D1→D2 bridge; the "ambientalistas idiotas extremos" dominion-theology passage (Bolsa de Córdoba, 2026); the "Agenda Verde" passage (Debate "Keynes y la Teoría General," 2026); the Hoppe natural-law regulation claim (Davos 2026); the "Los fallos de mercado... no existen" restatement (Madrid Economic Forum, 14 March 2026); and the Madrid address as a whole (21 codes, no climate content). Full text and analysis are in the earlier reports.

A note on the "five cycles" passage: the codebook cites it as the clearest example of `Selective_Empiricism` ("science and the data are on our side"), but it is coded `Climate_Skepticism_or_Dismissal` and `Pseudo_Science_or_Ideological_Science`. A recoding was considered on 2026-10-11 and not adopted; the discrepancy between the codebook example and the coded sub-code is an open item.

---

## Inductive Categories

**No inductive categories are formalized in this pass.** The two previously noted candidate patterns (theological/dominion framing; primitivism-as-regulation metaphor) have not been systematically re-examined; a full inductive-category review is recommended before the next codebook revision.

---

## Notes for Triangulation with Dimension 2 (Corpus B)

Unchanged from earlier reports. D2 (State Capability Erosion) analysis proceeds separately (budget analysis in `analysis/D2_budget/`); the periglaciares/glacier-law reform (13 November 2025) remains the highest-priority D1→D2 bridge.

---

## Conclusions and Next Steps

1. **The central finding is unchanged and slightly sharper.** D1.1 (62.8%) dwarfs D1.2 (8.7%) and D1.3 is 28.5%. Climate obstruction operates primarily through a generic anti-institutional, anti-elite frame rather than through disputing climate data; `Anti_Casta` is the single most frequent code (116).
2. **Do not reuse the "declining density" claim.** Density is roughly stable; the defensible evolution finding is compositional (D1.2 receding from 12.0% to 4.2%, D1.3 rising, D1.1 constant).
3. **State the scope of three codes accurately in the paper.** `Anti_Socialism_Anti_Collectivism`, `Civilizational_Defense` and `Pseudo_Science_or_Ideological_Science` capture the discursive infrastructure of climate rejection under the Option A rule, not climate talk itself; the climate-signature split (42%/58%) is the climate-explicit view.
4. **Cite corpus statistics from this report (or later), not earlier versions.** Update the article draft's Table 3 / Section 4.4 figures (613 → 597; D1.1/D1.2/D1.3 = 375/52/170) and the sub-code counts for `Attack_on_Experts_and_Technocrats` (32 → 20), `Pseudo_Science_or_Ideological_Science` (10 → 8), `Anti_State_Anti_Bureaucratic` (93 → 92) and `Delegitimization_of_Regulation` (85 → 84).

**Open items:**
- `Woke_Bundling` shows the same definition drift (9 of 41 passages mention climate in the passage); wording not yet revised.
- Overcoding check on identical passages carrying two or three codes.
- `Selective_Empiricism`: the codebook example (Davos 2025) is not coded as such; rows #225 and #242 are progress narratives that fit the dual-move definition poorly.
- Continue coding newly delivered speeches; re-run `sync_xlsx_to_md.py` and regenerate this report after each batch.

---

## Output Paths

| File | Path |
| ----- | ----- |
| This report (current; canonical name) | `analysis/results/v4/final_analysis_report_v4.md` |
| Prior reports (superseded for reporting, not deleted) | `analysis/results/v4/final_analysis_report_v4_20260809.md`, `analysis/results/v4/final_analysis_report_v4_20260719.md` |
| Master workbook (source of truth) | `analysis/results/v4/qda_v4_coded_corpus_261011.xlsx` |
| Frequency tally | `analysis/coded_speeches/v4/frequency_tally_v4.json` |
| Code counts per speech | `analysis/results/v4/milei_corpus_v4_code_counts.csv` |
| Quantitative analysis memo | `analysis/results/v4/quant_analysis/quant_analysis_memo.md` |
| Definition review record | `analysis/technical_memory.md`, `analysis/methodology_summary_v4.md`, `analysis/coding_book_v4.md` |
