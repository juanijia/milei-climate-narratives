# Final Analysis Report v4 — Updated (2026-08-09): Milei's Climate Narratives

**Version:** 4.0 (updated pass) | **Date:** 2026-08-09 | **Coded by:** Claude (discourse-coder-v4), under codebook v4 | **Supersedes for reporting purposes (does not replace):** `final_analysis_report_v4.md` (2026-07-19)

**Relationship to the article draft:** This report presents the current state of the Corpus A (presidential speeches) analysis described in Section 4 ("Empirical Research Design") of `docs/Draft/draft_20260809.md`, and is the results base for that article's Findings section. It uses the same terminology and coding scheme defined there (Dimension 1 — Discursive Delegitimization; sub-dimensions D1.1/D1.2/D1.3; the fourteen sub-codes in Table 3 of the draft).

---

## What changed since the 2026-07-19 report

Between 19 July and 8 August 2026, an internal quality audit (`analysis/_draft_v4_excerpt_omission_audit.md`) found that the original coding pass had, in ten speeches, wrongly treated content that repeated arguments from earlier-coded speeches as grounds for leaving a passage uncoded or under-coded — the coding protocol requires each speech to be coded on its own terms regardless of cross-speech repetition (Rule 4 of `skills/discourse-coder-v4/SKILL.md`). All ten speeches were recoded on 2026-08-08. This report reflects the corrected corpus; the numbers below differ from the 19 July report in ways summarized here rather than silently:

- **Total code instances rose from 538 to 613** (+75, +13.9%), entirely from the ten recoded speeches.
- **The corpus's three explicit climate-signature sub-codes** (`Sustainability_as_Ideological_or_Harmful`, `Rejection_of_Multilateral_Governance`, `Climate_Skepticism_or_Dismissal`) **are unaffected — still 55 instances total.** All 75 added codes fall under the generic anti-state/anti-casta/anti-regulation/cultural-backlash sub-codes. This is itself informative: the correction adds density exactly where the "discursive infrastructure" thesis (see below) predicts it should — in generic, not climate-named, rhetoric.
- **Zero-code speeches dropped from 33 (17%) to 23 (12%)** of the corpus.
- **The reported decline in code density across 2023–2026 is substantially revised.** The 19 July report's headline claim — that rhetorical density falls steadily from 3.60 (2023) to 1.72 codes/speech (2026) — turns out to have been partly an artifact of under-coding concentrated in later speeches (nine of the ten corrected speeches are from mid-2025 through April 2026). The corrected trajectory (§ Rhetorical Evolution below) is roughly stable, not declining. This is flagged prominently because the original report built interpretive weight on the declining-density claim; that specific claim should not be reused without this correction.
- One additional physical file exists in `analysis/coded_speeches/v4/` beyond the 193 tracked in the master corpus database — an explicitly marked duplicate-provenance copy of the 2024-09-24 UN General Assembly address (`2024-09-24-milei-debate-general-del-79-periodo-de-sesiones.md`, frontmatter `duplicate_of: 2024-09-24-milei-un-general-assembly.md`), carrying zero live code tags by design. It is excluded from all counts below, consistent with the corpus's duplicate-transcript protocol.

All figures below were recomputed directly from the coded `.md` files using the project's canonical parser (`skills/qda-outputs/scripts/corpus_data.py`), the same code used to regenerate `frequency_tally_v4.json` on 2026-08-08 — not read off any cached spreadsheet.

---

## Executive Summary

Across the complete corpus of 193 speeches and public discourses delivered by Javier Milei as presidential candidate and President of Argentina (8 October 2023 – 29 April 2026), the discursive-delegitimization framework (Dimension 1) identifies 613 codeable passages. As in the prior pass, the corpus's central finding holds and is now more robustly supported: 61.5% of codes target the legitimacy of state intervention and sustainability governance in the abstract (D1.1) rather than climate science itself (D1.2, 10.8%) or invoke cultural-backlash framing (D1.3, 27.7%). Milei's climate obstruction is overwhelmingly institutional and economic-theoretical rather than scientific-denialist: explicit climate-science denial (`Climate_Skepticism_or_Dismissal`) still appears in only two speeches across two and a half years, while the anti-state, anti-"casta", and anti-regulatory discursive infrastructure — now confirmed even more dominant after correction (`Anti_Casta`, 116 instances, is the single most frequent sub-code in the corpus) — recurs constantly and constitutes the load-bearing apparatus that climate-specific attacks plug into whenever they do appear. The corpus's three explicit climate-signature sub-codes (55 instances total) split almost evenly between speeches pre-flagged as high climate-relevance (42%) and speeches that were not (58%) — direct quantitative support for the project's "Option A" scope decision to code this rhetoric wherever it appears rather than only in pre-selected climate speeches. The single densest speech in the corpus, once corrected, is the 14 March 2026 Madrid Economic Forum address (21 codes) — a speech containing zero explicit climate content, illustrating precisely how the generic discursive infrastructure and the climate-specific attacks operate as separable registers.

---

## Corpus Overview

- **Speech events analyzed:** 193 (matching the master corpus database; all rows `coded = ok`)
- **Physical coded files:** 194 (one duplicate-provenance file excluded from counts — see above)
- **Date range:** 2023-10-08 (second presidential debate) – 2026-04-29 (Expo EFI 2026 closing)
- **Speeches with ≥1 D1 code:** 170 of 193 (88%)
- **Genuine zero-code speeches:** 23 of 193 (12%) — concentrated in `acto institucional` (5), `acto conmemorativo` (5), `bilateral/diplomatico` (4), and `cumbre internacional` (3): predominantly ceremonial, commemorative, or diplomatic content with no delegitimization move of any kind
- **Total coded passages / code annotations:** 613 (mean 3.18/speech)
- **Passages carrying two or more stacked codes:** 36
- **Active/formalized inductive categories:** 0
- **Coding dimension:** D1 (Discursive Delegitimization) only, applied to speeches (Corpus A). D2 (State Capability Erosion / Corpus B) is a separate, not-yet-collected protocol — see Section 4.1.2 of the article draft.

**Table 1. Corpus and coding results at a glance**

| Metric | 2026-07-19 report | 2026-08-09 (this report) |
| ----- | ----- | ----- |
| Speech events | 193 | 193 |
| Speeches with ≥1 code | 160 (83%) | 170 (88%) |
| Zero-code speeches | 33 (17%) | 23 (12%) |
| Total code instances | 538 | 613 |
| Stacked-code passages | 34 | 36 |
| D1.1 share | 61.2% (329) | 61.5% (377) |
| D1.2 share | 11.7% (63) | 10.8% (66) |
| D1.3 share | 27.1% (146) | 27.7% (170) |
| Climate-signature codes | 55 | 55 (unchanged) |

---

## Dimension 1 — Discursive Delegitimization: Key Findings

**Table 2. Sub-code frequencies, ranked**

| Rank | Sub-code | Sub-dimension | Count | Share of D1 |
| ----- | ----- | ----- | ----- | ----- |
| 1 | Anti_Casta | D1.1 | 116 | 18.9% |
| 2 | Anti_Socialism_Anti_Collectivism | D1.3 | 102 | 16.6% |
| 3 | Anti_State_Anti_Bureaucratic | D1.1 | 93 | 15.2% |
| 4 | Delegitimization_of_Regulation | D1.1 | 85 | 13.9% |
| 5 | Woke_Bundling | D1.3 | 41 | 6.7% |
| 6 | Market_Primacy | D1.1 | 35 | 5.7% |
| 7 | Attack_on_Experts_and_Technocrats | D1.2 | 32 | 5.2% |
| 8 | Civilizational_Defense | D1.3 | 27 | 4.4% |
| 9 | Sustainability_as_Ideological_or_Harmful | D1.1 | 24 | 3.9% |
| 9 | Rejection_of_Multilateral_Governance | D1.1 | 24 | 3.9% |
| 11 | Attack_on_Universities_and_Research_Institutions | D1.2 | 14 | 2.3% |
| 12 | Pseudo_Science_or_Ideological_Science | D1.2 | 10 | 1.6% |
| 13 | Climate_Skepticism_or_Dismissal | D1.2 | 7 | 1.1% |
| 14 | Selective_Empiricism | D1.2 | 3 | 0.5% |

### D1.1 — Delegitimization of State Intervention and Sustainability Governance (61.5%, 377 codes)

The dominant sub-dimension by a wide margin, and now even more so than in the July pass. `Anti_Casta` (116) is, after correction, the single most frequent sub-code in the entire corpus — ahead of `Anti_Socialism_Anti_Collectivism` (102). Together with `Anti_State_Anti_Bureaucratic` (93) and `Delegitimization_of_Regulation` (85), these three generic sub-codes account for 294 of 613 codes (48.0% of the whole corpus). Climate and environmental institutions are never singled out for special condemnation in this register; they are swept into a pre-existing, much larger anti-institutional frame that recurs in nearly every speech genre. `Delegitimization_of_Regulation`'s flagship claim — that "market failures do not exist" ("los fallos de mercado... no existen") — recurs verbatim or near-verbatim across at least five speeches in the corpus (Davos 2024, 2025, 2026; Apertura 144°, 2026; Madrid Economic Forum, 2026), each time eliminating the standard economic justification for environmental regulation (externalities) at the level of first principles, without engaging climate science.

`Sustainability_as_Ideological_or_Harmful` (24) and `Rejection_of_Multilateral_Governance` (24) remain the sub-codes carrying the corpus's *named* climate-obstruction content — the UN's "Zero Emission" critique, the Club of Rome dismissal, the "Agenda Verde"/demographic-collapse claim, and the periglaciares/glacier-law passage. Their absolute counts are unchanged by the correction, confirming these are genuinely rare, high-salience passages rather than an artifact of under-coding elsewhere.

### D1.2 — Delegitimization of Public Science and Expertise (10.8%, 66 codes)

Still the smallest sub-dimension, and proportionally slightly smaller after correction (10.8% vs. 11.7% in July) — the ten recoded speeches added almost no D1.2 content, reinforcing that science/expertise attacks are concentrated in a specific register (keynote/thought-leadership addresses) rather than distributed evenly across the corpus. Only 7 codes across 193 speeches constitute direct climate-science denial (`Climate_Skepticism_or_Dismissal`), still confined to the 2023 presidential debate and the 2025 Davos "five cycles" passage. `Attack_on_Experts_and_Technocrats` (32) remains the largest D1.2 sub-code and mostly targets economists and forecasters, not climate scientists specifically.

### D1.3 — Cultural Backlash (27.7%, 170 codes)

The corrected pass strengthens D1.3's already-substantial share (27.1% → 27.7%). `Anti_Socialism_Anti_Collectivism` (102) is now the corpus's second most frequent sub-code overall (up from 86), appearing across nearly every register. `Woke_Bundling` (41) is the mechanism by which climate governance gets contaminated by association with reproductive-rights and gender-ideology framing. `Civilizational_Defense` (27, up from 19) shows the largest proportional increase of any D1.3 sub-code after correction, reflecting the recoded speeches' concentration in late-2025/2026 addresses, where the theological and civilizational register intensifies (see Rhetorical Evolution below).

---

## Rhetorical Evolution Across the Corpus (2023–2026)

**Table 3. Density and composition by year (corrected)**

| Year | Speeches | D1.1 | D1.2 | D1.3 | Total codes | Avg./speech | D1.1 share | D1.2 share | D1.3 share |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 2023 | 5 | 13 | 2 | 3 | 18 | 3.60 | 72.2% | 11.1% | 16.7% |
| 2024 | 88 | 170 | 43 | 79 | 292 | 3.32 | 58.2% | 14.7% | 27.1% |
| 2025 | 71 | 135 | 16 | 56 | 207 | 2.92 | 65.2% | 7.7% | 27.1% |
| 2026 | 29 | 59 | 5 | 32 | 96 | 3.31 | 61.5% | 5.2% | 33.3% |

Two findings survive the correction essentially intact, and one is substantially revised:

**Revised: raw code density does not decline steadily across the presidency.** The prior report's claim of a steady fall from 3.60 to 1.72 codes/speech is not supported once the ten under-coded speeches are corrected — density is better described as roughly stable, oscillating between 2.92 and 3.60 across all four years, with 2026 (through 29 April, a partial year) essentially matching 2024. Nine of the ten corrected speeches fall in mid-2025 through April 2026, which is exactly the period the original report characterized as declining; the "decline" was, in substantial part, an artifact of the omission bug rather than a genuine feature of Milei's rhetoric.

**Confirmed: D1.2 (science/expertise attacks) recedes as a *share* of the discourse even though raw density does not decline.** D1.2's share of D1 falls from a 2024 peak of 14.7% to 7.7% (2025) and 5.2% (2026) — a clear and, after correction, still-robust downward trend. Milei increasingly grounds his regulatory and anti-collectivist arguments in property-rights philosophy (Hoppe, Huerta de Soto) rather than empirical or scientific claims, a shift that requires no engagement with contested data and cannot be falsified by it.

**Confirmed: D1.3 (cultural backlash) climbs steadily across the period** — 16.7% (2023) → 27.1% (2024) → 27.1% (2025) → 33.3% (2026) — while D1.1 remains dominant throughout (58–72% every year, never dropping below three-fifths of the corpus). Read together, the corrected data support a more precise version of the original claim: it is not that anti-state/civilizational framing "intensifies while density falls," but that **the composition of a roughly stable volume of rhetoric shifts away from empirical/scientific register (D1.2) and toward civilizational register (D1.3), while the anti-statist/institutional core (D1.1) remains the constant, dominant baseline.**

**New milestone speeches surfaced by the correction:**

- **14 March 2026, Madrid Economic Forum** — now the single densest speech in the corpus (21 codes), overtaking Davos 2024 (19 codes). Notably, it contains **zero** climate-specific content: its codes are entirely `Anti_Casta` (named-businessman rent-seeking attacks — Grupo FATE/Madanes Quintanilla, Paolo Rocca/Techint), `Anti_State_Anti_Bureaucratic`, `Delegitimization_of_Regulation` (including a fresh instance of "los fallos de mercado... no existen"), `Anti_Socialism_Anti_Collectivism`, and `Civilizational_Defense`. This is the corpus's clearest single-speech illustration of the generic discursive infrastructure operating at full intensity independent of any climate content.
- **29 April 2026, Expo EFI closing** — 17 codes (previously near-zero), now the corpus's third-densest speech, delivered on the corpus's final recorded date.
- **15 November 2024, CPAC Investors Mar-a-Lago** and **10 March 2026, Gala Algemeiner** — both recoded from near-zero to double-digit or high-single-digit code counts, both concentrated in `Anti_Casta`/`Civilizational_Defense` register.

The corpus's previously identified milestone speeches — the 2023 debate, Davos 2024/2025/2026, the UN General Assembly addresses (2024, 2025), Apertura 142°/143°/144°, the Club de la Libertad periglaciares passage (13 Nov. 2025), and Bolsa de Córdoba (16 Mar. 2026) — are unaffected by the correction (none were among the ten recoded files) and their code counts and quoted passages remain as reported on 19 July.

---

## Discursive Patterns by Venue and Audience

**Table 4. Code density and composition by event type (top 10 by total codes)**

| Event type (`tipo`) | n | Total codes | Avg./speech | D1.1 share | D1.2 share | D1.3 share |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| Foro económico | 21 | 115 | 5.48 | 58% | 14% | 28% |
| Evento ideológico/político | 21 | 89 | 4.24 | 43% | 9% | 48% |
| Acto institucional | 26 | 59 | 2.27 | 66% | 10% | 24% |
| Fundación / think tank | 13 | 49 | 3.77 | 55% | 16% | 29% |
| Cumbre internacional | 12 | 40 | 3.33 | 80% | 5% | 15% |
| Bolsa / cámara de comercio | 12 | 33 | 2.75 | 64% | 12% | 24% |
| Cadena nacional | 10 | 31 | 3.10 | 81% | 3% | 16% |
| Empresa | 10 | 30 | 3.00 | 73% | 17% | 10% |
| Premio / reconocimiento | 14 | 28 | 2.00 | 46% | 14% | 39% |
| Sectorial | 7 | 23 | 3.29 | 74% | 9% | 17% |

Economic and institutional venues run heavily D1.1 (`cadena nacional` 81%, `cumbre internacional` 80%, `sectorial` 74%, `empresa` 73%) — regulation, market-primacy, and anti-bureaucratic framing is the default register when Milei addresses economic or governing audiences. Ideological/political events and awards ceremonies invert toward D1.3 (48% and 40% respectively), consistent with the corpus-wide finding that cultural-backlash framing is the register reserved for identity-aligned or ceremonial audiences rather than technical/economic ones. `Foro económico` (Davos-style keynotes) is both the single highest-volume category (115 codes) and reasonably balanced across all three sub-dimensions, consistent with these being the corpus's longest, most argumentatively complete set-piece speeches.

**Table 5. Code density by country (n ≥ 3 speeches)**

| País | n | Total codes | Avg./speech |
| ----- | ----- | ----- | ----- |
| Suiza (Davos) | 5 | 32 | 6.40 |
| España | 8 | 45 | 5.62 |
| EE.UU. | 21 | 92 | 4.38 |
| Brasil | 4 | 16 | 4.00 |
| Argentina | 129 | 382 | 2.96 |
| Uruguay | 3 | 6 | 2.00 |
| Israel | 10 | 19 | 1.90 |
| Paraguay | 5 | 9 | 1.80 |

Foreign venues — especially Switzerland (Davos) and Spain — carry substantially higher average code density than domestic Argentine speeches (2.96/speech), even though Argentina accounts for two-thirds of all speech events and the largest absolute code volume (382 of 613, 62.3%). This is consistent with the venue-type finding above: Milei's highest-density rhetoric is concentrated in international economic/ideological set-piece events (Davos, Madrid, CPAC-adjacent galas) rather than routine domestic appearances.

---

## Co-occurrence and Rhetorical Bundles

36 passages (5.9% of all coded passages) carry two or more stacked codes under the codebook's overcoding rule — applied only when a second code captures a genuinely distinct rhetorical move. The most frequent pairings:

**Table 6. Most frequent stacked-code pairs**

| Co-occurring pair | Count | What the bundle achieves |
| ----- | ----- | ----- |
| `Anti_State_Anti_Bureaucratic` + `Delegitimization_of_Regulation` | 3 | The generic (non-climate) fusion of "bureaucrats are parasites" with "regulation is illegitimate" |
| `Rejection_of_Multilateral_Governance` + `Woke_Bundling` | 3 | Institutions (UN, WEF) framed as vehicles for the broader "woke" ideological project |
| `Rejection_of_Multilateral_Governance` + `Sustainability_as_Ideological_or_Harmful` | 3 | Delegitimizes both the institution proposing climate policy and the policy itself in one move |
| `Sustainability_as_Ideological_or_Harmful` + `Climate_Skepticism_or_Dismissal` | 2 | Pairs "the policy is harmful" with "the underlying science is doubtful" |
| `Climate_Skepticism_or_Dismissal` + `Woke_Bundling` | 2 | Contaminates climate-science denial by association with the broader "woke" cultural target |
| `Anti_Casta` + `Anti_State_Anti_Bureaucratic` | 2 | The generic elite-capture and organizational-form critiques applied together |
| `Sustainability_as_Ideological_or_Harmful` + `Woke_Bundling` | 2 | The climate-is-socialism-in-disguise move |
| `Rejection_of_Multilateral_Governance` + `Civilizational_Defense` | 2 | Elevates institutional rejection to a defense of Western civilization itself |
| `Sustainability_as_Ideological_or_Harmful` + `Civilizational_Defense` | 2 | The dominion-theology justification for resource extraction (Bolsa de Córdoba) |
| `Delegitimization_of_Regulation` + `Rejection_of_Multilateral_Governance` | 2 | Ties deregulation arguments directly to rejection of the international bodies proposing regulation |

As in the July pass, dense multi-code bundling remains concentrated around the corpus's explicit climate-adjacent content — most of the corpus's 613 codes are single, standalone passages, confirming that stacking is a marker Milei reserves for his highest-priority arguments rather than a routine habit.

---

## Testing the "Discursive Infrastructure" Thesis

The article's Section 4.2 scope rule ("Option A") holds that generalized anti-state, anti-regulatory, and anti-"casta" rhetoric should be coded wherever it appears, not only when explicitly climate-adjacent, because it constitutes the discursive infrastructure that climate-specific attacks later plug into. This is directly testable using the three sub-codes that most explicitly carry climate content (`Sustainability_as_Ideological_or_Harmful`, `Rejection_of_Multilateral_Governance`, `Climate_Skepticism_or_Dismissal`): of 55 total climate-signature instances, only 23 (42%) occur in speeches the master database flags as high climate-relevance (`clima = ✔`); the remaining 32 (58%) occur in speeches flagged only "possible" (`~`, 26 instances) or unflagged (blank, 6 instances). Because the correction added zero new climate-signature codes, this 42%/58% split is unchanged from the July report and is now confirmed robust to the recap-audit correction — direct quantitative support for coding this rhetoric wherever it appears rather than gating on an explicit climate mention per passage.

---

## Key Quotes and Exemplary Passages

The eight flagship passages identified in the 19 July report are unaffected by the correction and remain the corpus's clearest illustrations (full text and analysis in `final_analysis_report_v4.md`): the "el fallo del mercado es un oxímoron" claim (Davos 2024); the Club of Rome/Malthus passage (Luna Park, 2024); the WEF "Zero Emission" attack (UN General Assembly, 2024); the "five cycles" climate-science denial (Davos 2025); the periglaciares/glacier-law passage (Corrientes, 2025) — still the corpus's single most important D1→D2 bridge; the "ambientalistas idiotas extremos" dominion-theology passage (Bolsa de Córdoba, 2026); the "Agenda Verde" passage (Debate "Keynes y la Teoría General," 2026); and the Hoppe natural-law regulation claim (Davos 2026).

Two new passages, surfaced by the correction, are added here:

**9. "Los fallos de mercado... desde mi punto de vista, no existen."**
*[Market failures... from my point of view, do not exist.]* — Madrid Economic Forum, 14 March 2026. `D1.1 > Delegitimization_of_Regulation`.
A fourth near-verbatim restatement of the corpus's load-bearing market-failure-denial axiom (after Davos 2024, 2025, and 2026), confirming this is Milei's single most repeated theoretical claim across venues and years. Immediately followed in the same speech by an explicit `D1.2 > Pseudo_Science_or_Ideological_Science` move attacking neoclassical welfare economics itself as "una estructura matemática" mistaken for reality — the clearest corpus instance of the market-failure denial and the epistemic attack on economic (not climate) science appearing back-to-back in the same argumentative unit.

**10. The Madrid Economic Forum address as a whole (14 March 2026, 21 codes, zero climate content).**
Not a single quotable line but a structural finding: the corpus's single densest speech contains no explicit climate or environmental content at all — its density comes entirely from named-businessman `Anti_Casta` attacks (Grupo FATE/Madanes Quintanilla; Paolo Rocca/Techint), generic anti-state and deregulation argument, anti-collectivist historical illustration (Berlin Wall, North/South Korea, Cuba), and civilizational framing. It is the corpus's cleanest empirical illustration of the discursive-infrastructure thesis: the generic apparatus operates at full intensity independent of any climate-specific trigger.

---

## Inductive Categories

**No inductive categories are formalized in this pass** — the tally's `Inductive` section remains empty across the full corrected corpus. This is unchanged from the July report. The two previously noted candidate patterns (theological/dominion framing; primitivism-as-regulation metaphor) were not systematically re-examined against the ten recoded speeches in this pass; a full inductive-category review against the corrected corpus is recommended before the next codebook revision, since several of the recoded speeches (2026-03-10 Gala Algemeiner, 2026-03-14 Madrid Economic Forum) fall within the period where the theological/civilizational register was intensifying.

---

## Notes for Triangulation with Dimension 2 (Corpus B)

Unchanged from the 19 July report — D2 (State Capability Erosion) has not yet been collected. The periglaciares/glacier-law reform (13 November 2025) remains the highest-priority item, unaffected by this correction. See Section 4.1.2 of `docs/Draft/draft_20260809.md` for the current Corpus B collection plan.

---

## Conclusions and Next Steps

1. **The corpus's central finding is confirmed and strengthened by correction, not weakened.** D1.1 (61.5%) still dwarfs D1.2 (10.8%); direct climate-science denial appears in only 2 of 193 speeches. `Anti_Casta` is now, after correction, the single most frequent code in the corpus (116 instances) — the strongest possible confirmation that Milei's climate obstruction operates primarily through a generic anti-institutional, anti-elite frame rather than through disputing climate data.

2. **The declining-density claim from the July report should not be reused without correction.** The corrected data show density that is roughly stable (2.92–3.60 codes/speech) across 2023–2026, not steadily declining. The compositional shift — D1.2 receding, D1.3 rising, D1.1 constant — is confirmed and is the more precise and defensible version of the evolution finding.

3. **The "discursive infrastructure" thesis is now more directly evidenced**, both by the 42%/58% climate-signature split (unchanged, robust to correction) and by the new Madrid Economic Forum exhibit — the corpus's single densest speech, with zero explicit climate content.

4. **Quality-control practices matter and are documented.** This correction — like the text-truncation fix reported on 2026-08-06 — is disclosed here rather than silently absorbed into a "final" number, consistent with the audit-trail approach to confirmability described in Section 4.2 of the article draft. Any citation of corpus-wide statistics in the manuscript should cite this report (or a later one) rather than the 19 July version.

**Next steps:**
- Update the article draft's any in-text citations of corpus statistics (e.g., Section 4.4's Table 5) to the figures in this report before submission.
- Begin D2 (Corpus B) collection per the priority list above.
- Consider a full re-run of the quantitative pipeline (`analysis/results/v4/quant_analysis/`) — word-count-normalized density, co-occurrence phi-coefficients, and rhetorical-mode clustering — against the corrected 194-file corpus; the existing quant-analysis outputs there predate this correction (dated 2026-07-20) and should be treated as directional only until refreshed.
- Continue coding newly delivered speeches as they occur; re-run `update_frequency_tally.py` and regenerate this report after each batch.

---

## Output Paths

| File | Path |
| ----- | ----- |
| This report | `analysis/results/v4/final_analysis_report_v4_20260809.md` |
| Prior report (2026-07-19, superseded for reporting, not deleted) | `analysis/results/v4/final_analysis_report_v4.md` |
| Frequency tally (source data, current) | `analysis/coded_speeches/v4/frequency_tally_v4.json` |
| Recap-audit documentation | `analysis/_draft_v4_excerpt_omission_audit.md` |
| Article draft (Section 4 defines the methodology this report reports on) | `docs/Draft/draft_20260809.md` |
