"""
Audio Mixer Engine
Handles BGM ducking, SFX triggering, and audio track mastering using FFmpeg.
Supports both .wav and .mp3 SFX formats.
"""

import os
import subprocess
import imageio_ffmpeg


class AudioMixer:
    def __init__(self, bgm_path: str = "assets/bgm/ambient_explainer_bgm.wav", sfx_dir: str = "assets/sfx"):
        self.bgm_path = bgm_path
        self.sfx_dir = sfx_dir
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    def _find_sfx_path(self, sfx_name: str):
        if not sfx_name or sfx_name == "none":
            return None
        for ext in [".wav", ".mp3"]:
            p = os.path.join(self.sfx_dir, f"{sfx_name}{ext}")
            if os.path.exists(p):
                return p
        return None

    def mix_scene_audio(
        self,
        voice_path: str,
        output_mixed_path: str,
        sfx_name: str = "none",
        duration: float = 5.0,
        bgm_volume: float = 0.12
    ) -> str:
        """
        Combines voiceover, sound effect, and ducked background music into a master audio file.
        Uses FFmpeg complex audio filtergraph.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_mixed_path)), exist_ok=True)
        sfx_path = self._find_sfx_path(sfx_name)

        inputs = ["-i", voice_path]
        filter_parts = []
        mix_count = 1

        # 1. Voice input is [0:a]
        filter_parts.append("[0:a]volume=1.0[voice]")

        # 2. Add SFX if valid
        if sfx_path and os.path.exists(sfx_path):
            inputs.extend(["-i", sfx_path])
            sfx_idx = mix_count
            mix_count += 1
            filter_parts.append(f"[{sfx_idx}:a]volume=0.85[sfx]")

        # 3. Add BGM if exists
        has_bgm = self.bgm_path and os.path.exists(self.bgm_path)
        if has_bgm:
            inputs.extend(["-stream_loop", "-1", "-i", self.bgm_path])
            bgm_idx = mix_count
            mix_count += 1
            # Ducked background music
            filter_parts.append(f"[{bgm_idx}:a]volume={bgm_volume},atrim=0:{duration}[bgm]")

        # Construct amix
        if mix_count == 3:
            filter_parts.append("[voice][sfx][bgm]amix=inputs=3:duration=first:dropout_transition=2[outa]")
        elif mix_count == 2:
            second = "sfx" if (sfx_path and os.path.exists(sfx_path)) else "bgm"
            filter_parts.append(f"[voice][{second}]amix=inputs=2:duration=first:dropout_transition=2[outa]")
        else:
            filter_parts.append("[voice]anull[outa]")

        cmd = [
            self.ffmpeg_exe,
            "-y",
            *inputs,
            "-filter_complex", ";".join(filter_parts),
            "-map", "[outa]",
            "-t", str(duration),
            "-ac", "2",
            "-ar", "44100",
            output_mixed_path
        ]

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return output_mixed_path
        except subprocess.CalledProcessError:
            return voice_path
