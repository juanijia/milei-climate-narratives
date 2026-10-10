# §5.1 — Passage pre-selection and Table 3 audit

**Status:** pre-selection parked for later decision. Nothing here is committed to the manuscript.
**Sources:** `analysis/results/v4/qda_v4_coded_corpus_20260809.xlsx` (`Coded Passages` sheet); raw transcripts in `data/raw_speeches/`.
**Date compiled:** 19 September 2026.

---

## 1. Table 3 audit — current state of the 14 exemplar slots

| # | Sub-code | Current Table 3 exemplar | Verdict |
|---|---|---|---|
| 1 | `Market_Primacy` | *"Market failure is an oxymoron. Market failures do not exist"* — Davos, 17 Jan 2024 | ⚠️ See Problem B |
| 2 | `Anti_State_Anti_Bureaucratic` | Apertura 144°, 1 Mar 2026 | ✅ Verbatim, correctly attributed |
| 3 | `Anti_Casta` | Apertura 142°, 1 Mar 2024 | ✅ Verbatim |
| 4 | `Delegitimization_of_Regulation` | Davos, 21 Jan 2026 | ✅ Verbatim ("dinámicamente ineficientes" confirmed) |
| 5 | `Sustainability_as_Ideological_or_Harmful` | Periglaciares, Corrientes, 13 Nov 2025 | ✅ Verbatim — ⚠️ see Problem C |
| 6 | `Rejection_of_Multilateral_Governance` | Davos, 17 Jan 2024 | ✅ Verbatim |
| 7 | `Attack_on_Universities_and_Research_Institutions` | Apertura 142°, 1 Mar 2024 | ✅ Verbatim |
| 8 | `Attack_on_Experts_and_Technocrats` | UN General Assembly, 24 Sep 2024 | ✅ Verbatim |
| 9 | `Climate_Skepticism_or_Dismissal` | Presidential debate, 8 Oct 2023 | ✅ Verbatim |
| 10 | `Pseudo_Science_or_Ideological_Science` | `elegir` | ⬜ Empty |
| 11 | `Selective_Empiricism` | Five cycles / flat-earthers — Davos, 23 Jan 2025 | ❌ See Problem A |
| 12 | `Woke_Bundling` | Davos, 17 Jan 2024 | ✅ Verbatim |
| 13 | `Anti_Socialism_Anti_Collectivism` | `elegir` | ⬜ Empty |
| 14 | `Civilizational_Defense` | `elegir` | ⬜ Empty |

### Problem A — `Selective_Empiricism` illustrates the wrong code

The "five cycles / flat-earthers" passage is coded `Climate_Skepticism_or_Dismissal` **and** `Pseudo_Science_or_Ideological_Science`. It does not carry `Selective_Empiricism` anywhere in the corpus. `Selective_Empiricism` has exactly three instances (Davos 17 Jan 2024; Tech Forum Argentina 19 Oct 2024; Meta Day Argentina 12 Nov 2024), all pro-market empirical-authority claims.

**Secondary issue:** none of the three denies climate science *in the same passage*, which is what the codebook definition requires ("...while the same epistemic standing is denied to climate science in the same rhetorical move"). Either the exemplar or the definition needs revision. This is a codebook question for the full team, not a writing decision.

### Problem B — `Market_Primacy`, two issues

1. *"el fallo del mercado es un oxímoron. No existe fallo de mercado"* is genuinely in the Davos 2024 transcript (`data/raw_speeches/2024-01-17-milei-wef-davos.md`, line 59) but is **not a coded passage** — the coder selected the adjacent sentence instead. If Table 3 exemplifies coded passages, this does not qualify; if it exemplifies the codebook from the speeches, it is fine. The table should be internally consistent either way.
2. The nearest coded passage is **double-coded** (`Market_Primacy` + `Delegitimization_of_Regulation`), making it a weak definitional exemplar.

### Problem C — periglaciares is wanted in two places

The periglaciares passage is already Table 3's `Sustainability_as_Ideological_or_Harmful` exemplar. Reserving it for §5.2.3 (decision of 19 Sep) means it appears twice. Options: (i) keep in Table 3, paraphrase in §5.2.3; (ii) replace Table 3's exemplar with the UN 2024 "Zero Emission" passage and keep the quote for §5.2.3.

---

## 2. Candidates for the empty and broken slots

### `Pseudo_Science_or_Ideological_Science`
*Definition: the institutional production of climate or environmental knowledge itself, not just specific findings, is framed as epistemically corrupt.*

| ID | Passage (verbatim) | Venue, date | Stacking | Note |
|---|---|---|---|---|
| P1 | *"Sin embargo, cuando uno argumenta que la Tierra ha tenido ya cinco ciclos de cambios bruscos de temperatura y que en cuatro de ellos el hombre ni existía, nos tildan de terraplanistas para desacreditar nuestras ideas, sin importar que la ciencia y los datos estén de nuestro lado."* | Davos, 23 Jan 2025 | + `Climate_Skepticism` | Already carries this code. Clean fix for Problem A: move the quote from row 11 to row 10. |
| P2 | *"El problema esencial de occidente hoy es que no sólo debemos enfrentarnos a quienes siguen bregando por el socialismo empobrecedor; sino también a nuestros propios líderes, pensadores y académicos que, amparados en un marco teórico equivocado, socavan los fundamentos del sistema…"* | Davos, 17 Jan 2024 | Unstacked | Definitionally cleaner, but concerns economists, not environmental knowledge. |
| P3 | *"...por el Club de Roma y por todos los asesinos verdes que andan dando vuelta, neomarxistas que plantean el problema del hombre con la naturaleza…"* | Tech Forum Argentina, 19 Oct 2024 | + `Anti_Socialism` | Most climate-specific; names the Club of Rome. |

### `Selective_Empiricism` — the complete set (only three exist)

| ID | Passage | Venue, date |
|---|---|---|
| S1 | *"La conclusión es obvia: lejos de ser la causa de nuestros problemas, el capitalismo de libre empresa, como sistema económico, es la única herramienta que tenemos para terminar con el hambre, la pobreza y la indigencia, a lo largo y a lo ancho de todo el planeta. La evidencia empírica es incuestionable."* | Davos, 17 Jan 2024 |
| S2 | Whale oil → coal → kerosene substitution narrative as proof of human ingenuity against resource limits | Tech Forum Argentina, 19 Oct 2024 |
| S3 | *"Imagínense que, en 250 años, pasamos de que el 95% de la humanidad pasara hambre a que hoy existe un problema generalizado de obesidad, a nivel mundial."* | Meta Day Argentina, 12 Nov 2024 |

**Recommendation:** S1 — the strongest claim of incontestable empirical authority for the market.

### `Anti_Socialism_Anti_Collectivism`
*Definition: environmentalism framed as disguised socialism or collectivism — a strategic vehicle for state expansion.*

| ID | Passage | Venue, date | Note |
|---|---|---|---|
| A1 | *"Ese comunismo que antes aparecía bajo la bandera soviética hoy se muestra bajo otra apariencia: se oculta detrás de múltiples causas nobles y humanitarias, todas en apariencia independientes, pero íntimamente ligadas por una agenda común de guerra contra la tradición…"* | CPAC Budapest, 21 Mar 2026 | Best definitional fit — **already placed in the by-scope sub-section.** |
| A2 | *"...el Club de Roma y… todos los asesinos verdes que andan dando vuelta, neomarxistas que plantean el problema del hombre con la naturaleza y quieren arreglar el mundo matando inocentes, llámese a los aborteros."* | Tech Forum Argentina, 19 Oct 2024 | Explicitly equates environmentalism with neo-Marxism. Strongest remaining climate-linked option. |
| A3 | *"...es falso que la izquierda sea la ideología de los pobres y los oprimidos… la praxis operativa del socialismo consiste en tener al pobre como cliente de su sistema."* | CPAC Brasil, 7 Jul 2024 | Cleanest definitionally; no environmental referent. |

### `Civilizational_Defense`

| ID | Passage | Venue, date | Note |
|---|---|---|---|
| C1 | *"...the 2030 Agenda, although well-intentioned in its goals, is nothing more than a supranational government program, socialist in nature, which seeks to solve the problems of modernity with solutions that violate the sovereignty of nation states…"* | UN General Assembly, 24 Sep 2024 | Names the sustainability agenda directly. Triple-coded (`Rejection_of_Multilateral` + `SaIH` + `Civilizational_Defense`). Delivered in English. |
| C2 | *"...no hay causa más noble que la causa de Occidente, una línea histórica de la que todos nosotros somos herederos…"* | CPAC investors, Mar-a-Lago, 15 Nov 2024 | Purest civilizational framing; unstacked; no environmental referent. |
| C3 | *"...dejemos de pensar de modo precámbrico. Porque no estamos proponiendo negar los impactos ambientales…"* | Bolsa de Comercio de Córdoba, 16 Mar 2026 | Rare domestic instance, explicitly about environmental impact. Full passage needs extracting before use. |

---

## 3. §5.1 flagship shortlist — body text

Budget agreed: 3–4 quotes, one per sub-dimension. Periglaciares reserved for §5.2.3.

| Slot | Passage | Venue, date | Argumentative function |
|---|---|---|---|
| **D1.1 — axiom** | *"Si las transacciones son voluntarias, el único contexto en el que puede haber un fallo de mercado es si hay coacción. Y el único con la capacidad de coaccionar de manera generalizada es el estado que tiene el monopolio de la violencia. Los fallos de mercado no existen."* | Davos, 17 Jan 2024 | Environmental externalities are the textbook market failure; declaring the category empty forecloses the justification for environmental regulation at first principles, without touching climate science. Repeated near-verbatim at Davos 2025, Davos 2026 and Apertura 144°. |
| **D1.1 — named target** | *"Nor has the tutelage of the World Economic Forum helped, where ridiculous policies are promoted with Malthusian blinders on — such as 'Zero Emission' policies — which harm poor countries in particular. To policies linked to sexual and reproductive rights, when the birth rate in Western countries is plummeting, heralding a bleak future for all."* | UN General Assembly, 24 Sep 2024 | The named attack on net-zero, delivered at the institution that administers it. Delivered in English — no translation needed. Also carries `Woke_Bundling`, so it can serve D1.3 instead. |
| **D1.2** | *"Sin embargo, cuando uno argumenta que la Tierra ha tenido ya cinco ciclos de cambios bruscos de temperatura y que en cuatro de ellos el hombre ni existía, nos tildan de terraplanistas… sin importar que la ciencia y los datos estén de nuestro lado."* | Davos, 23 Jan 2025 | The corpus's only substantive anti-attribution argument, plus the epistemic-authority inversion (consensus as dogma, sceptic as true empiricist) in one move. **Conflicts with P1.** |
| **D1.3** | *"...el Club de Roma y… todos los asesinos verdes que andan dando vuelta, neomarxistas que plantean el problema del hombre con la naturaleza y quieren arreglar el mundo matando inocentes, llámese a los aborteros."* | Tech Forum Argentina, 19 Oct 2024 | Shows the bundling mechanism with a named environmental target, and avoids repeating Table 3's `Woke_Bundling` exemplar and the by-scope Budapest quote. **Conflicts with A2/P3.** |

---

## 4. Passages wanted in two places — decisions pending

| Passage | Competing uses |
|---|---|
| Davos 2025, five cycles / *terraplanistas* | Table 3 `Pseudo_Science` (P1) **vs** §5.1 D1.2 flagship |
| Periglaciares, 13 Nov 2025 | Table 3 `Sustainability_as_Ideological_or_Harmful` **vs** §5.2.3 |
| CPAC Budapest, 21 Mar 2026 | §5.1 by-scope (placed) **vs** Table 3 `Anti_Socialism` (A1) |
| Tech Forum 2024, *asesinos verdes* | Table 3 `Anti_Socialism` (A2) or `Pseudo_Science` (P3) **vs** §5.1 D1.3 flagship |
| UN 2024, "Zero Emission" | §5.1 D1.1 named target **or** D1.3 **or** Table 3 `SaIH` replacement |

---

## 5. Already placed in the manuscript

| Passage | Venue, date | Location |
|---|---|---|
| *Partido del Estado* enumeration | Cena de la Fundación Faro, Buenos Aires, 13 Nov 2024 | §5.1, "By scope" — national register |
| *"causas nobles y humanitarias"* | CPAC Budapest, 21 Mar 2026 | §5.1, "By scope" — international register |
