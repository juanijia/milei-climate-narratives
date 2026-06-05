# Methodology Summary v2: Milei's Climate Narratives

**Date:** June 2026  
**Version:** 2.0  
**Previous version:** `analysis/methodology_summary.md` (v1)

---

## Overview

Phase 3 v2 applies a revised analytical framework to the same corpus coded in v1. The v2 framework is grounded in the research design formalized in `docs/Draft/draft_literaturereview_researchdesign.md`, which integrates three bodies of literature: climate obstruction and discourses of climate delay, policy dismantling theory, and right-wing populism and climate backlash research.

The central theoretical contribution of v2 is to reframe the analysis around a **dual mechanism** of sustainability-policy retrenchment: discursive delegitimization coupled with material capability erosion. This dual mechanism captures how libertarian governance can hollow out sustainability governance without necessarily engaging in outright climate denial — making the analytical framework more precise for the Argentine case.

---

## Why v2? The Shift from v1

The v1 framework (see `analysis/coding_book.md`) organized rhetoric into four pillars: Epistemological Discrediting, Denialism, Cultural Backlash, and a Dual Policy Output tracker. This structure was productive and generated four inductive categories from the corpus (Civilizational_Defense_Frame, Selective_Empiricism, Temporal_Appropriation, Reported_Denial).

However, the v1 framework had three limitations that v2 addresses:

1. **The pillars were theoretically heterogeneous.** Epistemological Discrediting and Denialism both targeted epistemic authority but operated at different levels; Cultural Backlash was largely orthogonal. Grouping them as parallel pillars obscured their different mechanisms of obstruction.

2. **The Dual Policy Output tracker treated institutional change as a residual category** rather than a full analytical dimension. The policy-dismantling literature (Bauer et al. 2012) shows that capability erosion is a mechanism in its own right — not just an "output" of rhetoric but a co-constitutive process that should be tracked with equal analytical weight.

3. **The v1 framework was speech-focused.** The v2 framework explicitly allows for coding passages that reference or justify institutional and budgetary changes, expanding the analytical reach of the corpus beyond purely rhetorical analysis.

---

## The V2 Analytical Framework

The v2 framework is organized around two dimensions:

### Dimension 1 — Discursive Delegitimization (Narrative)

Captures how Milei's discourse delegitimizes the state, sustainability governance, and scientific expertise as the legitimate basis for climate action. Three sub-dimensions:

- **D1.1 — Delegitimization of State Intervention and Sustainability Governance:** Market primacy arguments, anti-state rhetoric, "la casta" framing applied to environmental institutions, rejection of regulation, and opposition to multilateral governance.

- **D1.2 — Delegitimization of Public Science and Expertise:** Attacks on CONICET and public research, criticism of universities, delegitimization of expert authority, climate skepticism, and framing science as ideologically captured.

- **D1.3 — Woke/Cultural Backlash:** Ideological bundling of climate with "wokeism" and neo-Marxism; civilizational defense framing.

The key mechanism in D1 is **contested legitimacy**: Milei does not necessarily need to deny climate change — what matters is whether state institutions are granted the epistemic authority and political legitimacy to act on it.

### Dimension 2 — State Capability Erosion (Material-Institutional)

Captures what Milei says *about* institutional changes that erode the state's practical ability to govern sustainability transitions. Three sub-dimensions:

- **D2.1 — Budgetary Retrenchment:** Budget cuts to scientific institutions, environmental agencies, sustainability programs, and universities.

- **D2.2 — Institutional Downgrading and Administrative Restructuring:** Ministry reorganizations, agency eliminations, regulatory institution changes, and administrative hollowing-out.

- **D2.3 — Sustainability-Policy Dismantling:** Changes in formal climate commitments, withdrawal from international initiatives, instrument changes, deregulation, and reduced enforcement.

The key mechanism in D2 is **implementation gap**: even if formal climate commitments remain in place, eroding the administrative, regulatory, scientific, and fiscal capacities that implement them is a form of effective policy dismantling.

---

## Abductive Approach in V2

The v2 framework remains abductive. The seed categories above are deductive starting points derived from the theoretical literature. The corpus may generate new patterns, particularly given Argentina's distinctive configuration (libertarian-populist rather than productivist-nationalist, as in Brazil). The v1 inductive categories are carried forward as candidate codes with v2 mappings.

New patterns should be added to `analysis/coding_book_v2.md` under Phase 2: Inductive, following the protocol in the discourse-coder-v2 skill.

---

## Key Analytical Questions for Phase 3 v2

1. How does Milei distribute his rhetoric across D1.1, D1.2, and D1.3? Is scientific delegitimization (D1.2) as prominent as state/governance delegitimization (D1.1), or is it subordinate?

2. How much does D2 appear in speech data? When Milei references institutional changes, how does he frame them — as efficiency measures, ideological cleanup, fiscal necessity, or market liberation?

3. What is the relationship between D1 and D2 in specific speeches? Do high-D1 speeches tend to precede or accompany high-D2 moments (budget announcements, restructuring decrees)?

4. Do the v1 inductive categories (particularly Civilizational_Defense and Temporal_Appropriation) map cleanly onto v2 sub-codes, or do they remain analytically distinct? This will inform whether to formalize them as permanent categories.

5. Does the corpus show evolution over time — does the ratio of D1 (rhetoric) to D2 (institutional action references) shift as the government consolidates?

---

## Output Structure

V2 outputs are saved to separate directories to preserve v1 outputs:

| Output | Path |
|--------|------|
| Coded speeches | `analysis/coded_speeches/v2` |
| Frequency tally | `analysis/coded_speeches/v2/frequency_tally_v2.json` |
| Final report | `analysis/results/v2/final_analysis_report_v2.md` |
| This document | `analysis/methodology_summary_v2.md` |

V1 outputs in `analysis/coded_speeches/v1` and `analysis/results` remain untouched.
