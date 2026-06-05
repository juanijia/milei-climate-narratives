---
name: speech-collector
description: >
  Scrapes political speeches, interviews, and news articles from URLs and saves them as
  structured Markdown files ready for qualitative coding. Use this skill whenever you are:
  collecting speech texts from websites, scraping article or interview content for a research
  corpus, building a collection of political discourse from multiple URLs, extracting text from
  news or government sites, processing a list of source URLs into clean markdown files, or
  visiting URLs from a spreadsheet to build a text dataset. Also use whenever the user says
  things like "collect speeches", "scrape articles", "build the corpus", "gather the source
  texts", or "process the URLs from Notes.xlsx". This skill ensures consistent frontmatter,
  reliable boilerplate-stripping, correct file naming, and automatic logging.
---

# Speech Collector

You are collecting political discourse texts from web sources and saving them as clean,
consistently formatted Markdown files for qualitative research coding.

## Before You Start

1. Check `data/sources/Notes.xlsx` for the primary URL list — use the `xlsx` skill to read it.
   This file contains URLs and metadata (titles, dates, source types) that you'll use to
   populate frontmatter.
2. If working from a list of URLs provided directly, use those as your starting point.
3. You may also conduct additional web searches to find climate-related speeches or interviews
   not already in the source list.

## How to Collect Each Item

For each URL:

1. **Fetch the page** using web browsing tools (`WebFetch` or browser tools).
2. **Extract primary content only** — strip everything that isn't the speech or article itself.
   See the Boilerplate Removal section below.
3. **Save the file** with the correct naming convention and frontmatter template.
4. **Log the result** in `data/raw_speeches/collection_log.md`.

## File Naming Convention

```
data/raw_speeches/YYYY-MM-DD-keyword-slug.md
```

- Use the date the speech was given (or article published), not today's date.
- The slug should be 2–5 lowercase hyphenated words describing the content.
- Examples:
  - `2024-09-23-milei-un-general-assembly.md`
  - `2023-12-10-milei-davos-interview.md`
  - `2022-06-15-milei-climate-change-entrevista.md`

## Frontmatter Template

Every file must begin with this YAML frontmatter block:

```markdown
---
title: "[Speech or article title]"
date: YYYY-MM-DD
source_url: "https://..."
source_type: speech | interview | tweet_thread | article | youtube
language: es
youtube_transcript: true | false
summary_en: "[Brief 1–2 sentence English summary of the content]"
---
```

- `source_type`: Choose the most accurate option. Use `youtube` only for videos handled by
  the youtube-transcript skill.
- `youtube_transcript`: Set `true` only if the content comes from a YouTube transcript.
  For all other source types, set `false`.
- `summary_en`: Write in English even though the body is in Spanish. This helps researchers
  quickly scan the corpus without reading Spanish. Keep it factual: what topic, what position,
  what occasion.

## Boilerplate Removal Rules

**Strip these elements** — they add noise and confuse coding:
- Navigation menus, headers, footers
- Cookie banners and consent notices
- Social media share buttons and "follow us" prompts
- Related articles / "you might also like" sections
- Advertisement text
- Site-wide sidebars and widget content
- Author bios not directly relevant to the speech

**Keep these elements:**
- All text directly attributed to Milei (spoken or written)
- In Q&A / interview formats: interviewer questions, labeled as `[INTERVIEWER:]`
- Journalist descriptions of delivery, setting, or context — especially useful for
  discourse analysis (e.g., "applause", "shouting from the crowd", "reading from notes")
- Quoted reactions from other political figures if they appear in direct response to Milei

**Language note:** Preserve all speech content in the original Spanish. Do not translate.
Add the English summary only in the frontmatter `summary_en` field.

## Failure Handling

- If a URL returns a 404 or is clearly broken: log as `FAILED` and move on.
- If a URL is paywalled and no content is visible: log as `PAYWALLED` and move on.
- Do not retry more than once. Note any retry in the log.
- If partial content is accessible (e.g., intro paragraphs before a paywall), save what is
  available and note `[CONTENT TRUNCATED — PAYWALL]` at the end of the file.

## Collection Log Format

Maintain `data/raw_speeches/collection_log.md` with a running table. Append one row per URL
after processing it:

```markdown
| Date Collected | Title | Source URL | Status | Filename |
|---|---|---|---|---|
| 2026-04-16 | Discurso ante la ONU | https://... | OK | 2024-09-23-milei-un-general-assembly.md |
| 2026-04-16 | Entrevista TN | https://... | FAILED | — |
```

Status values: `OK`, `FAILED`, `PAYWALLED`, `PARTIAL`

Create the log file if it doesn't exist. Initialize it with the table header.

## Working Through Multiple URLs

When processing many URLs (e.g., from Notes.xlsx), work through them methodically:
- Process them one at a time to avoid overwhelming memory
- After every 5–10 items, note your progress in the conversation
- If a URL is a YouTube link, flag it for the youtube-transcript skill rather than trying to
  scrape the video page as HTML

## Quality Check Before Saving

Before writing each file, ask yourself:
- Does the content start with the frontmatter block?
- Is the `date` field accurate (not today, but the original date)?
- Is the text free of obvious boilerplate (nav menus, share buttons, unrelated articles)?
- Is the filename correctly formatted as `YYYY-MM-DD-slug.md`?
- Has the log been updated?

A well-collected corpus is the foundation of a sound analysis. Taking an extra moment to
check each file before saving is worth the effort.
