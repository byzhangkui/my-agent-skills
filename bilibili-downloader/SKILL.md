---
name: bilibili-downloader
description: Download Bilibili videos, multi-part uploads, and course pages with yt-dlp. Use when Codex needs to provide commands or troubleshooting for saving Bilibili content locally, especially when the user wants high quality video, needs browser cookies for logged-in access, wants a specific page such as ?p=4, needs batch download of a multi-part upload, or wants to inspect available formats before downloading.
---

# Bilibili Downloader

## Overview

Use `yt-dlp` plus browser cookies to download Bilibili videos at the highest quality the user's account can access. Always remind the user that Bilibili downloads should be done with a logged-in browser session or exported cookies. Prefer concrete shell commands over long explanations, and treat courses and member-only quality tiers as login-dependent. Default to the clearest available version, not the most compatible one.

## Workflow

1. Check whether `yt-dlp` is installed before suggesting any download command. If it is missing, tell the user to install `yt-dlp` first, and mention `ffmpeg` at the same time when stream merging will be needed.
2. Confirm the target URL type.
3. Confirm the browser to read cookies from.
4. Inspect formats with `-F` before choosing a download command.
5. Prefer the highest available quality by default and use `bv+ba/b` so separate video and audio streams can merge through `ffmpeg`.
6. Adjust for single-page, multi-part, playlist, course, or audio-only requests.

## Prerequisite Check

Before giving download steps, first verify that `yt-dlp` exists on the user's machine with a simple check such as:

```bash
yt-dlp --version
```

If that command is not found or the user says `yt-dlp` is not installed, stop and tell them to install it first instead of continuing with download commands.

On macOS, suggest:

```bash
brew install yt-dlp ffmpeg
```

After installation, resume with format inspection and the final download command.

## URL Handling

- For standard videos, accept URLs like `https://www.bilibili.com/video/BV...`.
- For a specific part of a multi-part upload, preserve `?p=<number>`.
- Remove unrelated tracking parameters such as `spm_id_from` or `vd_source` unless they are needed to keep the page selection.
- If the user says "course", default to downloading the full playlist or anthology, not a single page.
- If the provided link is still a BV page, treat it as a course playlist when the user asks for the course.
- If the link points to a dedicated course or classroom page, say that support depends on whether `yt-dlp` can extract the playable media and whether the platform applies DRM.

## Default Commands

Use `chrome` as the default browser example unless the user names another browser.

Before giving any command, remind the user that high-quality Bilibili downloads typically require login and that the command assumes browser cookies from a logged-in session.

Check formats first:

```bash
yt-dlp -F --cookies-from-browser chrome "https://www.bilibili.com/video/BVxxxxxxxx"
```

Download the best video and audio streams the account can access:

```bash
yt-dlp --cookies-from-browser chrome -f "bv+ba/b" "https://www.bilibili.com/video/BVxxxxxxxx"
```

If the user explicitly asks for the clearest version, give the same command unless a prior `-F` result shows a more specific best format pair to pin.

Download a specific page in a multi-part upload:

```bash
yt-dlp --cookies-from-browser chrome -f "bv+ba/b" "https://www.bilibili.com/video/BVxxxxxxxx?p=4"
```

Save to `~/Downloads` with a stable name template:

```bash
yt-dlp \
  --cookies-from-browser chrome \
  -f "bv+ba/b" \
  -P ~/Downloads \
  -o "%(playlist_index)s-%(title)s [%(id)s].%(ext)s" \
  "https://www.bilibili.com/video/BVxxxxxxxx"
```

For courses or other multi-item learning content, create a dedicated subfolder under `~/Downloads`:

```bash
yt-dlp \
  --cookies-from-browser chrome \
  -f "bv+ba/b" \
  -P "home:~/Downloads/%(playlist_title)s" \
  -o "%(playlist_index)s-%(title)s [%(id)s].%(ext)s" \
  "URL"
```

## Quality Rules

- Tell the user that actual maximum quality depends on what appears in `yt-dlp -F`.
- Explain that higher resolutions often require login, and some tiers may require a paid membership.
- Even if the user does not ask, default to the highest available quality and recommend checking formats first with `-F`.
- If the user wants "highest quality" or "most clear", default to `-f "bv+ba/b"` after checking formats.
- If `-F` output is already available in the conversation, prefer pinning the exact top-quality pair from that output instead of replying with a generic selector.
- Do not prefer AVC over HEVC unless the user asks for compatibility or reports playback issues.
- If the user wants to prefer a ceiling such as 1080p, use sorting:

```bash
yt-dlp --cookies-from-browser chrome -S "res:1080,+br,+size" -f "bv+ba/b" "URL"
```

- Mention that `ffmpeg` is required for merging separate streams.

## Browser Cookies

- Always mention that login is recommended before providing the final command.
- Prefer `--cookies-from-browser <browser>` over manually exported cookie files.
- Common browser values: `chrome`, `edge`, `firefox`, `safari`.
- If the user reports low quality or `403`, tell them to open the video in the browser, confirm they are logged in, then retry immediately.
- If browser cookie extraction fails, fall back to:

```bash
yt-dlp --cookies cookies.txt -f "bv+ba/b" "URL"
```

## Common Variants

Audio only:

```bash
yt-dlp --cookies-from-browser chrome -x --audio-format mp3 "URL"
```

Single video only, not the full playlist:

```bash
yt-dlp --cookies-from-browser chrome --no-playlist -f "bv+ba/b" "URL"
```

Full multi-part upload:

```bash
yt-dlp --cookies-from-browser chrome -f "bv+ba/b" "https://www.bilibili.com/video/BVxxxxxxxx"
```

Course download into its own folder:

```bash
yt-dlp --cookies-from-browser chrome -f "bv+ba/b" -P "home:~/Downloads/%(playlist_title)s" -o "%(playlist_index)s-%(title)s [%(id)s].%(ext)s" "URL"
```

## Troubleshooting

- If `yt-dlp` is missing or outdated, suggest `brew install yt-dlp ffmpeg` on macOS and `yt-dlp -U` for updates.
- If `-F` shows only low-quality formats, explain that the account probably lacks access to higher tiers on that item.
- If extraction fails on a course page, say plainly that some course pages may not be supported by the extractor or may use DRM, which `yt-dlp` cannot bypass.
- If the user pastes a command instead of asking a question, convert it into the next concrete command they should run.

## Response Style

- Keep responses command-first.
- First confirm `yt-dlp` is installed if that has not already been established in the conversation.
- Always include a short login reminder before or after the command.
- Default the output path to `~/Downloads` unless the user asks for another location.
- If the content is a course, default to a dedicated subfolder under `~/Downloads`, preferably named from `%(playlist_title)s`.
- If the user provides multiple course URLs, download each URL as its own playlist and store each one in its own subfolder.
- Do not use `--no-playlist` when the user asks for a course or an entire course.
- Preserve the user's exact BV URL and `?p=` selection when present.
- Avoid speculative claims about paid courses or DRM. State limitations as possibilities unless confirmed by an error log.
- When the user asks for one final command, return a single cleaned command that targets the highest available quality plus one short login reminder.
- If known formats are already listed, choose the clearest exact format IDs instead of a generic fallback.
