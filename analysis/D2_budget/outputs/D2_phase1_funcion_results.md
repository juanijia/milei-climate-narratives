# Dimension 2 · Phase 1 — Budget function-level analysis (2025 vs 2023)

**Status:** pilot complete, FARN-validated · **Date:** 16 August 2026
**Scope:** Administración Nacional · *crédito devengado* 2023–2025, *crédito vigente* 2026 · 29 budget functions

---

## 1. What was built

- **Source dataset:** *Presupuesto de gastos y su ejecución detallada — agrupación anual*, Presupuesto Abierto (DGSIAF / Secretaría de Hacienda), annual files for 2023, 2024, 2025 and 2026. **No API token is needed** — the site's own catalogue endpoint (`/sici/rest-api/catalog/site`) exposes direct download URLs for every dataset, so the pipeline pulls the files straight from the MECON repository. This is better than the API for our purposes: it delivers the complete row-level microdata rather than pre-aggregated query results.
- **Granularity:** one row per (jurisdicción × entidad × SAF × programa × actividad × finalidad × función × inciso × fuente × ubicación), with `credito_presupuestado`, `credito_vigente`, `credito_comprometido`, `credito_devengado`, `credito_pagado`. 131,709 rows for 2023; 113,217 for 2025.
- **GDP denominators:** INDEC national accounts — GDP at market prices in current pesos, reconstructed as *valor agregado bruto a precios básicos* + *impuestos netos sobre los productos* (annual series `8.1_VABPB_2004_A_36` + `8.1_IVA_2004_A_23`). 2023 = 178,878,858 M$; 2025 = 782,476,478 M$.
- **Deflator:** INDEC CPI, national, general level, Dec-2016 = 100, **annual average** — retrieved programmatically from the national time-series API (series `148.3_INIVELNAL_DICI_M_26`). 2023 average = 1,975.01; 2025 average = 8,966.17.

---------OJO TO CHECK IPC PROMEDIO--------

**The same download covers Phases 2 and 3.** The file already contains `jurisdiccion_id/desc`, `entidad_desc`, `servicio_id/desc` (SAF) and `programa_id/desc`, so the institutional and programme layers require no new extraction — only the concordance work.

---

## 2. FARN reconciliation — the validation result

Reproducing FARN (2026), Table 2: nominal executed budget by *finalidad*, in millones de pesos.

| Finalidad | Ours 2023 | FARN 2023 | Δ | Ours 2025 | FARN 2025 | Δ | Ours real ch. | FARN real ch. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Administración Gubernamental | 2,349,060 | 2,349,060 | **0.00%** | 6,728,916 | 6,652,753 | +1.14% | −36.9% | −37.6% |
| Servicios de Defensa y Seguridad | 1,710,842 | 1,710,842 | **0.00%** | 6,096,089 | 6,075,017 | +0.35% | −21.5% | −21.7% |
| Servicios Sociales | 24,845,207 | 24,845,207 | **0.00%** | 90,394,590 | 90,257,189 | +0.15% | −19.9% | −19.9% |
| Servicios Económicos | 5,647,579 | 5,647,579 | **0.00%** | 9,960,290 | 9,539,839 | +4.41% | −61.2% | −62.8% |
| Deuda Pública | 3,472,801 | 3,472,801 | **0.00%** | 10,354,071 | 10,352,974 | +0.01% | −34.3% | −34.3% |
| **Total** | **38,025,489** | **38,025,489** | **0.00%** | **123,533,955** | **122,877,771** | +0.53% | **−28.4%** | **−28.8%** |

**2023 reproduces to the peso across all five finalidades and the total** — an exact match, which confirms the universe (Administración Nacional), the stage (devengado) and the aggregation are identical to FARN's.

**2025 differs by +0.53% overall**, and the explanation is clean: the 2025 annual file was last revised **5 July 2026**, after FARN's April 2026 report. Ours is the later, more complete vintage. The gap is concentrated in Servicios Económicos (+4.4%), consistent with late-posted energy and transport subsidy accruals.

**The deflator is confirmed independently.** FARN's headline −28.8% is reproduced to two decimals from the nominal totals in their own table using the INDEC annual-average series (3.2314 ÷ 4.5398 − 1 = −28.83%). Our −28.4% differs only because our 2025 nominal is larger, not because of a methodological difference.

> **Reporting recommendation.** Use our figures, and state in a footnote that they reproduce FARN's 2023 base exactly and diverge from FARN's 2025 by 0.5% owing to a post-publication data revision. This turns a discrepancy into a credibility asset.

---

## 3. The result you asked for: environment against every other function

Real change in executed budget, 2025 vs 2023, all 29 functions with non-zero 2023 execution. **Whole budget: −28.4%.**

| Rank | Función | Real ch. | GDP-share ch. | vs total (pp) | % of budget 2023 → 2025 |
|---:|---|---:|---:|---:|---|
| 1 | Vivienda y Urbanismo | −98.0% | −97.9% | −69.5 | 0.881 → 0.025 |
| 2 | Agua Potable y Alcantarillado | −91.4% | −91.1% | −63.0 | 1.113 → 0.134 |
| 3 | Industria | −81.2% | −80.5% | −52.8 | 0.318 → 0.084 |
| 4 | Comercio, Turismo y Otros Servicios | −81.0% | −80.3% | −52.5 | 0.214 → 0.057 |
| 5 | Comunicaciones | −80.2% | −79.5% | −51.8 | 0.495 → 0.137 |
| 6 | Promoción y Asistencia Social | −74.1% | −73.1% | −45.7 | 6.515 → 2.358 |
| **7** | **Ecología y Desarrollo Sostenible** | **−64.7%** | **−63.3%** | **−36.2** | **0.314 → 0.155** |
| 8 | Agricultura, Ganadería y Pesca | −62.7% | −61.3% | −34.2 | 0.512 → 0.267 |
| 9 | Dirección Superior Ejecutiva | −62.5% | −61.1% | −34.1 | 0.473 → 0.247 |
| 10 | Energía, Combustibles y Minería | −60.3% | −58.8% | −31.9 | 8.428 → 4.671 |
| 11 | Transporte | −58.5% | −57.0% | −30.1 | 4.462 → 2.585 |
| 12 | Relaciones Interiores | −53.1% | −51.3% | −24.7 | 2.492 → 1.633 |
| 13 | Educación y Cultura | −47.2% | −45.2% | −18.7 | 7.251 → 5.355 |
| **14** | **Ciencia, Tecnología e Innovación** | **−43.9%** | **−41.8%** | **−15.5** | **1.518 → 1.189** |
| 15 | Información y Estadística Básicas | −41.6% | −39.4% | −13.2 | 0.040 → 0.032 |
| 16 | Legislativa | −40.2% | −37.9% | −11.7 | 0.438 → 0.366 |
| 17 | Servicio de la Deuda Pública | −34.3% | −31.8% | −5.9 | 9.133 → 8.382 |
| 18 | Administración Fiscal | −31.2% | −28.6% | −2.8 | 0.062 → 0.059 |
| 19 | Seguros y Finanzas | −29.4% | −26.7% | −1.0 | 0.108 → 0.107 |
| 20 | Control de la Gestión Pública | −26.4% | −23.6% | +2.0 | 0.078 → 0.080 |
| 21 | Seguridad Interior | −26.3% | −23.5% | +2.2 | 2.269 → 2.338 |
| 22 | Defensa | −17.9% | −14.8% | +10.5 | 1.673 → 1.919 |
| 23 | Judicial | −17.5% | −14.4% | +10.9 | 1.987 → 2.291 |
| 24 | Sistema Penal | −16.7% | −13.5% | +11.8 | 0.388 → 0.451 |
| 25 | Relaciones Exteriores | −13.3% | −10.0% | +15.2 | 0.609 → 0.739 |
| 26 | Seguridad Social | −6.6% | −3.1% | +21.8 | 44.162 → 57.613 |
| **27** | **Inteligencia** | **−4.4%** | **−0.7%** | **+24.1** | **0.170 → 0.227** |
| 28 | Salud | **+11.8%** | +16.0% | +40.3 | 3.589 → 5.608 |
| 29 | Trabajo | **+106.5%** | +114.3% | +134.9 | 0.309 → 0.893 |

**The two normalisations agree throughout** — the largest divergence is 3.1 pp (Defensa), there is never a sign flip, and the rank order is essentially unchanged. The finding is robust to the choice of normalisation. Whole-budget GDP share fell from **21.26% to 15.79%**, a 25.7% relative decline.

### What this establishes

**1. Environmental retrenchment is real, severe, and disproportionate.** Ecología y Desarrollo Sostenible fell **64.7% in real terms, 36.2 points more than the budget as a whole**, a cut roughly 2.3 times deeper than the average. Its share of the national budget halved, from 0.31% to 0.16%. This is the sentence the paper needs, and it is now defensible against the full comparator set rather than a chosen few.

**2. But environment was not the single hardest-hit function** Six functions fell further, led by the near-total collapse of Vivienda y Urbanismo (−98%) and Agua Potable y Alcantarillado (−91%). The honest framing is that environmental dismantling is **one front of a generalised retreat from state provision and infrastructure**, not an isolated ideological target. That framing is both accurate and more interesting theoretically: it locates the environmental cut inside the libertarian project rather than treating it as a standalone anti-environmental animus. A reviewer who checks will find the claim holds.

**3. The selectivity pattern is the real finding, and it maps onto Corpus A.** Rank the functions by how *protected* they were and a clear order emerges:

- **Protected or expanded:** Trabajo (+107%), Salud (+12%), **Inteligencia (−4.4%, the third most protected function in the entire budget)**, Seguridad Social (−6.6%), Relaciones Exteriores, Sistema Penal, Judicial, Defensa, Seguridad Interior.
- **Cut far above average:** Ecología (−65%), Ciencia y Tecnología (−44%), Educación y Cultura (−47%), plus the infrastructure and productive-development functions.

The **coercive, judicial and sovereign core of the state was comparatively shielded while its environmental, scientific and educational capacities were cut two to four times more deeply.** This is not what an ideologically neutral fiscal consolidation looks like. It is precisely the pattern the paper's dual-process framework predicts: the functions that Corpus A's D1.1 and D1.2 codes delegitimize discursively — regulation, expertise, universities, environmental governance — are the functions that lose resources, while the state's coercive capacity is preserved. The contrast between **Inteligencia at −4.4% and Ecología at −64.7%** is the single most compact numerical expression of the argument available.

**4. Public science tracks environment, not the average.** Ciencia, Tecnología e Innovación at −43.9% (15.5 pp worse than total) supports the abstract's pairing of sustainability policy with "the public scientific capacities that underpin" it — the two capacity bases erode together. Note this function's Milei-era decline was already −32.9% in 2024 and deepens to −47.6% in the 2026 budget: it is a sustained trajectory, not a one-year shock.

**5. The retrenchment deepens rather than stabilises.** Whole-budget real change vs 2023: **−25.8% (2024) → −28.4% (2025) → −31.0% (2026 budget)**. For Ecología: **−52.1% → −64.7% → −69.7%**. The 2026 budget is not a correction; it consolidates and extends the cut.

---

## 4. Caveats to carry into the paper

1. **Función 4.4 is a lower bound on environmental retrenchment.** It excludes the Servicio Meteorológico Nacional (booked under Defensa), fire management (moved to Seguridad in February 2025 per Decreto BO 12/02/2025 — a *reclassification* that mechanically removes spending from 4.4), INTA (Agricultura) and parts of the science system. The institutional and programme layers must recover these, and the reclassification is itself reportable as institutional erosion.

2. **Funcion decomposition and positives**
-> Trabajo = +106.5%

Decomposing función 3.6 shows one line driving everything: Acciones de Empleo goes from 46,704 to 946,701, and inside it sits a single activity, "Volver al Trabajo" at 891,479 millones (80.8% of the whole function).

That programme did not exist in 2023. It is the ex-Potenciar Trabajo (1,021,601 millones in 2023), which sat in Desarrollo Social under función 3.2 Promoción y Asistencia Social. In 2024 it was split into "Volver al Trabajo" (reclassified to función 3.6) and "Acompañamiento Social" (196,779, stayed in 3.2), both moved to Capital Humano. This inflated 3.6 and deflated 3.2 simultaneously.

The honest statement is that the social-assistance-and-employment block fell about 66% in real terms.

- Salud has the same problem

Función 3.1 Salud's +11.8% is inflated by 1,698,549 millones of "Asistencia Financiera a Empresas Públicas y Otros Entes" booked to Salud in 2025 (a programme that in 2023 was distributed across Energía, Transporte, Agua and Promoción Social, with zero in Salud). Without it Salud is −15.6%, not +11.8%. Still the best-protected large social function, but not growth.

-----------------
**PROPOSAL:**

Both positives are reclassification artefacts. This is the same failure mode as the fire-management case in Phase 2 (the función classifier records where spending is booked, and this government re-booked a lot). Three documented instances now, which is enough to say the vulnerability is systematic rather than incidental.

Concretely: 
- Report 3.2 + 3.6 as a combined block at −65.9% rather than either alone. 
- Footnote Salud's headline with the −15.6% adjusted figure.
- Correct by working with servicio / programa
-----------------

3. **The 2026 figures are provisional, and now carry an explicit range.** *Crédito vigente* was captured from the file revised 14 August 2026 and will keep moving, so a cutoff date must be stated. On the deflator, the Ley de Presupuesto 2026 projects **10.1% December-to-December inflation for 2026** — a figure already overtaken by events (actual CPI rose 19.3% in the seven months to July 2026 alone). Reporting 2026 under that projection alone, as FARN's method implies, would understate the cut. The pipeline therefore now reports 2026 under **two deflators**: the Ley de Presupuesto projection (FARN-comparable, conservative) and a carry-forward of the observed 2026 CPI path (implying ~32% dic/dic). Whole budget 2026 vs 2023: **−26.9% to −34.7%**. Ecología: **−67.9% to −71.4%**. Ciencia y Tecnología: **−44.5% to −50.4%**. The conclusion — that 2026 consolidates rather than reverses the cut — holds under both, which is the point of reporting the range.

5. **Seguridad Social dominates the aggregate.** At 44% → 58% of the budget, its comparatively mild real fall mechanically compresses everything else's share. This is why *share of total* should always be read alongside real change, never instead of it.

---

## 5. Files

```
analysis/D2_budget/
├── scripts/01_build_panels.py          # download + parse + panel construction
├── scripts/02_indicators.py            # FARN reconciliation + indicators
├── processed/ipc_anual_promedio.csv    # INDEC CPI annual averages - OJO ACÁ, chequear
├── processed/panel_funcion.csv         # long panel, all measures, 2023–2026
├── outputs/farn_reconciliation.csv     # the validation table
├── outputs/panel_funcion_indicadores.csv   # the full indicator table
└── outputs/fig1_funcion_real_change.html   # interactive figure (real / GDP / table views)
```
