---
name: transcribe-audio
description: Extracts text from audio files (mp3, wav, aiff, etc.). Use this skill when asked to transcribe, read, or convert an audio file into text.
---

# Audio Transcription Skill

Gemini natively supports multimodal capabilities, including direct audio processing. There is no need for local models or system APIs.

## How to Use

When the user asks you to transcribe an audio file:

1. Use the `read_file` tool and pass the absolute path to the audio file.
2. Gemini will automatically process the audio and extract the text.
3. Return the transcribed text to the user.

### Supported Formats
- MP3, WAV, AIFF, AAC, OGG, FLAC
