---
name: youtube-transcript
description: >
  Extracts transcripts from YouTube video URLs and formats them as clean text for qualitative
  research and discourse analysis. Use this skill whenever: a URL in the source list points to
  a YouTube video, the user asks to "get the transcript" or "extract the subtitles" from a video,
  a speech or interview exists only as a YouTube video and you need its text, or you need to
  add a YouTube-sourced speech to `data/raw_speeches/`. Also use when you see `source_type: youtube`
  in a speech collection task. This skill handles both auto-generated and manual Spanish captions,
  produces clean running text without timestamps, and integrates with the speech-collector output
  format so the transcript is ready for discourse coding.
---

# YouTube Transcript Extractor

You are extracting transcript text from YouTube videos of political speeches and interviews
for use in qualitative discourse analysis. The goal is clean, readable running text — not raw
caption files with timestamps.

## Installation Check

Before attempting extraction, verify `yt-dlp` is available:

```bash
yt-dlp --version
```

If not installed:
```bash
pip install yt-dlp --break-system-packages
```

## Extraction Approach (try in order)

### Method 1 — yt-dlp (preferred)

Use `yt-dlp` to download the subtitle file without downloading the video:

```bash
# Download Spanish subtitles only (auto-generated or manual, whichever exists)
yt-dlp --write-auto-subs --write-subs --sub-lang es --skip-download \
  --output "/tmp/yt_transcript" "<youtube_url>"
```

This produces a `.vtt` or `.srt` file. After downloading, parse it into clean text:
- Strip all timestamps (lines like `00:00:12.340 --> 00:00:15.600`)
- Strip WebVTT headers and positioning tags (`<c>`, `<00:00:12.340>`, etc.)
- Remove duplicate lines (VTT files often repeat lines across cue blocks)
- Join into flowing paragraphs or line-separated segments

**If Spanish subtitles aren't available**, try Portuguese then English as fallbacks:
```bash
yt-dlp --write-auto-subs --sub-lang pt,en --skip-download \
  --output "/tmp/yt_transcript" "<youtube_url>"
```
Note in the frontmatter if a language other than Spanish was used.

### Method 2 — Browser-based extraction (fallback)

If `yt-dlp` fails or the video is geo-restricted:
1. Navigate to the video URL with browser tools
2. Click the three-dot menu below the video → "Open transcript"
3. Copy the transcript text from the panel that opens
4. Clean up the timestamps manually

### Method 3 — No captions available

If neither method yields a transcript:
1. Set `youtube_transcript: false` in frontmatter
2. Use the video title, description, and any visible on-screen text to write a brief summary
3. Note: `[TRANSCRIPT UNAVAILABLE — auto-captions not detected for this video]`
4. Log status as `NO_TRANSCRIPT` in `collection_log.md`

## Cleaning the Raw Transcript

After extraction, the raw VTT/SRT output needs cleaning before saving:

1. **Remove timestamps** — delete all timestamp lines and cue identifiers
2. **Remove duplicate segments** — VTT files cue by cue often repeat the same sentence;
   keep each sentence once
3. **Fix run-on joins** — when caption chunks are joined, add a space if one is missing
4. **Preserve paragraph breaks** where they exist in the original (speaker pauses often
   map to natural paragraph boundaries)
5. **Do not attempt to "fix" the Spanish** — preserve exactly what was said, including
   false starts, repetitions, and colloquialisms; these are analytically significant

The cleaned transcript should read as flowing prose, not as a list of caption chunks.

## Output Format

Save the transcript as part of the standard speech Markdown file. Use the same frontmatter
template as the speech-collector skill, adding the `youtube_transcript` field:

```markdown
---
title: "[Video title]"
date: YYYY-MM-DD
source_url: "https://www.youtube.com/watch?v=..."
source_type: youtube
language: es
youtube_transcript: true
caption_type: auto | manual
summary_en: "[Brief 1–2 sentence English summary]"
---

[SOURCE: YouTube transcript — auto-generated captions]

[Full cleaned transcript text in Spanish]
```

- `caption_type`: Set to `auto` for auto-generated captions, `manual` for manually uploaded
  subtitles. Auto-generated captions can have transcription errors; note this when coding.
- The `[SOURCE: ...]` line at the start of the body (not in frontmatter) signals to the
  analyst that the text came from auto-generated captions and may need extra scrutiny.

## Saving the File

Save to `data/raw_speeches/YYYY-MM-DD-slug.md` following the same naming convention as the
speech-collector skill. Update `data/raw_speeches/collection_log.md` accordingly.

Status values for the log:
- `OK` — transcript extracted and saved successfully
- `NO_TRANSCRIPT` — video exists but no captions available
- `FAILED` — URL is broken, video is private or deleted

## Common Issues

**yt-dlp returns no subtitle files:**
- Some videos don't have auto-captions enabled; try Method 2
- Very old videos or live streams may lack captions entirely

**Garbled auto-captions in Spanish:**
- This is expected for rapid speech or regional accents; preserve the text as-is
- Add a note in the frontmatter or coding memo: `[NOTE: Auto-captions may contain
  transcription errors in this segment]`

**Video is age-restricted or requires login:**
- Note as `FAILED` in the log and move on; do not attempt to bypass authentication

**Transcript is in a mix of Spanish and English:**
- Preserve the language as spoken (code-switching is itself analytically meaningful)
- Set `language: es-en` in frontmatter to flag the mix
