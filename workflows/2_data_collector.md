---
description: Phase 2 workflow for retrieving raw speeches and texts from URLs.
---
# The Data Collector Agent Workflow

**Goal:** Gather the raw data (speeches and discourses) into the `data/raw_speeches` folder.

## Steps
1. Navigate to `data/sources`.
2. Open the source files (spreadsheets or text files containing URLs).
3. Use the preliminary html sources as reference to conduct an extensive web search to include more discourses, interviews, and references.
4. Extract automated or manual transcripts from any YouTube video links provided in the sources or found during the web search.
5. Use web browsing tools (`read_url_content` or `browser_subagent`) to visit each article/speech URL.
5. Extract the primary text of the speech or article from the HTML.
6. Save each speech as a new Markdown file (`.md`) inside `data/raw_speeches/`. Name them consistently (e.g., `YYYY-MM-DD-speech-title.md`).
7. Remove any boilerplate website text to leave only the content of the speech.
8. Record the status of each download in a `data/raw_speeches/collection_log.md`.
