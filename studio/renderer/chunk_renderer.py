"""
Scene-by-Scene Chunk Renderer
Renders individual scenes into self-contained MP4 video chunks.
Prevents RAM crashes by processing scenes independently.
"""

import os
import subprocess
from typing import Dict, Any, List
import cv2
import numpy as np
import imageio_ffmpeg

from studio.visual.scene_composer import SceneComposer
from studio.visual.subtitle_engine import KineticSubtitleEngine
from studio.audio.tts_engine import TTSEngine
from studio.audio.audio_mixer import AudioMixer


class ChunkRenderer:
    def __init__(
        self,
        width: int = 1920,
        height: int = 1080,
        fps: int = 24,
        temp_dir: str = "temp"
    ):
        self.width = width
        self.height = height
        self.fps = fps
        self.temp_dir = temp_dir
        self.composer = SceneComposer(width, height)
        self.subtitle_engine = KineticSubtitleEngine()
        self.tts = TTSEngine()
        self.mixer = AudioMixer()
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

        os.makedirs(os.path.join(temp_dir, "audio"), exist_ok=True)
        os.makedirs(os.path.join(temp_dir, "chunks"), exist_ok=True)

    def render_scene_chunk(
        self,
        scene: Dict[str, Any],
        scene_idx: int,
        lang: str = "hi"
    ) -> str:
        """
        Renders a single scene to temp/chunks/scene_{idx:03d}.mp4
        """
        narration = scene.get("narration", "")
        voice_path = os.path.join(self.temp_dir, "audio", f"voice_{scene_idx:03d}.mp3")
        mixed_audio_path = os.path.join(self.temp_dir, "audio", f"mixed_{scene_idx:03d}.wav")
        chunk_path = os.path.join(self.temp_dir, "chunks", f"scene_{scene_idx:03d}.mp4")

        # 1. Synthesize Voice & Extract Accurate Timestamps + Duration
        print(f"  [Scene {scene_idx}] Generating Voiceover...")
        words, raw_duration = self.tts.synthesize(narration, voice_path, lang=lang)

        # Padding of 0.3s after speech ends for natural breath
        duration = max(2.5, raw_duration + 0.3)

        # 2. Mix Scene Audio (Voice + SFX + BGM)
        sfx_name = scene.get("sfx", "none")
        self.mixer.mix_scene_audio(voice_path, mixed_audio_path, sfx_name=sfx_name, duration=duration)

        # 3. Prepare Subtitle Groups
        subtitle_groups = self.subtitle_engine.group_timestamps(words)

        # 4. Stream Frames directly to FFmpeg via stdin pipe
        total_frames = int(duration * self.fps)
        print(f"  [Scene {scene_idx}] Rendering {total_frames} frames ({duration:.1f}s)...")

        cmd = [
            self.ffmpeg_exe,
            "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{self.width}x{self.height}",
            "-pix_fmt", "bgr24",
            "-r", str(self.fps),
            "-i", "-",
            "-i", mixed_audio_path,
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", str(duration),
            chunk_path
        ]

        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        shake_val = scene.get("shake", 0.0)

        for f in range(total_frames):
            t = f / float(self.fps)

            # Check if speaking
            is_speaking = any(w["start"] <= t <= w["end"] for w in words)

            # Subtle ease-in camera zoom over scene
            zoom_progress = 1.0 + (t / duration) * 0.08

            # Compose visual frame
            pil_frame = self.composer.compose_frame(
                scene_info=scene,
                t=t,
                is_speaking=is_speaking,
                camera_zoom=zoom_progress,
                shake_intensity=shake_val if t < 0.8 else 0.0
            )

            # Burn Kinetic Subtitles onto frame
            pil_frame = self.subtitle_engine.draw_subtitle_on_frame(
                pil_frame,
                current_time=t,
                groups=subtitle_groups
            )

            # Convert PIL RGB to OpenCV BGR raw bytes
            frame_np = np.array(pil_frame)
            frame_bgr = cv2.cvtColor(frame_np, cv2.COLOR_RGB2BGR)

            # Pipe to FFmpeg with error guard
            try:
                proc.stdin.write(frame_bgr.tobytes())
            except (BrokenPipeError, OSError):
                break

        try:
            proc.stdin.close()
        except Exception:
            pass
        proc.wait()

        print(f"  [Scene {scene_idx}] Chunk saved -> {chunk_path}")
        return chunk_path
