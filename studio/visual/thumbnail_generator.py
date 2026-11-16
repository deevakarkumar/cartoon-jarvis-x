"""
YouTube High-CTR Viral Thumbnail Generator
Renders eye-catching, high-contrast thumbnails with bold clickbait hooks,
dramatic stick-figure poses, and glowing procedural vector props.
"""

import os
from typing import Dict, Any, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from studio.visual.stick_rig import StickFigureRig
from studio.visual.scene_composer import SceneComposer


class ThumbnailGenerator:
    def __init__(self, width: int = 1280, height: int = 720):
        self.width = width
        self.height = height
        self.rig = StickFigureRig()
        self.composer = SceneComposer(width, height)
        self.font = self._load_font(int(height * 0.11))
        self.font_sub = self._load_font(int(height * 0.08))

    def _load_font(self, size: int) -> ImageFont.ImageFont:
        possible_fonts = [
            "C:/Windows/Fonts/impact.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/seguiemj.ttf",
            "C:/Windows/Fonts/comicbd.ttf"
        ]
        for f in possible_fonts:
            if os.path.exists(f):
                try:
                    return ImageFont.truetype(f, size)
                except Exception:
                    continue
        return ImageFont.load_default()

    def generate_thumbnail(
        self,
        hook_text: str,
        bg_style: str = "dusk_space",
        prop_type: str = "question_mark",
        char_pose: str = "panicking",
        char_expression: str = "screaming",
        output_path: str = "output_videos/thumbnail.jpg"
    ) -> str:
        """
        Renders a viral YouTube thumbnail.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 1. Base Environment
        base = self.composer.render_background(bg_style)

        # 2. Add dramatic radial vignette for focus
        vignette = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        v_draw = ImageDraw.Draw(vignette)
        cx, cy = self.width // 2, self.height // 2
        for r in range(int(self.width * 0.4), int(self.width * 0.75), 18):
            alpha = int(min(180, (r - self.width * 0.4) / (self.width * 0.35) * 160))
            v_draw.ellipse([cx - r, cy - int(r * 0.6), cx + r, cy + int(r * 0.6)], outline=(0, 0, 0, alpha), width=18)
        base.paste(vignette, (0, 0), vignette)

        # 3. Draw Hero Character (Left-aligned, perfectly framed)
        char_x = int(self.width * 0.26)
        char_y = int(self.height * 0.96)
        char_scale = 1.35 if self.width >= self.height else 1.6

        self.rig.draw_character(
            base,
            x=char_x,
            y=char_y,
            scale=char_scale,
            flip_x=False,
            expression=char_expression,
            pose=char_pose,
            mouth_open_ratio=0.85
        )

        # 4. Draw Hero Prop (Right-aligned, large & glowing)
        prop_x = int(self.width * 0.74)
        prop_y = int(self.height * 0.52)
        prop_scale = 1.45
        self.composer.draw_prop(base, prop_type, prop_x, prop_y, scale=prop_scale)

        # 5. Bold High-CTR Clickbait Text Overlay (Unified Badge)
        draw = ImageDraw.Draw(base)
        hook_upper = hook_text.upper().strip()
        words = hook_upper.split()
        if len(words) > 3:
            mid = len(words) // 2
            lines = [" ".join(words[:mid]), " ".join(words[mid:])]
        else:
            lines = [hook_upper]

        badge_pad_x = 36
        badge_pad_y = 16
        all_lines_info = []
        max_line_w = 0
        total_h = 0
        for idx, line in enumerate(lines):
            cur_font = self.font if idx == 0 else self.font_sub
            bbox = draw.textbbox((0, 0), line, font=cur_font)
            lw = bbox[2] - bbox[0]
            lh = bbox[3] - bbox[1]
            all_lines_info.append((line, cur_font, lw, lh))
            if lw > max_line_w:
                max_line_w = lw
            total_h += lh + 10

        badge_w = max_line_w + badge_pad_x * 2
        badge_h = total_h + badge_pad_y * 2
        badge_x = (self.width - badge_w) // 2
        badge_y = int(self.height * 0.06)

        # Draw unified dark badge with striking gold border
        draw.rounded_rectangle(
            [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
            radius=18,
            fill=(12, 12, 18, 235),
            outline=(255, 215, 0),
            width=4
        )

        cur_text_y = badge_y + badge_pad_y
        for idx, (line, cur_font, lw, lh) in enumerate(all_lines_info):
            lx = (self.width - lw) // 2
            # Outline for ultra legibility
            for dx in range(-4, 5):
                for dy in range(-4, 5):
                    draw.text((lx + dx, cur_text_y + dy), line, font=cur_font, fill=(0, 0, 0))
            # Text fill (Yellow headline, Electric Red subline)
            fill_c = (255, 230, 0) if idx == 0 else (255, 60, 60)
            draw.text((lx, cur_text_y), line, font=cur_font, fill=fill_c)
            cur_text_y += lh + 10

        # Convert to RGB and save high quality JPEG
        final_thumb = base.convert("RGB")
        final_thumb.save(output_path, "JPEG", quality=95)
        print(f"  [Thumbnail] Saved -> {output_path}")
        return output_path
