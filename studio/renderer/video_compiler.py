"""
Video Compiler Engine
Concatenates individual scene chunks into the final master MP4 video
using FFmpeg concat demuxer (lossless & sub-second assembly).
"""

import os
import subprocess
from typing import List
import imageio_ffmpeg


class VideoCompiler:
    def __init__(self, output_dir: str = "output_videos"):
        self.output_dir = output_dir
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        os.makedirs(output_dir, exist_ok=True)

    def concatenate_chunks(
        self,
        chunk_paths: List[str],
        output_filename: str = "final_explainer.mp4"
    ) -> str:
        """
        Concatenates MP4 chunks into a single final master video.
        """
        if not chunk_paths:
            raise ValueError("No video chunks provided to concatenate.")

        final_output_path = os.path.join(self.output_dir, output_filename)
        concat_txt_path = os.path.join(os.path.dirname(chunk_paths[0]), "concat_list.txt")

        # Write FFmpeg concat list
        with open(concat_txt_path, "w", encoding="utf-8") as f:
            for path in chunk_paths:
                abs_path = os.path.abspath(path).replace("\\", "/")
                f.write(f"file '{abs_path}'\n")

        # Fast lossless copy concat
        cmd = [
            self.ffmpeg_exe,
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_txt_path,
            "-c", "copy",
            final_output_path
        ]

        print(f"Stitching {len(chunk_paths)} scenes into {final_output_path}...")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Video assembly complete! Output ready at: {final_output_path}")

        return final_output_path
