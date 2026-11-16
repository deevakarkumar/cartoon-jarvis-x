"""
Kinetic Subtitles Engine
Renders high-retention, word-by-word highlighted subtitles with dark outlines
and pop effects on Pillow frames.
"""

from typing import List, Dict, Any, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
import os


class KineticSubtitleEngine:
    def __init__(
        self,
        font_size: int = 52,
        primary_color: Tuple[int, int, int] = (255, 230, 0),    # Vibrant Yellow
        normal_color: Tuple[int, int, int] = (255, 255, 255),    # White
        outline_color: Tuple[int, int, int] = (10, 10, 15),     # Deep Black
        outline_width: int = 5,
        words_per_group: int = 4
    ):
        self.font_size = font_size
        self.primary_color = primary_color
        self.normal_color = normal_color
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.words_per_group = words_per_group
        self.font = self._load_best_font(font_size)

    def _load_best_font(self, size: int) -> ImageFont.ImageFont:
        """Loads a bold punchy font from system or falls back gracefully."""
        possible_fonts = [
            "C:/Windows/Fonts/impact.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/seguiemj.ttf",
            "C:/Windows/Fonts/comicbd.ttf",
            "C:/Windows/Fonts/tahomabd.ttf"
        ]
        for f in possible_fonts:
            if os.path.exists(f):
                try:
                    return ImageFont.truetype(f, size)
                except Exception:
                    continue
        return ImageFont.load_default()

    def group_timestamps(self, words: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Groups words into bite-sized 3-5 word subtitle batches.
        """
        groups = []
        for i in range(0, len(words), self.words_per_group):
            chunk = words[i:i + self.words_per_group]
            if not chunk:
                continue
            groups.append({
                "start": chunk[0]["start"],
                "end": chunk[-1]["end"] + 0.2,
                "words": chunk
            })
        return groups

    def draw_subtitle_on_frame(
        self,
        img: Image.Image,
        current_time: float,
        groups: List[Dict[str, Any]],
        y_ratio: float = 0.82
    ) -> Image.Image:
        """
        Draws the active word group for the given timestamp onto the image.
        The currently spoken word is highlighted in primary_color.
        """
        # Find active group
        active_group = None
        for g in groups:
            if g["start"] <= current_time <= g["end"]:
                active_group = g
                break

        if not active_group:
            return img

        draw = ImageDraw.Draw(img)
        w, h = img.size
        center_y = int(h * y_ratio)

        # Measure dimensions of each word
        word_items = active_group["words"]
        text_elements = []
        total_width = 0
        space_width = 16

        for item in word_items:
            txt = item["word"]
            # getbbox returns (left, top, right, bottom)
            bbox = draw.textbbox((0, 0), txt, font=self.font)
            txt_w = bbox[2] - bbox[0]
            txt_h = bbox[3] - bbox[1]
            text_elements.append({
                "word": txt,
                "start": item["start"],
                "end": item["end"],
                "width": txt_w,
                "height": txt_h
            })
            total_width += txt_w + space_width

        total_width -= space_width
        start_x = (w - total_width) // 2

        cur_x = start_x
        for elem in text_elements:
            is_active = (elem["start"] <= current_time <= elem["end"])
            color = self.primary_color if is_active else self.normal_color
            
            # Subtle bounce/pop for active word
            y_offset = -4 if is_active else 0
            
            # Draw outline for maximum readability
            for dx in range(-self.outline_width, self.outline_width + 1):
                for dy in range(-self.outline_width, self.outline_width + 1):
                    if dx * dx + dy * dy <= self.outline_width * self.outline_width:
                        draw.text(
                            (cur_x + dx, center_y + y_offset + dy),
                            elem["word"],
                            font=self.font,
                            fill=self.outline_color
                        )

            # Draw main text
            draw.text(
                (cur_x, center_y + y_offset),
                elem["word"],
                font=self.font,
                fill=color
            )

            cur_x += elem["width"] + space_width

        return img
