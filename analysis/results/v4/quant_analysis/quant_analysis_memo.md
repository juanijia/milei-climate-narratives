---
title: "Quantitative Analysis of the D1 Code Counts — Milei Climate Narratives Corpus (v4)"
date: 2026-10-11
source_data: analysis/results/v4/milei_corpus_v4_code_counts.csv
scope: "Descriptive, cross-tabulation, and pattern analysis of all 193 coded speeches (Dimension 1 only, codebook v4), incl. venue-group overview"
supersedes: "2026-10-11 first version (n=613 codes). Re-run after the 2026-10-11 v4 definition review (16 passages removed, n=597); produced by quant_analysis.ipynb"
---

# Quantitative Analysis Memo — v4 Corpus (n=193 speeches, 597 D1 code instances)

This memo reports the quantitative pass over `milei_corpus_v4_code_counts.csv`, executed in `quant_analysis.ipynb` (pandas/scipy/scikit-learn). All 193 speeches have `coded=ok`. The authoritative total is **597** code instances (Excel `Coded Passages` sheet). It was 613 before the 2026-10-11 definition review, in which 16 passages were removed (13 Attack on Experts, 2 Pseudo-Science, 1 Anti-State, 1 Delegitimization of Regulation) and three definitions were broadened; **all figures below have been recomputed**. Word counts come from the matched raw transcripts in `data/raw_speeches/`. Rate figures are **codes per 1,000 words** ("/1k") unless stated otherwise. "Mean /1k" is the mean of per-speech rates; "pooled /1k" is total codes ÷ total words for the group.

## 1. Overview

- 597 D1 code instances across 193 speeches (mean 3.09/speech, median 2, max 21); 764,943 words in total (mean 3,963 per speech).
- By dimension: **D1.1 = 375 (62.8%)**, D1.2 = 52 (8.7%), D1.3 = 170 (28.5%). D1.2 remains the least-used dimension.
- Sub-code ranking: `Anti_Casta` (116) > `Anti_Socialism_Anti_Collectivism` (102) > `Anti_State_Anti_Bureaucratic` (92) > `Delegitimization_of_Regulation` (84) > `Woke_Bundling` (41) > `Market_Primacy` (35) > `Civilizational_Defense` (27) > `Rejection_of_Multilateral_Governance` (24) = `Sustainability_as_Ideological_or_Harmful` (24) > `Attack_on_Experts_and_Technocrats` (20) > `Attack_on_Universities_and_Research_Institutions` (14) > `Pseudo_Science_or_Ideological_Science` (8) > `Climate_Skepticism_or_Dismissal` (7) > `Selective_Empiricism` (3).
  - The most climate-specific sub-codes are among the rarest in absolute terms; their concentration matters more than their count (§5).
- 23/193 speeches (12%) carry zero D1 codes. They cluster in ceremonial/diplomatic genres: `acto institucional` (5), `acto conmemorativo` (5/5 of that type), `bilateral / diplomatico` (4), `cumbre internacional` (3). By country: Argentina 13, Israel 4, EE.UU. 2. By clima flag: 19 blank, 4 `~`, none `✔`.

**Charts:** `02_subcode_ranking.png`, `03_codes_histogram.png`
## 2. Time trend

Codes per 1,000 words (pooled) by quarter: 2023Q4 **2.39** (5 speeches, transition) → 2024Q1 1.31 → 2024Q2 0.58 → 2024Q3 0.96 → 2024Q4 0.73 → 2025Q1 0.98 → 2025Q2 0.46 → 2025Q3 0.90 → 2025Q4 0.79 → 2026Q1 0.76 → 2026Q2 0.70 (9 speeches, partial quarter).

Reading: a sharp drop after the 2023 campaign/transition period, then a **plateau at roughly 0.5–1.0 /1k** with quarter-to-quarter noise (no steady decline). Raw volume peaks in 2024Q4 (97 codes) and 2024Q3 (86), driven by speech volume (34 and 20 speeches). (The time-trend section was dropped from the notebook; these figures are computed from `corpus_enriched.csv`.)

**Chart:** `01_time_series.png` (from an earlier run)
## 3. Venue and country effects

**By `tipo`** (n≥5 groups, k=15) — Kruskal-Wallis on /1k: H=29.80, **p=0.008** (significant venue-type effect; computed from `corpus_enriched.csv`, not currently a notebook cell). Mean /1k (n): `cumbre internacional` **2.90** (12) > `evento ideologico/politico` 1.44 (21) > `bilateral / diplomatico` 1.32 (13) > `empresa` 1.30 (10) > `cadena nacional` 1.29 (10) > `acto conmemorativo/patrio` 1.14 (6) > `sectorial` 0.88 (7) > `foro economico` 0.86 (21) > `premio / reconocimiento` 0.84 (14) > `clase magistral / universidad` 0.81 (5) > `acto institucional` 0.80 (26) > `consejo empresarial` 0.64 (5) > `fundacion / think tank` 0.63 (13) > `bolsa / camara de comercio` 0.48 (12) > `acto conmemorativo` 0.00 (5). (Single-speech types such as `debate presidencial`, 9.62 /1k on 312 words, are excluded from the test.)

International summits are the densest major venue, about 3× `foro economico`: short, high-stakes speeches (mean 1,083 words) against long keynotes (7,748 words) that dilute density.

**By `pais`** (n≥3 groups, k=8) — Kruskal-Wallis H=15.17, **p=0.034**: Brasil 3.22 (n=4, G20) > EE.UU. 2.30 (21) > Suiza 1.75 (5, Davos) > Paraguay 1.50 > Hungria 1.48 > España 1.31 (8) > Uruguay 1.22 > **Argentina 0.88 (129)** > Israel 0.78 (10) > the rest (n≤2). Argentina vs. all international: 0.88 vs 1.62 /1k (medians 0.66 vs 0.91), Mann-Whitney **p=0.066**, i.e. borderline and not significant at 0.05; the country effect is mostly about specific international venues rather than a blanket "more intense abroad" pattern.

**Tables:** `pais_stats.csv`
## 4. Venue groups (6 groups) and scope

`venue_group` collapses the 23 `tipo` values into six analytical groups (`corpus_metadata.TIPO_GROUP`; same as the Venue Group column of the Excel workbook); `scope` = National (Argentina) vs International. Table in `venue_group_stats.csv`.

| Venue group | Speeches (%) | Codes (%) | Mean codes/speech | Zero-code speeches | Mean /1k (pooled) | D1.1 / D1.2 / D1.3 (% of group codes) |
|---|---|---|---|---|---|---|
| Economic & Business Forums | 61 (31.6%) | 234 (39.2%) | 3.84 | 1 (1.6%) | 0.85 (0.68) | 65.4 / 9.8 / 24.8 |
| State & Institutional Acts | 37 (19.2%) | 90 (15.1%) | 2.43 | 6 (16.2%) | 0.91 (0.87) | 71.1 / 7.8 / 21.1 |
| Awards, Academic & Think Tanks | 33 (17.1%) | 98 (16.4%) | 2.97 | 1 (3.0%) | 0.79 (0.57) | 59.2 / 11.2 / 29.6 |
| International & Diplomatic | 26 (13.5%) | 62 (10.4%) | 2.38 | 7 (26.9%) | 2.03 (1.82) | 69.4 / 3.2 / 27.4 |
| Ideological & Political Events | 22 (11.4%) | 91 (15.2%) | 4.14 | 2 (9.1%) | 1.81 (0.98) | 42.9 / 9.9 / 47.3 |
| Commemorative & Community | 14 (7.3%) | 22 (3.7%) | 1.57 | 6 (42.9%) | 0.93 (1.15) | 81.8 / 0.0 / 18.2 |
| **Total** | **193** | **597** | **3.09** | **23 (11.9%)** | **1.12 (0.78)** | **62.8 / 8.7 / 28.5** |

- **Where the codes are:** Economic & Business Forums supply 39% of all codes from 32% of speeches, simply because the speeches are long (mean 5,654 words); their density is below average. Ideological & Political Events and International & Diplomatic have the highest densities (1.8 and 2.0 mean /1k), with short speeches in the latter.
- **Density differences between groups are not significant:** Kruskal-Wallis on /1k, H=7.53, p=0.18, ε²=0.014 (negligible effect). The strong `tipo` effect in §3 is driven by specific venue types (summits), not by the six-group aggregation.
- **Dimension mix does differ:** chi-square venue group × dimension (code counts), χ²=29.2, dof=10, **p=0.0011**, Cramér's V=0.16 (small-to-moderate; treat as descriptive since code instances within a speech are not independent). Ideological & Political Events is the only group where D1.3 (47.3%) outweighs D1.1 (42.9%); State & Institutional Acts and Commemorative are the most D1.1-heavy; D1.2 is highest in Awards/Academic/Think Tanks (11.2%), Ideological & Political (9.9%) and Economic & Business Forums (9.8%) and nearly absent in International & Diplomatic (3.2%) and Commemorative (0%).
- **Scope** (speeches / codes): National 129 / 368; International 64 / 229. Mean /1k 0.88 vs 1.62 (Mann-Whitney p=0.066). Scope composition differs a lot by group: International & Diplomatic is 20 intl vs 6 national speeches; Awards, Academic & Think Tanks 19 vs 14; Ideological & Political 13 vs 9; State & Institutional Acts is almost wholly national (35 of 37; 1 of 90 codes international); Economic & Business Forums 52 national vs 9 international.

**Chart / tables:** `11_venue_group_overview.png`, `venue_group_stats.csv`, `venue_group_by_scope_speeches.csv`, `venue_group_by_scope_codes.csv`, `dim_by_venue_group.csv`, `subcode_composition_by_venue_group.csv`
## 5. Climate-focused deep dive

**Validating the `clima` heuristic:** mean /1k by flag: blank 1.03 (n=72), `~` 0.88 (n=111), **`✔` 4.82 (n=10)**; Kruskal-Wallis **p=0.0002**. Speeches flagged as high climate-relevance are ~5× denser in D1 codes than the rest (blank and `~` do not differ meaningfully), validating the heuristic as a speech-selection filter.

**Testing the "discursive infrastructure" thesis** (CLAUDE.md Option A scope): three sub-codes are used as climate-signature markers (`Sustainability_as_Ideological_or_Harmful`, `Rejection_of_Multilateral_Governance`, `Climate_Skepticism_or_Dismissal`); there are 55 instances corpus-wide. **23 (42%) occur in `clima=✔` speeches; 32 (58%) occur in speeches flagged `~` or blank.** The anti-environmental framing therefore appears well beyond the speeches an analyst would pre-select as "about climate", supporting coding climate-adjacent rhetoric wherever it appears.

**Top speeches by climate-signature density** (excerpting candidates):
1. **79th UN General Assembly (2024-09-24)**: 8 instances, 7.50 /1k, the densest.
2. Presidential debate (2023-10-08): 2 instances, 6.41 /1k (312 words).
3. 80th UN General Assembly (2025-09-24): 5 instances, 3.02 /1k.
4. G20 Leaders' Summit, session II (2024-11-18): 2 instances, 2.60 /1k.
5. G20 intervention (2024-11-18): 1 instance, 1.14 /1k.
6. Nuclear-plan announcement (2024-12-21): 1 instance, 0.81 /1k.
Further down: CPAC Budapest (3), Davos 2025 (3), livestock/agriculture exhibition (3).

The pattern is concentration in multilateral and international forums (UN twice, G20, Mercosur, Davos), consistent with §3.

**Charts:** `04_clima_density.png`, `05_climate_signature_time.png`

## 6. Co-occurrence and rhetorical-mode clusters

**Co-occurrence** (phi coefficients, sub-code presence per speech): strongest pairs are **`Pseudo_Science_or_Ideological_Science` ↔ `Selective_Empiricism` (0.42)**, **`Rejection_of_Multilateral_Governance` ↔ `Woke_Bundling` (0.40)**, `Attack_on_Universities_and_Research_Institutions` ↔ `Climate_Skepticism_or_Dismissal` (0.27), `Sustainability_as_Ideological_or_Harmful` ↔ `Attack_on_Experts_and_Technocrats` (0.24), `Delegitimization_of_Regulation` ↔ `Pseudo_Science_or_Ideological_Science` (0.23), `Market_Primacy` ↔ `Delegitimization_of_Regulation` (0.23), `Rejection_of_Multilateral_Governance` ↔ `Civilizational_Defense` (0.23), and `Sustainability_as_Ideological_or_Harmful` ↔ `Climate_Skepticism_or_Dismissal` (0.22). Rejection of multilateral bodies is rhetorically bundled with the anti-"woke"/civilizational frame, and sustainability-as-ideology links governance and epistemic attack.

**Clustering** (k-means on code-composition profiles; speeches with ≥3 codes, n=92; k=4, silhouette 0.13, i.e. weak, reported as such):
- **Cluster 1 — "International sovereigntist" (n=7, 4.11 /1k, the densest):** `Rejection_of_Multilateral_Governance` 46%, `Woke_Bundling` 18%, `Delegitimization_of_Regulation` 15%. Summits (4 of 7), EE.UU. 3.
- **Cluster 0 — "Anti-casta / anti-state baseline" (n=53, 1.26 /1k):** `Anti_Casta` 26%, `Anti_Socialism_Anti_Collectivism` 18%, `Delegitimization_of_Regulation` 18%, `Anti_State_Anti_Bureaucratic` 17%. The default register: economic forums 11, institutional acts 8, think tanks 6; 41 of 53 are Argentine speeches.
- **Cluster 3 — "Anti-collectivist / culture-war" (n=26, 1.43 /1k):** `Anti_Socialism_Anti_Collectivism` 21%, `Anti_Casta` 18%, `Anti_State_Anti_Bureaucratic` 15%, `Woke_Bundling` 14%. Ideological/political events 8, economic forums 6.
- **Cluster 2 — "Sustainability / climate-skeptic" (n=6, 2.55 /1k):** `Sustainability_as_Ideological_or_Harmful` 29%, `Delegitimization_of_Regulation` 16%, `Climate_Skepticism_or_Dismissal` 10%; too small to interpret beyond being a distinct mode.

*Change from the 613-code run:* the former "Expert-attack / anti-state keynote" cluster no longer appears separately (13 of the 16 removed passages were Attack on Experts); its speeches now fall into the anti-casta/anti-state baseline (Cluster 0). Cluster labels are not stable across runs, so compare by profile, not number.

Clusters by venue group (speeches with ≥3 codes): International & Diplomatic is 5 of 8 in Cluster 1; Ideological & Political 8 of 14 in Cluster 3; State & Institutional 12 of 13 in Cluster 0; Economic & Business Forums 22 of 37 in Cluster 0 and 10 in Cluster 3; Awards/Academic/Think Tanks 13 of 18 in Cluster 0. By `tipo`: `cumbre internacional` 4 of 5 in Cluster 1; `acto institucional` 8 of 8 and `foro economico` 11 of 15 in Cluster 0. Tables: `cluster_by_venue_group.csv`, `cluster_by_tipo.csv`, `cluster_by_pais.csv`.

**Charts:** `06_cooccurrence_heatmap.png`, `07_cluster_pca.png` (PC1+PC2 explain a small share of variance; the 2D plot is illustrative only)
## 7. Code composition by venue type and country

The **mix** of dimensions shifts with context (`dim_by_tipo.csv`, `dim_by_pais.csv`, `subcode_composition_by_*.csv`; % of the group's codes).

**By `tipo` (n≥5):** D1.1-heavy: `acto conmemorativo/patrio` 100% (7 codes), `cadena nacional` 81%, `cumbre internacional` 80%, `empresa` 79%, `clase magistral / universidad` 78% (18 codes), `sectorial` 77%. D1.3-heavy: `bilateral / diplomatico` 62.5% (16 codes), `evento ideologico/politico` 49%, `premio / reconocimiento` 39%. D1.2 peaks in `premio / reconocimiento` (14%), `fundacion / think tank` (13%), `foro economico` (12%), `consejo empresarial` (11%) and `empresa` (11%), and is 0% in diplomatic, commemorative and `clase magistral` venues and 3% in `cadena nacional`.

**By `pais` (n≥3):** Argentina (65/10/25 % D1.1/D1.2/D1.3), EE.UU. (63/4/33), Suiza (62.5/22/16), Brasil (62.5/6/31) and Israel (65/0/35) are D1.1-led; España (49% D1.1, 47% D1.3) and Paraguay (44/0/56, only 9 codes) lean D1.3; Suiza stands out for D1.2 (22%, Davos).

**Takeaway:** climate-obstruction rhetoric operates as governance/regulation delegitimization before economic and institutional audiences, and as cultural-backlash framing in ideological and diplomatic settings, with the summit-specific anti-multilateral mode (Cluster 1) as the most intense expression.

**Charts:** `08_subcode_composition_by_tipo.png`, `09_subcode_composition_by_pais.png`, `10_dimension_composition.png`
## 8. Implications for the paper draft

1. The timeline and venue patterns suggest obstruction rhetoric is **forum-specific** rather than diffuse: a baseline anti-casta/anti-collectivist register (Cluster 0) plus a sharper international sovereigntist mode (Cluster 1) at multilateral venues.
2. The 42%/58% split (§5) supports the Option A scope decision (coding climate-adjacent rhetoric regardless of explicit climate mention).
3. The 79th UN General Assembly speech is the strongest single candidate for close qualitative reading.
4. D1.2 stays the weakest dimension (52 instances, 8.7%): Milei's obstruction runs far more through governance and culture-war framing than direct science denial. State this as a finding.
5. Venue-group results can be reported descriptively (§4); the density test across the six groups is not significant (p=0.18), so claims about group differences should rest on the dimension mix (p=0.0011) rather than on density.

6. Because three definitions were broadened (Anti_Socialism, Civilizational_Defense, Pseudo_Science), the paper should state that these codes capture the discursive infrastructure of climate rejection under the Option A scope rule, not climate talk itself; §5 (42% of climate-signature codes inside `clima=✔` speeches) gives the climate-explicit view.
## Output files

All under `analysis/results/v4/quant_analysis/`, regenerated by `quant_analysis.ipynb` (run from inside the project folder; `BASE_DIR` is auto-detected):
- `corpus_enriched.csv` (= `milei_corpus_v4_data_analysis.csv`), `long_format.csv`, `clustered_speeches.csv`
- `tipo_stats.csv`, `pais_stats.csv`, `venue_group_stats.csv`, `venue_group_by_scope_speeches.csv`, `venue_group_by_scope_codes.csv`
- `dim_by_tipo.csv`, `dim_by_pais.csv`, `dim_by_venue_group.csv`, `subcode_composition_by_tipo.csv`, `subcode_composition_by_pais.csv`, `subcode_composition_by_venue_group.csv`
- `cluster_by_venue_group.csv`, `cluster_by_tipo.csv`, `cluster_by_pais.csv`
- `charts/01_time_series.png` … `charts/11_venue_group_overview.png`
- This memo.

