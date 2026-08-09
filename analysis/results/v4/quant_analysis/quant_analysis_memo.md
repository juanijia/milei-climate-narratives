---
title: "Quantitative Analysis of the D1 Code Counts — Milei Climate Narratives Corpus (v4)"
date: 2026-07-20
source_data: analysis/results/v4/milei_corpus_v4_code_counts.csv
scope: "Descriptive, cross-tabulation, and pattern analysis of all 193 coded speeches (Dimension 1 only, codebook v4)"
---

# Quantitative Analysis Memo — v4 Corpus (n=193 speeches, 538 D1 code instances)

This memo reports a full quantitative pass over `milei_corpus_v4_code_counts.csv`, executed in Python (pandas/scipy/scikit-learn). All 193 speeches have `coded=ok`. Word counts were computed from the matched raw transcripts in `data/raw_speeches/` (via the `matched_coded_file` column) to normalize code counts by speech length — this matters because venue types differ hugely in length (a `cadena nacional` address runs ~3,000 words; a `foro economico` keynote can run ~7,700). All rate figures below are **codes per 1,000 words** unless stated otherwise.

## 1. Overview

- 538 total D1 code instances across 193 speeches (mean 2.79/speech, median 2, max 19).
- Split by dimension: **D1.1 (State Intervention & Sustainability Governance) = 329 (61.2%)**, D1.2 (Public Science & Expertise) = 63 (11.7%), D1.3 (Cultural Backlash) = 146 (27.1%). D1.2 is by far the least-used dimension — expertise/science attacks are a minority rhetorical move relative to anti-state and cultural-backlash framing.
- Sub-code ranking (total instances): `Anti_Casta` (99) > `Anti_Socialism_Anti_Collectivism` (86) > `Anti_State_Anti_Bureaucratic` (84) > `Delegitimization_of_Regulation` (69) > `Woke_Bundling` (41) > `Attack_on_Experts_and_Technocrats` (31) > `Market_Primacy` (29) > `Rejection_of_Multilateral_Governance` (24) ≈ `Sustainability_as_Ideological_or_Harmful` (24) > `Civilizational_Defense` (19) > `Attack_on_Universities...` (14) > `Pseudo_Science...` (8) > `Climate_Skepticism_or_Dismissal` (7) > `Selective_Empiricism` (3).
  - The three most climate-specific sub-codes are among the rarest in absolute terms — but see §4, their concentration and reach matter more than their raw count.
- 33/193 speeches (17%) carry zero D1 codes. These cluster in ceremonial/diplomatic genres — `acto conmemorativo` (5/5 zero-coded), `bilateral/diplomatico` (5/13), `acto institucional` (7/26) — and disproportionately in Israel (6/10 Israel speeches are zero-coded, mostly Holocaust-memorial-type events). This is a genre effect, not under-coding: these are ceremonial speeches with little policy content.

**Chart:** `03_codes_histogram.png`

## 2. Time trend

Quarterly code density (codes per 1,000 words) **declines over the presidency**: 2.39 (2023Q4, transition period) → ~0.6–1.3 through 2024–2025 → 0.44 (2026Q1) → 0.28 (2026Q2, latest full quarter). Raw code volume per quarter is noisier (driven by how many speeches fall in each quarter), but the normalized density shows a real downward drift. This is worth flagging for the draft: either the anti-establishment framing intensity is cooling as the government matures, or it is being reserved for fewer, more targeted occasions (see §3 — international summits carry the highest density).

**Chart:** `01_time_series.png`

## 3. Venue and country effects

**By `tipo`** (speech-type), restricted to categories with n≥5 for stable estimates — Kruskal-Wallis H=32.4, **p=0.0035** (significant venue effect):

| tipo | n | mean codes/1k | median |
|---|---|---|---|
| cumbre internacional | 12 | **2.90** | 1.57 |
| empresa | 10 | 1.36 | 1.18 |
| cadena nacional | 10 | 1.29 | 0.99 |
| acto conmemorativo/patrio | 6 | 1.14 | 1.14 |
| bilateral / diplomatico | 13 | 1.10 | 0.86 |
| evento ideologico/politico | 21 | 1.10 | 0.99 |
| sectorial | 7 | 0.91 | 0.83 |
| acto institucional | 26 | 0.74 | 0.83 |
| foro economico | 21 | 0.68 | 0.44 |
| fundacion / think tank | 13 | 0.67 | 0.62 |
| consejo empresarial | 5 | 0.67 | 0.66 |
| clase magistral / universidad | 5 | 0.63 | 0.70 |
| premio / reconocimiento | 14 | 0.58 | 0.33 |
| bolsa / camara de comercio | 12 | 0.51 | 0.48 |
| acto conmemorativo | 5 | 0.00 | 0.00 |

Notable and slightly counter-intuitive: **international summits (`cumbre internacional`) have the highest density of any major venue type**, more than double `foro economico` (Davos-style keynotes). Summits are short, high-stakes, and rhetorically dense; the long-form economic keynotes dilute their code density over much more text even though they may carry more raw code instances.

**By `pais`** (n≥3 groups) — Kruskal-Wallis H=14.3, **p=0.046** (significant, weaker than venue-type effect):

Brasil (3.22, n=4, G20-driven) > Suiza (1.75, n=5, Davos) > EE.UU. (1.64, n=21) > Paraguay (1.50) > Hungria (1.48) > Uruguay (1.22) > España (1.00) > **Argentina (0.86, n=129)** > Chile (0.60) > Israel (0.42, n=10) > Alemania (0.31) > Rep. Checa (0.23) > Italia (0.16) > El Salvador (0.00).

Argentina vs. all-international binary comparison is **not** significant on its own (Mann-Whitney p=0.82) — the country effect is really about *specific* international venues (G20/Davos/UN-adjacent summits) rather than a blanket "more anti-establishment abroad" pattern. Israel is a clear low-density outlier, consistent with the zero-code finding in §1 (diplomatic/memorial content).

**Charts:** `tipo_stats.csv`, `pais_stats.csv` (full tables)

## 4. Climate-focused deep dive

**Validating the `clima` heuristic:** mean code density by clima flag — blank (0.90/1k, n=72) ≈ `~` (0.73/1k, n=111) << **`✔` (4.82/1k, n=10)**. Kruskal-Wallis **p=0.0001**. The heuristic strongly predicts code density: speeches flagged as high climate-relevance are ~5-6x denser in D1 codes than others. This is a meaningful validation of the corpus-selection heuristic itself.

**Testing the "discursive infrastructure" thesis** (CLAUDE.md's Option A scope note — that anti-environmental framing operates even in passages/speeches with no explicit climate mention): defining three sub-codes as the clearest "climate-signature" markers — `Sustainability_as_Ideological_or_Harmful`, `Rejection_of_Multilateral_Governance`, `Climate_Skepticism_or_Dismissal` — there are 55 total instances corpuswide. **Only 23 (42%) occur in `clima=✔` speeches; 32 (58%) occur in speeches flagged `~` or blank.** This is a substantive finding for the paper: the anti-environmental framing genuinely bleeds beyond the speeches an analyst would pre-select as "about climate," supporting the project's decision (documented in CLAUDE.md) to code climate-adjacent rhetoric wherever it appears rather than gating on an explicit climate/2030-Agenda mention per passage.

**Top speeches by climate-signature density** (candidates for qualitative excerpting in the draft):

1. **79th UN General Assembly (2024-09-24)** — 8 climate-signature instances, 7.50/1k words. By far the single densest anti-environmental speech in the corpus. Strong excerpt candidate.
2. Presidential debate (2023-10-08) — 2 instances, 6.41/1k (very short speech, 312 words).
3. 80th UN General Assembly (2025-09-24) — 5 instances, 3.02/1k.
4. G20 Leaders' Summit, session II, Brazil (2024-11-18) — 2 instances, 2.60/1k.
5. CPAC Budapest (2026-03-21) — 3 instances, 0.80/1k.
6. WEF Davos 2025 (2025-01-23) — 3 instances, 0.67/1k.

Pattern: climate-obstruction rhetoric concentrates heavily in **multilateral/international forums** (UN General Assembly twice, G20, Mercosur, Davos) rather than domestic broadcasts — consistent with the venue-effect finding in §3 that summits carry the highest density overall.

**Charts:** `04_clima_density.png`, `05_climate_signature_time.png`

## 5. Co-occurrence and rhetorical-mode clusters

**Co-occurrence** (phi coefficients on sub-code presence/absence per speech): the strongest pairings are `Pseudo_Science_or_Ideological_Science` ↔ `Selective_Empiricism` (0.42, both D1.2), and — substantively more interesting — **`Rejection_of_Multilateral_Governance` ↔ `Woke_Bundling` (0.40)** and `Rejection_of_Multilateral_Governance` ↔ `Civilizational_Defense` (0.27). This suggests a fused frame in which rejecting international climate/governance bodies is rhetorically bundled with a broader anti-"woke" cultural-backlash narrative, not argued on its own technical/economic terms. Also notable: `Sustainability_as_Ideological_or_Harmful` co-occurs with both `Climate_Skepticism_or_Dismissal` (0.22) and `Attack_on_Experts_and_Technocrats` (0.24) — a coherent D1.1↔D1.2 "climate-obstruction cluster" bridging governance delegitimization and epistemic attack.

**Chart:** `06_cooccurrence_heatmap.png`

**Rhetorical-mode clustering** (k-means on code-composition profiles — i.e., "shape" of each speech's code mix, not raw intensity — restricted to the 86 speeches with ≥3 codes for stable profiles; k=4 chosen by silhouette, though silhouette scores are modest at ~0.13-0.15, appropriate to report honestly for compositional political-rhetoric data):

- **Cluster 0 — "International sovereigntist" (n=7, mean 4.11 codes/1k, the densest cluster):** dominated by `Rejection_of_Multilateral_Governance` (46% of codes) + `Woke_Bundling` (18%). Concentrated in `cumbre internacional` and US venues. This is the clearest single-cluster expression of climate-obstruction-via-anti-multilateralism.
- **Cluster 1 — "Culture-war / anti-collectivist" (n=27):** `Anti_Casta` (28%) and `Anti_Socialism_Anti_Collectivism` (27%) roughly even, plus `Woke_Bundling` (12%). Domestic-leaning (`evento ideologico/politico`, `foro economico`), lower density (1.03/1k).
- **Cluster 2 — "Anti-institutional / epistemic attack" (n=10):** led by `Attack_on_Universities_and_Research_Institutions` (20%) combined with `Anti_Casta` and `Delegitimization_of_Regulation`. This is the cluster most tied to D1.2 science/expertise attacks specifically.
- **Cluster 3 — "Generic anti-state / deregulation" (n=42, the baseline mode):** `Delegitimization_of_Regulation` (20%) + `Anti_State_Anti_Bureaucratic` (19%) + `Anti_Casta` (16%). Spread across think tanks, business chambers, economic forums — the default rhetorical register for most non-summit domestic speeches.

**Chart:** `07_cluster_pca.png` (PC1+PC2 explain only ~26% of variance — expected for 14-dimensional compositional data; the 2D plot is illustrative, not the full clustering evidence)

## 6. Implications for the paper draft and `final_analysis_report_v4.md`

1. The declining time trend (§2) and the venue concentration in summits (§3-4) together suggest climate-obstruction rhetoric is not diffuse but **event-triggered and forum-specific** — worth a paragraph in the draft distinguishing "ambient" anti-state rhetoric (Cluster 3, the corpus baseline) from the sharper "international sovereigntist" mode (Cluster 0) that appears specifically at multilateral summits.
2. The 42%/58% split in §4 is strong quantitative support for the project's Option A scope decision — cite it directly if the draft needs to defend that methodological choice.
3. The UN General Assembly 2024 speech is the strongest single quantitative candidate for close qualitative reading/excerpting given its outlier density.
4. D1.2 (public science/expertise) remains the weakest dimension quantitatively (11.7% of all codes, only 63 instances) — if the draft argues for a strong "epistemic delegitimization" thesis, this may need qualification, or the paper could note it as a finding in itself (Milei's climate obstruction operates far more through governance/culture-war framing than direct science denial).

## 7. Code composition by venue type and country (added 2026-07-20)

Beyond density (§3), the **mix** of D1.1/D1.2/D1.3 codes shifts systematically by context.

**By venue type:** economic/institutional venues run heavily D1.1 (state/regulation framing) — `cadena nacional` 81%, `cumbre internacional` 80%, `sectorial` 74%, `empresa` 73% — while ceremonial/diplomatic venues invert toward D1.3 (cultural backlash) — `bilateral/diplomatico` 60%, `evento ideologico/politico` 47%, `premio/reconocimiento` 40%. D1.2 (science/expertise attacks) peaks in `foro economico` (20%) and `fundacion/think tank` (16%) — expertise-attack rhetoric is a keynote/thought-leadership register, rarely used in short broadcasts or ceremonial remarks (`cadena nacional` 3%, `bilateral/diplomatico` 0%).

**By country:** Argentina, EE.UU., Brasil, and Suiza (Davos) all run 62-64% D1.1 — anti-state/deregulation is the default register for domestic and major-economic-forum audiences. Paraguay, Israel, and España invert sharply toward D1.3 (56%, 55%, 54%) — these are dominated by diplomatic/ceremonial/religious-context speeches. Suiza stands out for D1.2 share (22%, the highest of any country) — consistent with Davos being the primary stage for direct attacks on "expert"/scientific consensus framing.

**Rhetorical-mode clusters (from §5) track venue and country almost one-to-one:** `cumbre internacional` is 80% "International sovereigntist" cluster (vs. 0% for `empresa`, `cadena nacional`); `empresa` is 100% "Generic anti-state/deregulation" baseline; `evento ideologico/politico` is 58% "Culture-war/anti-collectivist." By country: España is 80% culture-war cluster; Suiza is 67% baseline + 33% anti-institutional/epistemic (again matching its D1.2 concentration); Argentina is majority baseline (59%) with a substantial culture-war minority (25%).

**Takeaway for the draft:** climate-obstruction rhetoric is not a single register — it operates as governance/regulation delegitimization when Milei addresses economic and international elites, and as cultural-backlash/civilizational framing when addressing domestic political or diplomatic audiences. The two registers rarely blend in the same venue type.

**Charts:** `10_dimension_composition.png` (D1.1/D1.2/D1.3 stacked bars by tipo and pais), `08_subcode_composition_by_tipo.png`, `09_subcode_composition_by_pais.png` (full 14-subcode heatmaps)

## Output files

All saved under `analysis/results/v4/quant_analysis/`:
- `corpus_enriched.csv` — full corpus with word counts, rates, climate-signature totals
- `long_format.csv` — one row per code instance
- `tipo_stats.csv`, `pais_stats.csv` — venue/country summary tables
- `clustered_speeches.csv` — cluster assignments for speeches with ≥3 codes
- `dim_by_tipo.csv`, `dim_by_pais.csv` — dimension (D1.1/D1.2/D1.3) composition tables
- `subcode_composition_by_tipo.csv`, `subcode_composition_by_pais.csv` — full 14-subcode composition tables
- `charts/01_time_series.png` through `10_dimension_composition.png`
- This memo (`quant_analysis_memo.md`)
