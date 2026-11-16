# 🎬 Cartoon-Jarvis — Free YouTube Video Studio

> **Topic in → YouTube-ready video out. 100% Free. No paid APIs.**

A complete automated video generation engine that takes a topic and produces an engaging animated stickman story video ready for YouTube upload.

---

## ✨ Features

- 🧠 **AI Story Generation** — Gemini API (free tier) writes a retention-optimised script
- 🎙️ **Voice Generation** — `edge-tts` (Microsoft, free, offline) in Hindi & English  
- 🖼️ **Scene Images** — Pollinations AI (completely free) or auto-generated placeholders  
- 🎬 **Canvas Renderer** — Headless Chromium + FFmpeg renders smooth 24fps animated video  
- 📝 **Auto Subtitles** — Synced captions generated from TTS timestamps  
- 🖼️ **Thumbnail** — High-CTR YouTube thumbnail auto-generated  
- 📦 **YouTube Kit** — Viral titles, description, tags — all auto-generated  

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
pip install edge-tts pillow
```

### 2. Install Node dependencies (for renderer)
```bash
cd studio/renderer/aitrends_kit
npm install
npx playwright install chromium
```

### 3. Generate a video

```bash
# English video
python main.py --topic "What if the Moon disappeared?" --lang en --engine aitrends

# Hindi video
python main.py --topic "Agar AI sab kuch le le?" --lang hi --engine aitrends

# 5-minute long video
python main.py --topic "The truth about discipline" --lang en --duration 5min --engine aitrends
```

Output: `output_videos/<topic>_<lang>_aitrends.mp4`

---

## 📁 Project Structure

```
agent x/
├── main.py                  ← Entry point: topic → video
├── studio/
│   ├── brain/
│   │   └── ai_director.py   ← Story & script generation (Gemini)
│   ├── audio/               ← TTS & SFX generation
│   ├── visual/              ← Thumbnail generator
│   ├── renderer/
│   │   ├── aitrends_bridge.py   ← Canvas renderer orchestrator
│   │   └── aitrends_kit/        ← HTML Canvas engine + render.mjs
│   └── storage/             ← Storage manager
├── projects/                ← Per-video project folders (auto-created)
├── output_videos/           ← Final MP4s + thumbnails
└── assets/                  ← SFX, music, fonts
```

---

## 🎨 Engine Styles

| Style | Description |
|-------|-------------|
| `aitrends` | Modern stickman canvas animation (recommended) |
| `studio` | Native PIL-based chunk renderer |

---

## 📋 Requirements

- Python 3.11+
- Node.js 18+
- FFmpeg (must be in PATH)
- `edge-tts` (`pip install edge-tts`)
- Pillow (`pip install pillow`)
- Gemini API key (optional — offline fallback included)

---

## 🆓 100% Free Stack

| Component | Tool | Cost |
|-----------|------|------|
| Story/Script | Gemini 1.5 Flash (free tier) | \$0 |
| Voice | edge-tts (Microsoft Edge TTS) | \$0 |
| Images | Pollinations AI | \$0 |
| Rendering | Playwright + FFmpeg | \$0 |
| Thumbnails | Custom PIL generator | \$0 |

---

## 🗑️ Cleanup

```bash
# Delete a specific video and all its assets
python main.py --delete "motivation_will_fail_you"

# Clean temp/cache files
python main.py --clean-temp

# Check storage usage
python main.py --storage
```

---

Made with ❤️ for creators who want to build a YouTube channel for free.
