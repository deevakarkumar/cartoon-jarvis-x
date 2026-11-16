"""
Procedural SFX Generator ($0 Cost)
Generates high-quality sound effects (pop, whoosh, ding) using math/numpy,
ensuring zero external download requirements.
"""

import math
import os
import struct
import wave
import numpy as np


class SFXGenerator:
    def __init__(self, sfx_dir: str = "assets/sfx"):
        self.sfx_dir = sfx_dir
        os.makedirs(sfx_dir, exist_ok=True)
        self.sample_rate = 44100

    def ensure_sfx(self):
        """Ensures that default sound effects exist on disk."""
        pop_path = os.path.join(self.sfx_dir, "pop.wav")
        whoosh_path = os.path.join(self.sfx_dir, "whoosh.wav")
        ding_path = os.path.join(self.sfx_dir, "ding.wav")

        if not os.path.exists(pop_path):
            self._create_pop(pop_path)
        if not os.path.exists(whoosh_path):
            self._create_whoosh(whoosh_path)
        if not os.path.exists(ding_path):
            self._create_ding(ding_path)

    def _save_wav(self, file_path: str, samples: np.ndarray):
        samples = np.clip(samples, -1.0, 1.0)
        int_samples = (samples * 32767).astype(np.int16)
        with wave.open(file_path, "w") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(int_samples.tobytes())

    def _create_pop(self, file_path: str):
        # Short punchy frequency drop (500Hz -> 100Hz) in 0.09s
        duration = 0.09
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        freq = np.linspace(500, 100, len(t))
        phase = 2 * np.pi * np.cumsum(freq) / self.sample_rate
        envelope = np.exp(-t * 40)
        samples = np.sin(phase) * envelope * 0.8
        self._save_wav(file_path, samples)

    def _create_whoosh(self, file_path: str):
        # Filtered white noise with bell curve envelope (0.35s)
        duration = 0.35
        n_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        # Random noise
        noise = np.random.uniform(-1, 1, n_samples)
        # Soft bandpass filter approximation using sinusoidal modulation
        sweep = np.sin(np.pi * (t / duration)) ** 2
        carrier = np.sin(2 * np.pi * np.linspace(200, 800, n_samples) * t)
        samples = (noise * 0.4 + carrier * 0.6) * sweep * 0.6
        self._save_wav(file_path, samples)

    def _create_ding(self, file_path: str):
        # Bright metallic chime (1400Hz + 2800Hz) in 0.6s
        duration = 0.6
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        decay = np.exp(-t * 7)
        s1 = np.sin(2 * np.pi * 1400 * t)
        s2 = np.sin(2 * np.pi * 2800 * t) * 0.4
        s3 = np.sin(2 * np.pi * 4200 * t) * 0.15
        samples = (s1 + s2 + s3) * decay * 0.7
        self._save_wav(file_path, samples)


if __name__ == "__main__":
    gen = SFXGenerator("assets/sfx")
    gen.ensure_sfx()
    print("Default SFX verified and generated in assets/sfx/")
