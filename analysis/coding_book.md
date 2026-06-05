# Coding Book: Milei's Climate Narratives

This document holds the categories used for analyzing Javier Milei's speeches regarding climate change and climate policies. We employ an **abductive (inductive-deductive) approach**: starting with seed categories provided by the researcher, and subsequently expanding or refining them based on inductive patterns emerging from the data.

## Phase 1: Deductive (Seed Categories)

Based on the conceptual map from the methodology, code all speeches against these core pillars:

### 1. Epistemological Discrediting
- **Knowledge Problem**: Arguments stating that "no planner can aggregate" the complex knowledge needed for climate action.
- **No Market Failures**: Claims that "externalities = state failure", defending absolute free-market mechanisms.
- **Fallacy of Authority**: Arguments like "consensus != knowledge", challenging the scientific consensus on climate change.
- **Government Failure**: Focus on "intervention spirals", arguing state action causes more harm than good.

### 2. Denialism
- **Natural Cycles**: Assertions that current climate changes are part of historical natural cycles rather than anthropogenic.
- **Manipulated Models**: Claims that scientific models have "oversaturated parameters" and are unreliable.

### 3. Cultural Backlash
- **Woke Bundling**: Arguments merging "climate + gender" into a singular progressive enemy.
- **Neo-Marxism**: Framing the entire green agenda as a disguised socialist agenda.
- **Sovereignty Threat**: Labeling the "2030 agenda" as an attempt at world government and loss of national sovereignty.

### Dual Policy Output (Theoretical Framing)
Track if the presence of the above categories leads directly to:
- Discursive Delegitimation of climate institutions.
- State Capability Erosion (e.g., defunding environmental ministries, halting regulations).

## Phase 2: Inductive (Emerging Categories)

### Civilizational_Defense_Frame
**Definition:** A master framing device that positions Western civilization as under existential threat from socialism/collectivism, making every specific policy critique (including climate governance) a front in a civilizational war. Distinct from Neo-Marxism, which labels the ideological content of specific agendas: this category operates at the level of civilizational stakes — not "environmentalism is socialism" but "socialism is destroying civilization, and environmentalism is one of its weapons." Recognize it by the presence of civilizational language ("Occidente está en peligro," "el destino de Occidente") framing policy debates as threats to Western existence.

**Example:** *"hoy estoy acá para decirles que Occidente está en peligro, está en peligro porque aquellos, que supuestamente deben defender los valores de Occidente, se encuentran cooptados por una visión del mundo que – inexorablemente – conduce al socialismo"* (Davos 2024)

**First identified:** 2024-01-17-milei-wef-davos.md

---

### Selective_Empiricism
**Definition:** A rhetorical pattern in which Milei deploys the language of empirical authority ("la evidencia empírica es incuestionable," "la demostración teórica") exclusively for pro-market claims, while simultaneously characterizing opposing academic and institutional knowledge (including climate science) as ideologically captured and therefore invalid. Distinct from Fallacy_of_Authority (which directly challenges consensus) because here the rival empirical claim crowds out rather than refutes the dismissed one — the effect is to appropriate the prestige of empiricism while denying it to opposing knowledge-claims. Recognize it by the co-presence of strong empirical claims for libertarian positions alongside dismissal of expert institutions.

**Example:** *"La evidencia empírica es incuestionable"* (about capitalism's poverty-reduction record), followed by dismissal of "líderes, pensadores y académicos... amparados en un marco teórico equivocado" (Davos 2024).

**First identified:** 2024-01-17-milei-wef-davos.md — *tentative; flag for recurrence in corpus before applying routinely*

---

### Temporal_Appropriation
**Definition:** A rhetorical strategy in which Milei co-opts the normative language of intergenerational responsibility — typically the moral foundation of climate action and sustainability discourse — and redeploys it to argue against state intervention and multilateral climate governance. The pattern involves appropriating future-oriented and sacrifice-of-present framing ("incendian el futuro para mantener caliente el presente") while directing that moral logic *against* the 2030 Agenda, climate bodies, or environmental regulation. Recognize it by the co-presence of: (a) intergenerational or future-harm language, and (b) application of that language to delegitimize international climate/sustainability institutions. Distinct from Discursive_Delegitimation (which attacks institutional credibility directly) and Neo-Marxism (which reframes climate as socialism): Temporal_Appropriation operates at the level of *moral-temporal register* — capturing futurity itself as an anti-regulatory argument.

**Example:** *"incendian el futuro para mantener caliente el presente"* followed by "la Argentina decidió en su momento apartarse de este proceso [la Agenda 2030] porque veíamos en esta agenda un mal gasto de recursos escasos, con fines que no compartíamos y con el efecto de distraer la atención de las dificultades reales" (UN 80th Assembly, 2025-09-24)

**First identified:** 2025-09-24-milei-onu-80-asamblea-general.md

---

### Reported_Denial
**Definition:** An opposing speaker's reported-speech paraphrase of a Milei climate statement, recorded during the coding process as inter-discursive corroboration of a coded primary position. Applied when a political opponent accurately summarizes a Milei climate-related claim in a debate or public forum, providing evidence that the position circulates and is understood as such in public discourse. Distinct from primary discourse coding (it does not code Milei's own words) — function is confirmatory and contextual. Apply with the `INDUCTIVE` prefix and note it is not primary discourse.

**Example:** *"llegó a decir que el cambio climático es del socialismo"* — Bregman's paraphrase of Milei's pre-debate position, during the 2023 Presidential Debate cross-examination round.

**First identified:** 2023-10-08-milei-segundo-debate-presidencial.md

**Note:** Tentative — 1 corpus instance. Retain for completeness; evaluate whether to formalize after additional corpus documents.

---

## Instructions for the Analyst Agent
1. Read the raw/processed speeches from the `data/` folder.
2. Label text segments using the categories above.
3. If a segment contains a new theme or narrative not covered by deductive categories, create a new inductive category in Phase 2.
4. Provide a memo explaining why the segment fits the category.
