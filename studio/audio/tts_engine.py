"""
Neural Voiceover Engine ($0 Cost) using edge-tts
Generates studio-grade speech with millisecond word timestamps and true audio duration.
Resilient to network glitches, SSL inspection proxies (Sophos/antivirus), and offline timeouts.
"""

import asyncio
import os
import re
import ssl
import time
import json
import hashlib
import subprocess
from typing import List, Dict, Any, Tuple
import edge_tts
import edge_tts.communicate
import certifi
import imageio_ffmpeg

# Point OpenSSL and requests to certifi bundle
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# Prepare tolerant SSL context (handles local antivirus / captive portal MITM certs)
try:
    _SSL_VERIFIED = ssl.create_default_context(cafile=certifi.where())
except Exception:
    _SSL_VERIFIED = ssl.create_default_context()

_SSL_UNVERIFIED = ssl.create_default_context()
_SSL_UNVERIFIED.check_hostname = False
_SSL_UNVERIFIED.verify_mode = ssl.CERT_NONE


class TTSEngine:
    VOICE_MAP = {
        "hi": "hi-IN-MadhurNeural",        # Hindi Male narrative
        "hi_female": "hi-IN-SwaraNeural",   # Hindi Female narrative
        "en": "en-US-ChristopherNeural",   # English Male deep storytelling
        "en_female": "en-US-JennyNeural"   # English Female clear narrative
    }

    def __init__(self, default_lang: str = "hi"):
        self.default_lang = default_lang
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    def get_audio_duration(self, audio_path: str) -> float:
        """Extracts true audio duration using FFmpeg."""
        try:
            cmd = [self.ffmpeg_exe, "-i", audio_path]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
            if match:
                h, m, s = match.groups()
                return int(h) * 3600 + int(m) * 60 + float(s)
        except Exception:
            pass
        return 4.0

    async def _stream_edge_tts(
        self,
        text: str,
        voice: str,
        output_audio_path: str,
        ssl_ctx: ssl.SSLContext
    ) -> List[Dict[str, Any]]:
        # Set module SSL context
        edge_tts.communicate._SSL_CTX = ssl_ctx
        communicate = edge_tts.Communicate(text, voice)
        word_timestamps = []
        sentence_boundaries = []

        os.makedirs(os.path.dirname(os.path.abspath(output_audio_path)), exist_ok=True)

        with open(output_audio_path, "wb") as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    start_sec = chunk["offset"] / 10_000_000.0
                    duration_sec = chunk["duration"] / 10_000_000.0
                    word_timestamps.append({
                        "word": chunk["text"],
                        "start": round(start_sec, 3),
                        "end": round(start_sec + duration_sec, 3)
                    })
                elif chunk["type"] == "SentenceBoundary":
                    start_sec = chunk["offset"] / 10_000_000.0
                    duration_sec = chunk["duration"] / 10_000_000.0
                    sentence_boundaries.append({
                        "text": chunk.get("text", ""),
                        "start": start_sec,
                        "duration": duration_sec
                    })

        # If WordBoundary wasn't emitted, derive word timestamps from SentenceBoundary
        if not word_timestamps and sentence_boundaries:
            for sb in sentence_boundaries:
                words = sb["text"].strip().split()
                if not words:
                    continue
                w_dur = sb["duration"] / len(words)
                for idx, w in enumerate(words):
                    w_start = sb["start"] + idx * w_dur
                    word_timestamps.append({
                        "word": w,
                        "start": round(w_start, 3),
                        "end": round(w_start + w_dur, 3)
                    })

        return word_timestamps

    async def _synthesize_async(
        self,
        text: str,
        voice: str,
        output_audio_path: str
    ) -> List[Dict[str, Any]]:
        last_err = None
        # Try verified SSL first, then unverified SSL fallback (for corporate / antivirus proxies)
        ssl_options = [_SSL_VERIFIED, _SSL_UNVERIFIED]

        for attempt in range(3):
            ssl_ctx = ssl_options[min(attempt, len(ssl_options) - 1)]
            try:
                words = await self._stream_edge_tts(text, voice, output_audio_path, ssl_ctx)
                if os.path.exists(output_audio_path) and os.path.getsize(output_audio_path) > 500:
                    return words
            except Exception as e:
                last_err = e
                await asyncio.sleep(0.8 * (attempt + 1))

        # If all network attempts fail, generate offline fallback audio to prevent crash
        print(f"  [TTS Fallback] Network TTS unavailable ({last_err}), using offline audio...")
        words_list = text.strip().split()
        estimated_dur = max(3.5, len(words_list) * 0.42 + 0.6)

        # Synthesize quiet audio using FFmpeg lavfi
        os.makedirs(os.path.dirname(os.path.abspath(output_audio_path)), exist_ok=True)
        ffmpeg_cmd = [
            self.ffmpeg_exe, "-y",
            "-f", "lavfi", "-i", f"sine=frequency=0:duration={estimated_dur}",
            "-q:a", "9", "-acodec", "libmp3lame",
            output_audio_path
        ]
        subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Distribute words linearly
        word_dur = (estimated_dur - 0.4) / max(1, len(words_list))
        offline_words = []
        for i, w in enumerate(words_list):
            s = 0.2 + i * word_dur
            offline_words.append({
                "word": w,
                "start": round(s, 3),
                "end": round(s + word_dur, 3)
            })
        return offline_words

    def synthesize(
        self,
        text: str,
        output_audio_path: str,
        lang: str = "hi",
        voice: str = None,
        force_refresh: bool = False
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Synthesizes speech and returns (word_timestamps, total_duration).
        Uses hash-based verification to ensure the generated audio strictly matches
        the current text, language, and voice — never reusing stale audio from different scenes.
        """
        clean_text = text.strip()
        chosen_voice = voice or self.VOICE_MAP.get(lang, self.VOICE_MAP["en"])
        meta_path = output_audio_path + ".meta.json"
        
        # Calculate unique content hash
        content_hash = hashlib.sha256(f"{clean_text}_{lang}_{chosen_voice}".encode("utf-8")).hexdigest()

        # Check if valid matching cache exists
        is_cache_valid = False
        if not force_refresh and os.path.exists(output_audio_path) and os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                if meta.get("hash") == content_hash and os.path.getsize(output_audio_path) > 2000:
                    is_cache_valid = True
                    cached_words = meta.get("words", [])
                    cached_dur = meta.get("duration", 0.0)
                    if cached_words and cached_dur > 0.5:
                        return cached_words, cached_dur
            except Exception:
                is_cache_valid = False

        # If cache invalid or stale, remove old files to prevent audio leakage
        if not is_cache_valid:
            if os.path.exists(output_audio_path):
                try:
                    os.remove(output_audio_path)
                except Exception:
                    pass
            if os.path.exists(meta_path):
                try:
                    os.remove(meta_path)
                except Exception:
                    pass

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import nest_asyncio
                nest_asyncio.apply()
                words = loop.run_until_complete(self._synthesize_async(clean_text, chosen_voice, output_audio_path))
            else:
                words = loop.run_until_complete(self._synthesize_async(clean_text, chosen_voice, output_audio_path))
        except RuntimeError:
            words = asyncio.run(self._synthesize_async(clean_text, chosen_voice, output_audio_path))

        # Always verify true duration using FFmpeg
        true_duration = self.get_audio_duration(output_audio_path)

        # Fallback if words is still empty (fallback linear distribution)
        if not words and clean_text:
            raw_words = clean_text.split()
            if raw_words:
                time_per_word = max(0.1, (true_duration - 0.4) / len(raw_words))
                start_offset = 0.2
                for i, w in enumerate(raw_words):
                    w_s = start_offset + i * time_per_word
                    words.append({
                        "word": w,
                        "start": round(w_s, 3),
                        "end": round(w_s + time_per_word, 3)
                    })

        # Save metadata cache
        try:
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump({
                    "hash": content_hash,
                    "text": clean_text,
                    "lang": lang,
                    "voice": chosen_voice,
                    "duration": true_duration,
                    "words": words
                }, f, ensure_ascii=False)
        except Exception:
            pass

        return words, true_duration

