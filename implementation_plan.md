# Research Project Setup: Narrative Analysis of Milei's Climate Policies

This document outlines the proposed structure and workflow for your research project analyzing Javier Milei's speeches and discourses on climate policies.

## User Review Required

> [!WARNING]
> Please review this project structure and the proposed agent workflows. We will need to decide where to store the project files on your local machine and how to ingest your existing files (Google Doc, PDFs, Spreadsheet).

## Proposed Project Structure

I propose creating the following directory structure inside your `projects` folder to keep the research organized:

```text
milei-climate-narratives/
├── docs/
│   ├── abstract/        # To store the text from your Google Doc
│   ├── methodology/     # For your methodology PDFs
│   └── references/      # For academic references (PDFs)
├── data/
│   ├── sources/         # For the spreadsheet of HTML sources
│   ├── raw_speeches/    # Scraped/downloaded raw speech texts
│   └── processed/       # Cleaned and segmented speeches ready for coding
├── analysis/
│   ├── coding_book.md   # Document defining categories for inductive coding
│   └── results/         # Output of the narrative analysis
└── workflows/           # Agent instructions and defined workflows
    ├── 1_data_collector.md
    ├── 2_methodology_assistant.md
    └── 3_narrative_analyst.md
```

## Agent Team Workflow

To execute this project effectively using AI, we can structure the work into specialized "agent workflows". This means creating specific instruction files that guide the AI on how to handle different phases of the project.

### 1. The Methodologist (Phase 1)
- **Goal:** Understand the proposed methodology and academic references to refine the initial coding strategy.
- **Tasks:**
  - Read and summarize the methodology PDFs.
  - Review the abstract and academic references.
  - Draft the initial `coding_book.md` with the seed categories for inductive coding.

### 2. The Data Collector (Phase 2)
- **Goal:** Gather the raw data (speeches and discourses).
- **Tasks:**
  - Read the spreadsheet containing HTML sources.
  - Use web-browsing capabilities to visit each link, extract the relevant text of Milei's speeches, and save them as markdown or text files in the `data/raw_speeches/` directory.

### 3. The Narrative Analyst (Phase 3)
- **Goal:** Execute the narrative analysis.
- **Tasks:**
  - Process the raw speeches.
  - Apply the inductive coding strategy defined in the `coding_book.md`.
  - Identify emerging narratives, rhetorical strategies, and themes related to climate policies.
  - Produce initial results and summaries in the `analysis/results/` folder.

## Open Questions

> [!IMPORTANT]
> 1. **Project Location:** Should we create this folder structure inside `c:\Users\Juan Ignacio\.antigravity\projects\milei-climate-narratives`?
> 2. **Initial Data Ingestion:** How would you like to provide the existing files (Google Doc, PDFs, Spreadsheet)? You can copy them into the newly created folders once the structure is set up, or provide clear links/paths if they are already on your local machine.
> 3. **Methodology:** Do you have specific initial categories for the inductive coding ready, or should the "Methodologist" agent help derive them from the PDFs first?

## Verification Plan

Once approved, I will:
1. Create the entire directory structure.
2. Create the workflow markdown templates.
3. Provide instructions on where to place your initial files so we can trigger the first agent (The Methodologist).
