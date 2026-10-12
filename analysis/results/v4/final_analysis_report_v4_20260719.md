# Final Analysis Report v4: Milei's Climate Narratives
**Version:** 4.0 | **Date:** 2026-07-19 | **Coded by:** Claude (discourse-coder-v4)

---

## Executive Summary

Across the complete corpus of 193 speeches and public discourses delivered by Javier Milei as President of Argentina (8 October 2023 – 29 April 2026), the discursive-delegitimization framework (Dimension 1) identified 538 codeable passages, 61% of which target the legitimacy of state intervention and sustainability governance in the abstract (D1.1) rather than climate science itself (D1.2, 12%) or invoke cultural-backlash framing (D1.3, 27%). This is the corpus's central finding: Milei's climate obstruction is overwhelmingly *institutional and economic-theoretical* rather than scientific-denialist in character — he spends far more rhetorical energy declaring that "market failures do not exist" and that regulatory bodies are captured by a privileged "casta" than he does disputing the physical reality of climate change. Explicit climate-science denial appears in only two speeches across two and a half years (the 2023 presidential debate and Davos 2025's "five cycles" passage); by contrast, the anti-state, anti-casta, and anti-regulatory discursive infrastructure built up over 193 speeches recurs constantly and — per the codebook's Option A scope rule — constitutes the load-bearing apparatus that climate-specific attacks plug into whenever they do appear. The rhetoric evolves across the period: 2023–2024 features occasional direct climate-science skepticism and abstract market-failure theory aimed at international forums; 2025–2026 shifts toward named, concrete targets — an explicit "Agenda Verde" blamed for European demographic collapse, "ambientalistas idiotas extremos" blocking mining output, and, most consequentially, a named forthcoming law to weaken Argentina's glacier-protection buffer zones. That last example (2025-11-13) is the corpus's clearest documented bridge from discourse (D1) to concrete policy action (D2), and should anchor any triangulation with the project's formal-documentation corpus.

---

## Corpus Overview

- **Speeches coded:** 193 (196 physical files; 3 are non-authoritative English-transcript duplicates of an already-coded Spanish original and are excluded from all counts below — see Methodological Notes)
- **Date range:** 2023-10-08 (second presidential debate) – 2026-04-29 (Expo EFI 2026 closing)
- **Speeches with ≥1 D1 code:** 160 of 193 (83%)
- **Genuine zero-code speeches:** 33 of 193 (17%) — predominantly commemorative, foreign-policy/diplomatic, ceremonial, or bilateral small-talk content (Holocaust remembrance, military ceremonies, sports send-offs, condolence/tribute speeches)
- **Total coded passages / code annotations:** 538 (passages can carry multiple stacked codes; 34 pairwise stacked-code instances identified)
- **Active inductive categories:** 0 (none formalized in v4; see "Inductive Categories" below for candidate patterns considered and declined)
- **Venue types:** 23 categories spanning international forums (Davos, UN General Assembly, G20, Mercosur summits), domestic state-of-the-nation addresses (Apertura de Sesiones Ordinarias), cadenas nacionales, business chambers and stock exchanges, universities and think tanks, awards ceremonies, and bilateral meetings
- **Coding dimension:** D1 (Discursive Delegitimization) only, applied to speeches. D2 (State Capability Erosion) is a separate protocol for formal documentation (decrees, budgets, reorganization orders), not yet collected as of this report.
- **Scope rule (v4, "Option A"):** the master corpus database's `clima` heuristic (✔ / ~ / blank) is a *speech-selection* filter only, used to prioritize which speeches to code first — not a passage-level coding filter. Once a speech is selected, general anti-casta, anti-state, anti-regulation, market-primacy, anti-expert, and anti-collectivist rhetoric is coded on its own terms wherever it appears, without requiring an explicit climate/environmental mention in the passage. This is why speeches with no explicit climate content (e.g., education, economic-history, or fiscal-policy speeches) still contribute substantial code counts: per the codebook, this rhetoric constitutes the discursive infrastructure of climate obstruction even when climate itself is never named.

### Methodological Notes

Three pairs of coded files record the same underlying speech event in two languages (an official Spanish original and an AI-generated English transcript from an international host, e.g. the World Economic Forum). Per the corpus's duplicate-transcript protocol, only one file per event counts toward the master CSV and all frequency statistics: the 2024-09-24 UN General Assembly address counts under its English CFR transcript (the more complete source used for the original annotation pass); the 2025-01-23 and 2026-01-21/22 Davos addresses count under their Spanish originals. During this reporting pass, a verification check found that the English-transcript duplicates for the two Davos pairs had retained live, machine-parseable code tags from a pre-reconciliation coding pass despite explanatory notes stating they should not count — this silently double-counted 26 code instances in the frequency tally. This has been corrected: the stray tags were de-formatted to plain text (preserved for provenance, no longer parsed), and the tally, Excel workbook, and HTML explorer were regenerated. All statistics in this report reflect the corrected corpus.

---

## Dimension 1 — Discursive Delegitimization: Key Findings

Aggregate D1 distribution: **D1.1 = 329 codes (61.2%)**, **D1.2 = 63 codes (11.7%)**, **D1.3 = 146 codes (27.1%)**.

### D1.1 — Delegitimization of State Intervention and Sustainability Governance (61.2%)

By a wide margin the dominant sub-dimension, and within it the ranking is telling:

| Sub-code | Count | Share of D1.1 |
|---|---|---|
| Anti_Casta | 99 | 30.1% |
| Anti_State_Anti_Bureaucratic | 84 | 25.5% |
| Delegitimization_of_Regulation | 69 | 21.0% |
| Market_Primacy | 29 | 8.8% |
| Sustainability_as_Ideological_or_Harmful | 24 | 7.3% |
| Rejection_of_Multilateral_Governance | 24 | 7.3% |

`Anti_Casta` and `Anti_State_Anti_Bureaucratic` together account for over half of all D1.1 codes and nearly a third of the entire D1 corpus. This is the discourse's real center of gravity: a generalized, constantly-repeated narrative that state institutions — regardless of which policy domain they administer — are captured by a self-serving political class ("la casta") or are inherently parasitic bureaucratic drag. Climate and environmental agencies are never singled out for special condemnation; they are swept into this pre-existing, much larger anti-institutional frame. `Delegitimization_of_Regulation` (69, 21%) and `Market_Primacy` (29, 9%) supply the theoretical apparatus: the flagship claim, delivered almost verbatim across three consecutive Davos addresses (2024, 2025, 2026) and the 2026 Apertura, is that "market failures do not exist" ("los fallos de mercado no existen" / "el fallo del mercado es un oxímoron") — a claim that, if accepted, eliminates the standard economic justification for *any* environmental regulation (externalities, the paradigm case of market failure in environmental economics) at the level of first principles, without needing to argue about climate science at all.

`Sustainability_as_Ideological_or_Harmful` (24, 7.3%) and `Rejection_of_Multilateral_Governance` (24, 7.3%) are the sub-codes that most directly carry the corpus's *named* climate-obstruction content: the UN's "Zero Emission"/Malthusian critique (2024), the Club of Rome dismissal (2024), the "Agenda Verde"-and-demographic-collapse claim (2026), and the periglaciares/glacier-law passage (2025) all fall here. Though their raw counts are modest relative to Anti_Casta and Anti_State_Anti_Bureaucratic, they are disproportionately consequential: this is where the abstract anti-statist apparatus gets pointed at specific, named environmental institutions, agreements, and — in one case — pending legislation.

### D1.2 — Delegitimization of Public Science and Expertise (11.7%)

The smallest sub-dimension by a wide margin, which is itself a significant finding:

| Sub-code | Count | Share of D1.2 |
|---|---|---|
| Attack_on_Experts_and_Technocrats | 31 | 49.2% |
| Attack_on_Universities_and_Research_Institutions | 14 | 22.2% |
| Pseudo_Science_or_Ideological_Science | 8 | 12.7% |
| Climate_Skepticism_or_Dismissal | 7 | 11.1% |
| Selective_Empiricism | 3 | 4.8% |

Only 7 codes across the entire 2.5-year, 193-speech corpus constitute direct climate-science denial (`Climate_Skepticism_or_Dismissal`), concentrated in just two speeches: the 2023 presidential debate ("vagos socialistas que escriben papers de cuarta" dismissing climate scientists as producing worthless, ideologically-motivated research) and the 2025 Davos "five cycles" passage (the corpus's only substantive empirical argument against anthropogenic attribution). `Attack_on_Experts_and_Technocrats` (31) is nearly the whole rest of D1.2, and it mostly targets economists, not climate scientists — "petardistas tribuneros," "econochantas," professional forecasters who doubted the fiscal-adjustment program. This confirms the report's central thesis: Milei's obstruction pattern is a distinctively *libertarian* one (target the state's authority to regulate, deny that markets can fail) rather than the more familiar populist-right pattern of leading with denial of the underlying science. Where science *is* attacked, universities and "expert" institutions are framed as ideologically captured production sites (`Attack_on_Universities_and_Research_Institutions`, `Pseudo_Science_or_Ideological_Science`) rather than as simply wrong.

### D1.3 — Cultural Backlash (27.1%)

| Sub-code | Count | Share of D1.3 |
|---|---|---|
| Anti_Socialism_Anti_Collectivism | 86 | 58.9% |
| Woke_Bundling | 41 | 28.1% |
| Civilizational_Defense | 19 | 13.0% |

D1.3 functions as a meta-narrative that pre-loads specific arguments with civilizational stakes rather than making an independent case. `Anti_Socialism_Anti_Collectivism` (86) is the corpus's second-most-frequent sub-code overall, appearing constantly across nearly every register — from the theoretical (the post-Marxism thesis explaining how "class struggle" relocated into feminism, gender ideology, and environmentalism after 1989) to the visceral ("el cáncer de la humanidad es el socialismo... satánico"). `Woke_Bundling` (41) is the mechanism by which climate governance gets contaminated by association: at both the 2024 UN address and the 2025 Davos speech, "Zero Emission"/environmentalist policy is placed in the same breath as reproductive-rights policy via a shared Malthusian population-control genealogy, maximizing delegitimization for audiences hostile to either cause independently. `Civilizational_Defense` (19) is comparatively rare but escalates sharply in intensity across the period — from a generic "the West is in danger" framing (Davos 2024) to explicit theological grounding by 2026 (the "golden calf" idolatry framing of the WEF-led governance consensus at Davos 2025; the "¿para qué nos dio el Creador el planeta?" dominion argument at Bolsa de Córdoba 2026).

---

## Inductive Categories

**No inductive categories were formalized in v4** — the tally's `Inductive` section is empty across the full 193-speech corpus. This is itself notable: earlier project phases (v1–v3) had flagged candidates such as `Temporal_Appropriation` (co-opting sustainability's own intergenerational-responsibility vocabulary against sustainability governance) and `Reported_Denial`; both were formally eliminated from the v4 codebook after being found either too rare to warrant a standalone code or better captured by an existing deductive sub-code (see `coding_book_v4.md`'s retired-categories list). No replacement inductive pattern reached the ≥2-corroborated-instance formalization threshold during the v4 pass.

Two candidate patterns were noted in individual coding summaries but **not** promoted, and are recorded here for the methodologist's future reference:

- **Theological/dominion framing** (flagged at 2026-04-20 Bar-Ilan and 2026-03-16 Bolsa de Córdoba): capitalism, resource extraction, and anti-socialism increasingly grounded in explicit Judeo-Christian dominion theology rather than secular libertarian argument by 2026. This may be better understood as an intensification of the existing `Civilizational_Defense` sub-code than a distinct category, but its increasing frequency in the final coded quarter of the corpus is worth monitoring if new 2026 speeches are added.
- **Primitivism-as-regulation metaphor** (flagged at 2025-11-13): regulatory caution of any kind — environmental ("primitivo"), economic ("Picapiedras"/Flintstones), or technological ("tirapiedras cavernícolas" opposing AI) — repeatedly cast as literal prehistoric backwardness relative to Milei's growth agenda. A stylistic recurring motif rather than a distinct delegitimization *target*, and so was left uncoded as a freestanding category, but it cross-cuts D1.1 and D1.2 in a way the current codebook doesn't capture structurally.

---

## Rhetorical Evolution Across the Corpus (2023–2026)

The corpus shows a clear arc from *diffuse, escalating* rhetoric in the discourse's early register toward *concrete, named, policy-adjacent* attacks as Milei's government consolidates — even as raw code density per speech gradually declines.

**Density and composition by year:**

| Year | Speeches coded | D1.1 share | D1.2 share | D1.3 share | Total codes | Avg./speech |
|---|---|---|---|---|---|---|
| 2023 | 5 | 72.2% | 11.1% | 16.7% | 18 | 3.60 |
| 2024 | 88 | 58.9% | 15.2% | 25.9% | 282 | 3.20 |
| 2025 | 71 | 63.3% | 7.4% | 29.3% | 188 | 2.65 |
| 2026 | 29 | 62.0% | 8.0% | 30.0% | 50 | 1.72 |

Average code density per speech declines steadily (3.60 → 1.72) as the corpus expands to include hundreds of short, routine appearances (ribbon-cuttings, factory visits, award acceptances) that a candidate-era or newly-inaugurated president simply didn't have occasion to give. But this decline is a *volume* effect, not a *retreat*: D1.2 (science/expertise attacks) nearly halves as a share of D1 between 2024 and 2025 (15.2% → 7.4%) and never recovers, while D1.3 (cultural backlash) climbs steadily every year (16.7% → 30.0%). Read together with D1.1's consistent ~60-63% dominance, the trend is unambiguous: **explicit anti-science rhetoric recedes while anti-state and civilizational framing intensify** as Milei transitions from insurgent candidate to governing president with a working legislative majority — he has less need to relitigate whether climate science is real and more occasion to use consolidated institutional power to act against specific environmental rules.

**International forums vs. domestic state-of-the-nation addresses:** the corpus's five flagship international-forum speeches (Davos 2024/2025/2026, UN 2024/2025) average roughly 10.8 codes each; the three Apertura de Sesiones Ordinarias addresses (142°/2024, 143°/2025, 144°/2026) average 6.3 each but show a clear escalation — 3 → 7 → 9 codes — as the domestic "apertura" register catches up to the international one over time. International forums remain the primary venue for the corpus's most explicit, named climate-obstruction content (Davos's market-failure theorem, the UN's "Zero Emission" attack, Davos 2025's five-cycles denial); the apertura speeches instead build the domestic ideological infrastructure — anti-casta, anti-bureaucratic, deregulatory frameworks — that is later applied by name to environmental policy in other venues (Bolsa de Córdoba, the periglaciares announcement).

**Milestone speeches, chronologically:**

- **2023 (Debate Presidencial, Oct):** the corpus's only outright, ad hominem climate-science denial — climate scientists as "vagos socialistas que escriben papers de cuarta" — alongside an early `Sustainability_as_Ideological_or_Harmful` framing of climate funding as academic rent-extraction.
- **2024 (Davos, Jan):** the theoretical high-water mark — "el fallo del mercado es un oxímoron," delivered to the audience most invested in climate governance, plus the "casta privilegiada" extension of the anti-elite frame to global institutions (IPCC, UNEP, UNFCCC by implication).
- **2024 (UN General Assembly, Sep):** the corpus's most direct named attack on a specific climate policy — the WEF's "Zero Emission" policies explicitly called "ridiculous" and "Malthusian," bundled in the same passage with reproductive-rights policy.
- **2024 (Apertura 142°, Mar):** no explicit climate content, but the first formal presidential articulation of "la casta" as governing frame — the institutional vocabulary later applied to environmental agencies.
- **2025 (Davos, Jan):** the corpus's only substantive empirical argument against anthropogenic attribution (the "five cycles" claim), paired with the Malthus-abortion-population-control chain and the "golden calf" idolatry framing of the WEF consensus.
- **2025 (Club de la Libertad, Corrientes, Nov):** the periglaciares passage — a concrete, named forthcoming law to devolve glacier-adjacent mining-zone determination to the provinces, framed via dehumanizing rhetoric against "ambientalistas" ("prefieren que uno se muera de hambre") — the clearest D1→D2 bridge in the corpus (see below).
- **2026 (Bolsa de Comercio de Córdoba, Mar):** "ambientalistas idiotas extremos" blamed directly for Argentina's comparatively low mining output versus Chile, escalated with an explicit dominion-theology justification for resource extraction.
- **2026 (Debate "Keynes y la Teoría General", Apr):** the "Agenda Verde" named explicitly (rather than generic "ambientalismo") and blamed, alongside abortion and immigration policy, for Europe's demographic and pension-system collapse.
- **2026 (Davos, Jan) / Apertura 144° (Mar):** the register shifts from empirical/denialist to purely philosophical — Hoppe's property-rights proof and Huerta de Soto's dynamic-efficiency theorem ground the case that "intervention and regulation are... violent and therefore unjust" without any climate-specific content at all, implying the climate-obstruction argument no longer needs restating for an audience that has already absorbed it.

**Key analytical question — is there a trajectory from D1.3 culture-war framing toward D1.1 economic-foundational argument?** The data suggests the opposite of a clean linear handoff: D1.1 never drops below ~59% in any year and D1.3 rises alongside it, not at its expense — the two registers *compound* rather than substitute for each other over time. What does shift cleanly is D1.2's decline, confirming that the "governing register" abandons empirical science-denial arguments in favor of institutional (D1.1) and civilizational (D1.3) ones, which are far harder to falsify and require no engagement with contested data.

---

## Co-occurrence Patterns and Rhetorical Bundles

34 passages carry two or more stacked codes. The most frequent pairings cluster almost entirely around the corpus's explicit climate content, confirming that when Milei does address climate/environmental policy directly, he tends to do so with maximal rhetorical density rather than a single isolated claim:

| Co-occurring pair | Count | What the bundle achieves |
|---|---|---|
| `Rejection_of_Multilateral_Governance` + `Sustainability_as_Ideological_or_Harmful` | 3 | Delegitimizes both the *institution* proposing climate policy and the *policy itself* in one move (UN, WEF) |
| `Sustainability_as_Ideological_or_Harmful` + `Climate_Skepticism_or_Dismissal` | 2 | Pairs "the policy is harmful" with "the underlying science is doubtful" — belt-and-braces delegitimization |
| `Climate_Skepticism_or_Dismissal` + `Woke_Bundling` | 2 | Contaminates climate science denial by association with the broader "woke" cultural target |
| `Sustainability_as_Ideological_or_Harmful` + `Woke_Bundling` | 2 | The climate-is-socialism-in-disguise move — environmentalism reframed as one "head of the same beast" as feminism/gender ideology |
| `Rejection_of_Multilateral_Governance` + `Woke_Bundling` | 2 | Institutions (UN, WEF) framed as vehicles for the broader woke-ideological project, not neutral technical bodies |
| `Rejection_of_Multilateral_Governance` + `Civilizational_Defense` | 2 | Elevates institutional rejection from a policy disagreement to a defense of Western civilization itself |
| `Sustainability_as_Ideological_or_Harmful` + `Civilizational_Defense` | 2 | The dominion-theology justification for resource extraction (Bolsa de Córdoba) |
| `Anti_State_Anti_Bureaucratic` + `Delegitimization_of_Regulation` | 2 | The generic (non-climate) fusion of "bureaucrats are parasites" with "regulation is illegitimate" |

Outside the climate-specific cluster, stacking is comparatively rare — most of the corpus's 538 codes are single, standalone passages. This confirms that dense multi-code "bundling" is a marker Milei reserves for his highest-priority, most consequential arguments rather than routine rhetorical habit.

---

## Key Quotes and Exemplary Passages

**1. "El fallo del mercado es un oxímoron. No existe fallo de mercado."**
*[Market failure is an oxymoron. Market failures do not exist.]* — Davos, 17 January 2024. `D1.1 > Market_Primacy`.
The single most consequential theoretical sentence in the corpus. Environmental externalities are the textbook case of market failure in environmental economics; the entire academic and policy justification for carbon pricing, emissions standards, and pollution regulation rests on the concept. By declaring market failure not merely empirically rare but *logically impossible*, Milei forecloses the theoretical ground for climate regulation at the level of first principles — without engaging climate science at all. Repeated in near-identical form at Davos 2025, Davos 2026, and Apertura 144° (2026), it functions as the corpus's load-bearing axiom.

**2. "Lo que está inspirando toda la agenda asesina de hoy, es el Club de Roma... sugerían impulsar la agenda del aborto."**
*[What's inspiring today's whole murderous agenda is the Club of Rome... they suggested pushing the abortion agenda.]* — Luna Park book presentation, 22 May 2024. `D1.2 > Climate_Skepticism_or_Dismissal`.
Directly names the Club of Rome's 1972 resource-exhaustion predictions — the foundational text of modern environmental-limits discourse — and dismisses them as a discredited, "murderous" agenda traced through Malthus and linked to population control and abortion. Ends with a rare, explicit, pre-emptive self-quotation acknowledging the "science denier" label ("Pero el Señor Milei es un negacionista de la ciencia"), confirming Milei's own awareness that the line of argument reads as climate-science denialism.

**3. "Tampoco ha ayudado el tutelaje del Foro Económico Mundial... como las políticas de 'Emisión Cero' – que dañan, sobre todo, a los países pobres."**
*[Nor has the World Economic Forum's tutelage helped... such as 'Zero Emission' policies – which harm poor countries above all.]* — UN General Assembly, 24 September 2024. `D1.1 > Sustainability_as_Ideological_or_Harmful` + `D1.3 > Woke_Bundling`.
The most direct, named attack on net-zero climate policy delivered at the institution most associated with implementing it, reframing climate skepticism as solidarity with the Global South against "elite climate imperialism" — a geopolitically calibrated argument for an audience of predominantly developing nations.

**4. "La Tierra ha tenido ya cinco ciclos de cambios bruscos de temperatura y... en cuatro de ellos el hombre ni existía... nos tildan de terraplanistas... sin importar que la ciencia y los datos estén de nuestro lado."**
*[The Earth has already had five abrupt temperature-change cycles... in four of them man didn't even exist... they call us flat-earthers... regardless of the fact that the science and the data are on our side.]* — Davos, 23 January 2025. `D1.2 > Climate_Skepticism_or_Dismissal`.
The corpus's only substantive, evidence-framed argument against anthropogenic climate attribution — qualitatively different from the corpus's more common policy-level or institutional dismissals. Deploys an epistemic-authority inversion: the consensus position becomes dogmatic silencing, the skeptic becomes the true empiricist.

**5. "La ley de los periglaciares... permite... devolverles el federalismo a las provincias y que cada provincia determine cuál es la zona periglaciar... los ambientalistas... prefieren que uno se muera de hambre, pero no tocar nada."**
*[The periglacial law... allows returning federalism to the provinces so each one determines its own periglacial zone... environmentalists... would rather people starve than touch anything.]* — 12° Congreso de Economía Regional, Corrientes, 13 November 2025. `D1.1 > Sustainability_as_Ideological_or_Harmful`.
**The single most important passage in the corpus for the D1→D2 research question.** Unlike the corpus's otherwise-abstract ideological attacks on environmentalism, this is an active, named, forthcoming legislative proposal targeting Argentina's existing Glacier Protection Law (Ley de Glaciares 26.639) to expand mining access — the clearest documented case of discursive delegitimization translating into a concrete policy mechanism, and the top-priority item for triangulation with the project's D2 (formal documentation) corpus.

**6. "Estamos abrazados a los ambientalistas idiotas extremos... ¿Para qué nos dio el Creador el planeta? ¿Para contemplarlo?"**
*[We're shackled to extreme idiot environmentalists... Why did the Creator give us the planet? To contemplate it?]* — Bolsa de Comercio de Córdoba, 16 March 2026. `D1.1 > Sustainability_as_Ideological_or_Harmful` + `D1.3 > Civilizational_Defense`.
Directly attributes Argentina's mining underperformance relative to Chile (same mountain range) to environmentalist obstruction, then escalates to explicit dominion theology — resource extraction as divinely sanctioned human purpose — the corpus's clearest fusion of economic and theological argument applied specifically to environmental regulation of extraction.

**7. "Mientras que proponían la Agenda Verde asesinando a los niños inocentes por nacer... promovían el ingreso de extranjeros... Europa al borde del exterminio."**
*[While they proposed the Green Agenda, murdering innocent unborn children... they promoted the entry of foreigners... Europe on the brink of extermination.]* — Debate "Keynes y la Teoría General", 28 April 2026. `D1.1 > Sustainability_as_Ideological_or_Harmful`.
One of the corpus's only instances of "Agenda Verde" named explicitly (rather than generic "ambientalismo"), blamed as one leg of a three-part policy complex — alongside abortion and immigration — for Europe's demographic and pension-system collapse, via a "man against the earth" characterization of ecologism as fundamentally anti-human.

**8. "La intervención y la regulación son dinámicamente ineficientes por ser violentas y, por ende, injustas."**
*[Intervention and regulation are dynamically inefficient because they are violent and therefore unjust.]* — Davos, 21 January 2026. `D1.1 > Delegitimization_of_Regulation`.
The corpus's most philosophically load-bearing regulatory claim, grounded in Hoppe's natural-law property-rights proof rather than empirical or policy argument. Regulation is defined as categorically violent and therefore illegitimate regardless of its content or outcomes — environmental regulation is excluded from legitimate state action *by definition*, without needing to name climate policy at all. Represents the endpoint of the corpus's rhetorical evolution: from empirical denial (2023–2025) to unfalsifiable philosophical axiom (2026).

---

## Notes for Triangulation with Dimension 2 (Corpus B)

D2 (State Capability Erosion) applies to formal documentation — decrees, budget records, reorganization orders — not yet collected as part of this project. Based on the D1 findings above, the following are flagged as priority items for D2 collection and triangulation:

- **Highest priority:** the periglaciares/glacier-law reform referenced at 2025-11-13 (Corrientes). If introduced in Congress, the bill text, any accompanying budget/regulatory-impact documentation, and its legislative status should be collected — this is the corpus's only direct textual link between D1 rhetoric and a specific, named environmental-protection statute.
- **DNU and delegated-powers deregulation packages** (referenced across 2023-12-20, 2025-07-09 "Balance de la Desregulación con Facultades Delegadas," and elsewhere): which specific environmental, mining, or energy regulations were modified or eliminated under the omnibus deregulation authority, and whether any explicitly target climate-adjacent rules (emissions standards, environmental impact assessment requirements, glacier/native-forest protections).
- **Ministry of Environment and Sustainable Development:** budget allocations, staffing levels, and institutional status (downgrade, merger, or elimination) across the 2023–2026 period, to test whether the rhetorical "casta"/"burócrata" framing applied to environmental institutions in speeches (Davos 2024's "casta privilegiada" extended to global climate governance) corresponds to measurable institutional erosion domestically.
- **Mining and hydrocarbons regulatory framework** (RIGI — Régimen de Incentivo para Grandes Inversiones — and related instruments): given the explicit resource-extraction framing at Bolsa de Córdoba (2026) and the periglaciares passage, RIGI's environmental-impact and provincial-authority provisions are a natural D2 counterpart.
- **Multilateral commitment status:** formal documentation of Argentina's stance on the Paris Agreement, 2030 Agenda/SDG reporting, and Pact for the Future implementation, to test whether the UN/Davos rhetorical dissent (2024–2026) translates into withdrawal, non-compliance, or reduced formal engagement.

---

## Conclusions and Next Steps

1. **Milei's climate obstruction is primarily institutional and economic-theoretical, not scientific-denialist.** D1.1 (61.2%) dwarfs D1.2 (11.7%); direct climate-science denial appears in only 2 of 193 speeches. The dominant move is declaring market failure — the conceptual foundation of environmental regulation — logically impossible, and characterizing environmental (and all other) state institutions as captured by "la casta," rather than disputing climate data.

2. **The discursive infrastructure is general-purpose and climate-agnostic, but reliably gets pointed at named environmental targets when the occasion arises.** Per the Option A scope rule, the anti-casta/anti-state/anti-regulation apparatus recurs constantly across all speech types; roughly 20 speeches contain explicit, named climate-or-environment content, and these are disproportionately the corpus's densest, most heavily-stacked passages (Davos, UN, Bolsa de Córdoba, the periglaciares announcement).

3. **The rhetoric evolves from denial toward unfalsifiable philosophical axiom as the government consolidates.** D1.2's share nearly halves between 2024 and 2025 and never recovers; by 2026, the corpus's regulatory arguments (Davos, Apertura 144°) are grounded in Hoppe's and Huerta de Soto's natural-law/property-rights theorems rather than empirical claims — arguments that require no engagement with contested climate data and cannot be falsified by it.

4. **The corpus contains a documented, named bridge from discourse to policy action.** The 13 November 2025 periglaciares passage — a forthcoming law to weaken glacier-adjacent mining restrictions — is the single most important exhibit for this project's central research question and the top priority for D2 triangulation.

**Next steps:**
- Begin D2 (formal documentation) collection per the priority list above, anchored on the periglaciares/glacier-law reform.
- Monitor for the periglaciares bill's introduction and status; if introduced, add its text and any Congressional debate transcripts to the corpus.
- Continue coding new speeches as they are delivered (this report reflects the corpus as of 2026-04-29; Milei's presidency continues).
- Revisit the two candidate inductive patterns (theological/dominion framing; primitivism-as-regulation metaphor) if further speeches reinforce them past the 2-instance threshold — neither currently warrants formalization, but both are worth flagging in the next codebook revision cycle if new v4-coded speeches surface additional instances.
- No currently-active inductive categories require promotion to deductive status at this time.

---

## Output Paths

| File | Path |
|---|---|
| Excel workbook | `analysis/results/v4/qda_v4_coded_corpus_261011.xlsx` |
| HTML explorer | `analysis/results/v4/qda_explorer_v4.html` |
| Quantitative per-speech code-count database | `analysis/results/v4/milei_corpus_v4_code_counts.csv` |
| Final report | `analysis/results/v4/final_analysis_report_v4.md` (this file) |
| Frequency tally (source data) | `analysis/coded_speeches/v4/frequency_tally_v4.json` |
