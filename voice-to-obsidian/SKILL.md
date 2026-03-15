---
name: voice-to-obsidian
description: Transcribes an audio file into text using the "transcribe-audio" skill, then saves the result as a markdown file in the "~/Obsidian Vault/00_Inbox" directory with the naming convention Date-Time-Topic.md.
---

# Voice to Obsidian

This skill is designed to take an audio file (e.g., voice memo, lecture recording), transcribe it using the existing `transcribe-audio` skill, and then automatically save the transcription into an Obsidian Inbox.

## Workflow

When the user asks to process an audio file for their Obsidian Inbox, follow these steps:

### Step 1: Transcribe the Audio

1. Ensure the `transcribe-audio` skill is available or use its underlying capabilities.
2. Transcribe the provided audio file to extract the full text.

### Step 2: Determine the File Name

1. Determine the current date and time (format: `YYYY-MM-DD-HH-MM-SS`).
2. Determine a short "Topic" based on a quick summary of the transcribed text (e.g., `Project-Meeting`, `Ideas-for-App`). Replace spaces with hyphens.
3. The final filename should be: `YYYY-MM-DD-HH-MM-SS-<Topic>.md`.

### Step 3: Save to Obsidian Inbox

1. The target directory is exactly `~/Obsidian Vault/00_Inbox`.
2. Expand the `~` path if necessary to absolute path.
3. Check if the directory exists. If it doesn't, create it using `mkdir -p "~/Obsidian Vault/00_Inbox"`.
4. Write the transcribed text into the new markdown file in that directory. You can add a YAML frontmatter to the markdown file with the `date` and `topic` if appropriate, but the main content must be the full transcription.

### Step 4: Confirm

1. Respond to the user confirming that the transcription has been saved, providing the exact file path created.