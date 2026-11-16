"""
Scene Composer Engine
Composes the complete visual frame: background environment, procedural props,
character rigs with breathing/lip-sync, camera zooms, and screen shakes.
"""

import math
import random
from typing import Tuple, Dict, Any, Optional
from PIL import Image, ImageDraw
import numpy as np

from studio.visual.stick_rig import StickFigureRig


class SceneComposer:
    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height
        self.rig = StickFigureRig()

    def render_background(
        self,
        style: str = "dusk_space"
    ) -> Image.Image:
        """Creates stylized background canvas."""
        bg = Image.new("RGBA", (self.width, self.height))
        draw = ImageDraw.Draw(bg)

        if style == "dusk_space":
            # Gradient from deep navy/violet to dark horizon
            for y in range(self.height):
                t = y / self.height
                r = int(14 + 14 * t)
                g = int(14 + 10 * t)
                b = int(28 + 26 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))

            # Subtle perspective floor grid
            horizon_y = int(self.height * 0.72)
            draw.line([(0, horizon_y), (self.width, horizon_y)], fill=(45, 45, 75, 180), width=2)

            center_x = self.width // 2
            for offset in range(-self.width, self.width * 2, 140):
                draw.line([(center_x + offset // 4, horizon_y), (offset, self.height)], fill=(35, 35, 55, 120), width=1)

        elif style == "pitch_black_space":
            # Deep cosmic pitch black with twinkling distant stars
            bg = Image.new("RGBA", (self.width, self.height), (8, 9, 14, 255))
            draw = ImageDraw.Draw(bg)
            # Static seeded stars
            rng = random.Random(42)
            for _ in range(120):
                sx = rng.randint(0, self.width)
                sy = rng.randint(0, int(self.height * 0.75))
                brightness = rng.randint(150, 255)
                draw.point((sx, sy), fill=(brightness, brightness, brightness, 255))

            horizon_y = int(self.height * 0.75)
            draw.line([(0, horizon_y), (self.width, horizon_y)], fill=(30, 32, 45, 200), width=2)

        elif style == "frozen_ice":
            # Chilled cyan/dark blue tundra atmosphere
            for y in range(self.height):
                t = y / self.height
                r = int(10 + 20 * t)
                g = int(25 + 40 * t)
                b = int(45 + 65 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))

            horizon_y = int(self.height * 0.72)
            draw.line([(0, horizon_y), (self.width, horizon_y)], fill=(120, 200, 240, 160), width=3)
            # Ice floor texture
            draw.rectangle([(0, horizon_y), (self.width, self.height)], fill=(20, 45, 70, 255))

        elif style == "jungle_forest":
            # Deep mysterious dusk jungle / rainforest atmosphere
            for y in range(self.height):
                t = y / self.height
                # Gradient from dark twilight canopy (near-black green) to misty moss floor
                r = int(8 + 14 * t)
                g = int(22 + 25 * t)
                b = int(18 + 15 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))

            # Distant tree trunks silhouette in background
            rng = random.Random(77)
            for _ in range(12):
                tx = rng.randint(0, self.width)
                tw = rng.randint(25, 60)
                draw.rectangle([tx, 0, tx + tw, int(self.height * 0.76)], fill=(12, 28, 18, 140))

            horizon_y = int(self.height * 0.74)
            # Forest floor
            draw.rectangle([(0, horizon_y), (self.width, self.height)], fill=(15, 32, 18, 255))
            draw.line([(0, horizon_y), (self.width, horizon_y)], fill=(35, 70, 35, 200), width=4)

            # Little procedural grass tufts on ground
            for gx in range(40, self.width, 90):
                draw.line([(gx, horizon_y), (gx - 10, horizon_y - 25)], fill=(40, 85, 40, 220), width=3)
                draw.line([(gx, horizon_y), (gx + 12, horizon_y - 22)], fill=(45, 95, 45, 220), width=3)

        elif style == "ocean_depths":
            # Deep aquatic ocean abyss with water gradient & bubbles
            for y in range(self.height):
                t = y / self.height
                r = int(4 + 10 * t)
                g = int(25 + 45 * t)
                b = int(50 + 60 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))
            # Ocean floor
            floor_y = int(self.height * 0.8)
            draw.rectangle([(0, floor_y), (self.width, self.height)], fill=(5, 18, 30, 255))
            # Rising underwater bubbles
            rng = random.Random(101)
            for _ in range(35):
                bx = rng.randint(0, self.width)
                by = rng.randint(0, floor_y)
                br = rng.randint(3, 10)
                draw.ellipse([bx - br, by - br, bx + br, by + br], outline=(120, 210, 255, 160), width=2)

        elif style == "desert_dunes":
            # Burning arid desert with intense sun haze
            for y in range(self.height):
                t = y / self.height
                r = int(55 + 90 * t)
                g = int(35 + 45 * t)
                b = int(20 + 20 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))
            horizon_y = int(self.height * 0.72)
            # Rolling sand dunes
            draw.rectangle([(0, horizon_y), (self.width, self.height)], fill=(185, 125, 45, 255))
            draw.line([(0, horizon_y), (self.width, horizon_y)], fill=(225, 165, 60, 255), width=4)

        elif style == "neon_city":
            # Cyberpunk future city skyline with neon grids
            for y in range(self.height):
                t = y / self.height
                r = int(12 + 18 * t)
                g = int(8 + 12 * t)
                b = int(28 + 35 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))
            horizon_y = int(self.height * 0.74)
            # Distant skyscrapers
            rng = random.Random(88)
            for _ in range(16):
                bx = rng.randint(0, self.width)
                bw = rng.randint(40, 90)
                bh = rng.randint(150, 420)
                draw.rectangle([bx, horizon_y - bh, bx + bw, horizon_y], fill=(15, 12, 32, 220), outline=(0, 220, 255, 90), width=1)
            # Cyber grid floor
            draw.rectangle([(0, horizon_y), (self.width, self.height)], fill=(10, 8, 22, 255))
            draw.line([(0, horizon_y), (self.width, horizon_y)], fill=(255, 0, 128, 200), width=3)

        elif style == "volcano_lava":
            # Dark apocalyptic smoke sky with smoldering red/orange lava
            for y in range(self.height):
                t = y / self.height
                r = int(35 + 50 * t)
                g = int(12 + 15 * t)
                b = int(10 + 10 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))
            horizon_y = int(self.height * 0.75)
            # Jagged obsidian ground with lava cracks
            draw.rectangle([(0, horizon_y), (self.width, self.height)], fill=(22, 10, 10, 255))
            draw.line([(0, horizon_y), (self.width, horizon_y)], fill=(255, 60, 0, 220), width=4)
            # Glowing lava fissures
            for lx in range(0, self.width, 140):
                draw.line([(lx, horizon_y), (lx + 60, self.height)], fill=(255, 120, 0, 180), width=3)

        elif style == "hospital_lab":
            # High-tech clean medical laboratory with subtle heartbeat monitor grid
            for y in range(self.height):
                t = y / self.height
                r = int(220 + 20 * t)
                g = int(230 + 15 * t)
                b = int(235 + 15 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))
            horizon_y = int(self.height * 0.78)
            draw.rectangle([(0, horizon_y), (self.width, self.height)], fill=(195, 210, 220, 255))
            draw.line([(0, horizon_y), (self.width, horizon_y)], fill=(0, 160, 210, 180), width=3)

        elif style == "cozy_bedroom":
            # Dark dusk bedroom with large signature window and glowing moonlight
            for y in range(self.height):
                t = y / self.height
                r = int(18 + 12 * t)
                g = int(14 + 10 * t)
                b = int(32 + 20 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))
            # Large Signature Window with mullions and sky gradient
            win_w = int(self.width * 0.35)
            win_h = int(self.height * 0.45)
            win_x = int(self.width * 0.58)
            win_y = int(self.height * 0.12)
            # Sky outside window
            draw.rectangle([win_x, win_y, win_x + win_w, win_y + win_h], fill=(35, 45, 80, 255))
            # Distant city skyline outside window
            draw.rectangle([win_x + 20, win_y + win_h - 60, win_x + 90, win_y + win_h], fill=(20, 25, 45, 255))
            draw.rectangle([win_x + 110, win_y + win_h - 90, win_x + 180, win_y + win_h], fill=(22, 28, 50, 255))
            # Window frame & mullions
            draw.rectangle([win_x, win_y, win_x + win_w, win_y + win_h], outline=(70, 75, 110, 255), width=6)
            draw.line([(win_x + win_w // 2, win_y), (win_x + win_w // 2, win_y + win_h)], fill=(70, 75, 110, 255), width=4)
            draw.line([(win_x, win_y + win_h // 2), (win_x + win_w, win_y + win_h // 2)], fill=(70, 75, 110, 255), width=4)
            # Bed frame and mattress
            horizon_y = int(self.height * 0.74)
            bed_x = int(self.width * 0.08)
            bed_w = int(self.width * 0.45)
            bed_h = int(self.height * 0.18)
            draw.rectangle([(0, horizon_y), (self.width, self.height)], fill=(22, 20, 32, 255))
            draw.line([(0, horizon_y), (self.width, horizon_y)], fill=(45, 40, 65, 255), width=3)
            # Bed headboard
            draw.rectangle([bed_x - 15, horizon_y - bed_h - 40, bed_x + 10, horizon_y], fill=(60, 45, 40, 255))
            # Mattress / Duvet (cozy navy/teal blanket)
            draw.rounded_rectangle([bed_x, horizon_y - bed_h, bed_x + bed_w, horizon_y], radius=12, fill=(35, 65, 95, 255), outline=(60, 100, 140, 255), width=3)
            # Soft cream pillow
            draw.ellipse([bed_x + 15, horizon_y - bed_h - 15, bed_x + 95, horizon_y - bed_h + 25], fill=(220, 225, 235, 255))

        elif style == "living_room_couch":
            # Cozy evening living room with couch and TV ambient glow
            for y in range(self.height):
                t = y / self.height
                r = int(22 + 15 * t)
                g = int(18 + 12 * t)
                b = int(35 + 18 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))
            horizon_y = int(self.height * 0.76)
            draw.rectangle([(0, horizon_y), (self.width, self.height)], fill=(28, 22, 35, 255))
            draw.line([(0, horizon_y), (self.width, horizon_y)], fill=(65, 50, 75, 255), width=3)
            # Couch body (Mustard / warm ochre couch)
            couch_x = int(self.width * 0.22)
            couch_w = int(self.width * 0.56)
            couch_h = int(self.height * 0.22)
            # Couch back
            draw.rounded_rectangle([couch_x, horizon_y - couch_h, couch_x + couch_w, horizon_y - 20], radius=18, fill=(160, 110, 45, 255), outline=(100, 70, 25, 255), width=4)
            # Couch seat cushions
            draw.rounded_rectangle([couch_x - 15, horizon_y - int(couch_h * 0.55), couch_x + couch_w + 15, horizon_y], radius=14, fill=(185, 130, 55, 255), outline=(115, 80, 30, 255), width=4)
            # Wall poster / art frame
            draw.rectangle([int(self.width * 0.38), int(self.height * 0.15), int(self.width * 0.62), int(self.height * 0.4)], fill=(40, 35, 60, 255), outline=(90, 80, 120, 255), width=3)

        elif style == "school_classroom":
            # School classroom with green chalkboard and wooden desks
            for y in range(self.height):
                t = y / self.height
                r = int(30 + 15 * t)
                g = int(32 + 18 * t)
                b = int(45 + 20 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))
            # Large Green Chalkboard
            board_w = int(self.width * 0.58)
            board_h = int(self.height * 0.36)
            board_x = int(self.width * 0.21)
            board_y = int(self.height * 0.16)
            draw.rectangle([board_x, board_y, board_x + board_w, board_y + board_h], fill=(25, 65, 45, 255), outline=(120, 85, 55, 255), width=8)
            # Math scribbles on board
            draw.text((board_x + 40, board_y + 35), "DAY 1  ->  DAY 30", fill=(210, 235, 215, 180))
            draw.line([(board_x + 40, board_y + 70), (board_x + board_w - 40, board_y + 70)], fill=(180, 220, 190, 140), width=2)
            horizon_y = int(self.height * 0.74)
            draw.rectangle([(0, horizon_y), (self.width, self.height)], fill=(45, 38, 48, 255))
            draw.line([(0, horizon_y), (self.width, horizon_y)], fill=(85, 75, 90, 255), width=3)

        elif style == "ruins_wasteland":
            # Apocalyptic post-collapse Earth: dramatic crimson/violet dusk with dying sun & ruins
            for y in range(self.height):
                t = y / self.height
                r = int(28 + 65 * t)
                g = int(14 + 18 * t)
                b = int(24 + 12 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))

            # Giant low dying sun on the horizon
            sun_cx = int(self.width * 0.5)
            sun_cy = int(self.height * 0.62)
            sun_r = int(110 * (self.width / 1920.0))
            draw.ellipse([sun_cx - sun_r - 20, sun_cy - sun_r - 20, sun_cx + sun_r + 20, sun_cy + sun_r + 20], fill=(255, 90, 20, 80))
            draw.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r], fill=(255, 175, 45, 230))

            # Crumbling skyscraper ruins silhouette on horizon
            horizon_y = int(self.height * 0.74)
            rng = random.Random(33)
            for _ in range(14):
                rx = rng.randint(0, self.width)
                rw = rng.randint(45, 110)
                rh = rng.randint(80, 280)
                # Jagged broken roof
                draw.rectangle([rx, horizon_y - rh, rx + rw, horizon_y], fill=(18, 12, 22, 240))
                draw.line([(rx, horizon_y - rh), (rx + rw // 2, horizon_y - rh + 20), (rx + rw, horizon_y - rh)], fill=(12, 8, 16, 255), width=3)

            # Desolate cracked ground
            draw.rectangle([(0, horizon_y), (self.width, self.height)], fill=(20, 14, 18, 255))
            draw.line([(0, horizon_y), (self.width, horizon_y)], fill=(85, 35, 25, 255), width=4)
            # Glowing ember / magma cracks
            for cx in range(0, self.width, 160):
                draw.line([(cx, horizon_y), (cx + 50, self.height)], fill=(255, 110, 30, 160), width=3)

        elif style == "city_street":
            # Twilight metropolitan street with illuminated skyscrapers & warm street lamps
            for y in range(self.height):
                t = y / self.height
                r = int(14 + 18 * t)
                g = int(16 + 14 * t)
                b = int(34 + 26 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))

            horizon_y = int(self.height * 0.74)
            # Skyscraper silhouettes with lit window grids
            rng = random.Random(55)
            for i in range(12):
                bx = i * (self.width // 10) - 40
                bw = int(self.width * 0.11)
                bh = rng.randint(220, 480)
                draw.rectangle([bx, horizon_y - bh, bx + bw, horizon_y], fill=(16, 18, 30, 240))
                # Window dots
                for wy in range(horizon_y - bh + 25, horizon_y - 20, 28):
                    for wx in range(bx + 15, bx + bw - 15, 20):
                        if (wx + wy) % 3 == 0:
                            draw.rectangle([wx, wy, wx + 8, wy + 12], fill=(255, 215, 130, 190))

            # Asphalt road & sidewalk curb
            draw.rectangle([(0, horizon_y), (self.width, self.height)], fill=(24, 25, 32, 255))
            draw.line([(0, horizon_y), (self.width, horizon_y)], fill=(60, 65, 80, 255), width=4)
            draw.line([(0, horizon_y + 24), (self.width, horizon_y + 24)], fill=(120, 125, 140, 200), width=2) # curb

            # Street lamp posts with light cones
            for lx in [int(self.width * 0.18), int(self.width * 0.82)]:
                draw.line([(lx, horizon_y), (lx, horizon_y - 280)], fill=(30, 32, 42), width=6)
                draw.line([(lx, horizon_y - 280), (lx + 30, horizon_y - 295)], fill=(30, 32, 42), width=5)
                draw.ellipse([lx + 20, horizon_y - 305, lx + 44, horizon_y - 285], fill=(255, 220, 140, 255))
                # Soft light cone on ground
                draw.polygon([(lx + 32, horizon_y - 285), (lx - 60, horizon_y), (lx + 130, horizon_y)], fill=(255, 220, 140, 35))

        elif style == "webcomic_light":
            bg = Image.new("RGBA", (self.width, self.height), (245, 246, 250, 255))
            draw = ImageDraw.Draw(bg)
            step = 60
            for gx in range(0, self.width, step):
                for gy in range(0, self.height, step):
                    draw.point((gx, gy), fill=(210, 215, 225, 255))
            floor_y = int(self.height * 0.8)
            draw.line([(0, floor_y), (self.width, floor_y)], fill=(200, 205, 215, 255), width=3)

        elif style == "sports_stadium":
            # Grand night stadium with bright floodlights, crowd silhouette and green turf
            bg = Image.new("RGBA", (self.width, self.height))
            draw = ImageDraw.Draw(bg)
            # Sky gradient: dark navy to dusky stadium haze
            for y in range(int(self.height * 0.65)):
                t = y / (self.height * 0.65)
                r = int(12 + 18 * t)
                g = int(16 + 28 * t)
                b = int(32 + 45 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))
            # Distant crowd stands silhouette
            stand_y = int(self.height * 0.52)
            draw.rectangle([(0, stand_y), (self.width, int(self.height * 0.65))], fill=(18, 22, 34, 255))
            for cx in range(0, self.width, 22):
                draw.ellipse([cx, stand_y - 8, cx + 16, stand_y + 8], fill=(28, 34, 50, 255))
            # Huge Floodlight Towers with beams
            for lx in [int(self.width * 0.12), int(self.width * 0.88)]:
                tower_top = int(self.height * 0.18)
                draw.line([(lx, stand_y), (lx, tower_top)], fill=(40, 48, 65, 255), width=7)
                draw.rectangle([(lx - 25, tower_top - 12), (lx + 25, tower_top + 12)], fill=(240, 245, 255, 255))
                # Light beam cone
                draw.polygon([(lx, tower_top), (lx - int(self.width * 0.25), self.height), (lx + int(self.width * 0.25), self.height)], fill=(255, 255, 230, 28))
            # Green Turf Ground
            field_y = int(self.height * 0.65)
            for y in range(field_y, self.height):
                t = (y - field_y) / (self.height - field_y)
                r = int(18 + 14 * t)
                g = int(75 + 40 * t)
                b = int(32 + 20 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))
            # White field boundary lines
            draw.line([(0, field_y), (self.width, field_y)], fill=(230, 245, 230, 220), width=4)
            draw.line([(int(self.width * 0.5), field_y), (int(self.width * 0.5), self.height)], fill=(230, 245, 230, 180), width=3)
            # Center circle arc
            draw.arc([int(self.width * 0.35), field_y - 80, int(self.width * 0.65), field_y + 260], 0, 180, fill=(230, 245, 230, 180), width=3)

        elif style == "running_track":
            # Vibrant Red Tartan Athletic Sprint Track with white lane markings
            bg = Image.new("RGBA", (self.width, self.height))
            draw = ImageDraw.Draw(bg)
            # Sunny outdoor sky
            sky_h = int(self.height * 0.55)
            for y in range(sky_h):
                t = y / sky_h
                r = int(90 + 80 * t)
                g = int(160 + 60 * t)
                b = int(240 + 15 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))
            # Distant lush green grass field & trees
            draw.rectangle([(0, sky_h - 40), (self.width, sky_h)], fill=(45, 115, 55, 255))
            for tx in range(0, self.width, 90):
                draw.ellipse([tx, sky_h - 75, tx + 80, sky_h - 15], fill=(35, 95, 45, 240))
            # Red Tartan Athletic Track
            for y in range(sky_h, self.height):
                t = (y - sky_h) / (self.height - sky_h)
                r = int(175 + 35 * t)
                g = int(45 + 20 * t)
                b = int(40 + 15 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))
            # Sprint Track Lanes (perspective lines)
            for offset in [-0.35, -0.15, 0.05, 0.25, 0.45]:
                x_top = int(self.width * (0.5 + offset * 0.4))
                x_bot = int(self.width * (0.5 + offset * 1.3))
                draw.line([(x_top, sky_h), (x_bot, self.height)], fill=(255, 255, 255, 220), width=4)

        elif style == "gym_fitness":
            # High-energy Fitness Center & Weight Room
            bg = Image.new("RGBA", (self.width, self.height), (22, 24, 30, 255))
            draw = ImageDraw.Draw(bg)
            # Dark industrial walls with motivational neon stripe
            wall_h = int(self.height * 0.70)
            draw.rectangle([(0, 0), (self.width, wall_h)], fill=(16, 18, 22, 255))
            # Neon energy stripe along wall
            draw.line([(0, int(wall_h * 0.45)), (self.width, int(wall_h * 0.45))], fill=(255, 80, 20, 230), width=4)
            # Wall mirror with reflections
            mirror_x1 = int(self.width * 0.2)
            mirror_x2 = int(self.width * 0.8)
            draw.rectangle([(mirror_x1, int(wall_h * 0.15)), (mirror_x2, int(wall_h * 0.85))], fill=(32, 38, 48, 200), outline=(50, 60, 75), width=3)
            # Overhead industrial hanging lamps
            for lx in [int(self.width * 0.3), int(self.width * 0.7)]:
                draw.line([(lx, 0), (lx, 100)], fill=(70, 75, 85), width=3)
                draw.ellipse([lx - 30, 95, lx + 30, 120], fill=(240, 245, 255, 255))
                draw.polygon([(lx, 110), (lx - 180, wall_h), (lx + 180, wall_h)], fill=(255, 240, 200, 22))
            # Heavy Rubber Gym Mat Floor
            draw.rectangle([(0, wall_h), (self.width, self.height)], fill=(12, 13, 16, 255))
            draw.line([(0, wall_h), (self.width, wall_h)], fill=(60, 65, 80, 255), width=4)
            # Dumbbell rack silhouette in background
            rack_y = wall_h - 50
            draw.rectangle([(int(self.width * 0.05), rack_y), (int(self.width * 0.28), wall_h)], fill=(35, 40, 50, 255))
            for dx in range(int(self.width * 0.06), int(self.width * 0.26), 35):
                draw.rectangle([(dx, rack_y - 12), (dx + 25, rack_y + 8)], fill=(65, 75, 90, 255))

        elif style == "outdoor_park":
            # Fresh green morning park with trees, walking trail, and warm sunlight
            bg = Image.new("RGBA", (self.width, self.height))
            draw = ImageDraw.Draw(bg)
            # Morning sky
            sky_h = int(self.height * 0.58)
            for y in range(sky_h):
                t = y / sky_h
                r = int(120 + 90 * t)
                g = int(180 + 55 * t)
                b = int(245 + 10 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))
            # Morning Sun
            draw.ellipse([int(self.width * 0.8), int(sky_h * 0.2), int(self.width * 0.8) + 110, int(sky_h * 0.2) + 110], fill=(255, 235, 140, 240))
            # Rolling green hills
            draw.chord([(0, sky_h - 120), (self.width, sky_h + 80)], 0, 180, fill=(45, 125, 60, 255))
            # Shade trees
            for tx in [int(self.width * 0.15), int(self.width * 0.72)]:
                draw.rectangle([(tx - 12, sky_h - 60), (tx + 12, sky_h + 30)], fill=(75, 48, 28, 255))
                draw.ellipse([tx - 70, sky_h - 190, tx + 70, sky_h - 50], fill=(35, 110, 48, 245))
            # Grassy ground foreground
            ground_y = int(self.height * 0.68)
            draw.rectangle([(0, ground_y), (self.width, self.height)], fill=(55, 145, 70, 255))
            # Winding park jogging trail
            draw.polygon([
                (int(self.width * 0.45), ground_y), (int(self.width * 0.55), ground_y),
                (int(self.width * 0.75), self.height), (int(self.width * 0.35), self.height)
            ], fill=(205, 185, 145, 230))

        elif style == "office_workspace":
            # Modern Tech / Corporate Office with floor-to-ceiling glass window & city view
            bg = Image.new("RGBA", (self.width, self.height))
            draw = ImageDraw.Draw(bg)
            # Window city view
            win_y = int(self.height * 0.65)
            for y in range(win_y):
                t = y / win_y
                r = int(140 + 70 * t)
                g = int(185 + 45 * t)
                b = int(235 + 20 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))
            # Distant skyscrapers
            for bx, bw, bh in [(80, 120, 240), (240, 160, 310), (450, 140, 200), (700, 180, 340), (1000, 150, 260), (1300, 200, 320)]:
                draw.rectangle([(bx, win_y - bh), (bx + bw, win_y)], fill=(110, 130, 160, 240))
            # Window frame divider
            draw.line([(0, win_y), (self.width, win_y)], fill=(50, 55, 70, 255), width=6)
            draw.line([(int(self.width * 0.5), 0), (int(self.width * 0.5), win_y)], fill=(50, 55, 70, 255), width=6)
            # Modern wooden floor
            for y in range(win_y, self.height):
                t = (y - win_y) / (self.height - win_y)
                r = int(130 + 35 * t)
                g = int(90 + 25 * t)
                b = int(60 + 18 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))
            # Minimalist wooden desk
            desk_y = int(self.height * 0.75)
            draw.rectangle([(int(self.width * 0.25), desk_y), (int(self.width * 0.75), desk_y + 20)], fill=(75, 45, 28, 255))
            draw.rectangle([(int(self.width * 0.28), desk_y + 20), (int(self.width * 0.30), self.height)], fill=(45, 30, 20, 255))
            draw.rectangle([(int(self.width * 0.70), desk_y + 20), (int(self.width * 0.72), self.height)], fill=(45, 30, 20, 255))

        elif style == "kitchen_cooking":
            # Warm domestic culinary kitchen
            bg = Image.new("RGBA", (self.width, self.height), (245, 240, 230, 255))
            draw = ImageDraw.Draw(bg)
            # Subway tile wall
            counter_y = int(self.height * 0.70)
            for ty in range(0, counter_y, 40):
                draw.line([(0, ty), (self.width, ty)], fill=(225, 218, 205, 255), width=1)
            # Upper wooden kitchen cabinets
            draw.rectangle([(0, 0), (self.width, int(self.height * 0.22))], fill=(110, 75, 50, 255))
            for cx in range(0, self.width, 240):
                draw.line([(cx, 0), (cx, int(self.height * 0.22))], fill=(80, 50, 32, 255), width=3)
            # Kitchen Countertop
            draw.rectangle([(0, counter_y), (self.width, counter_y + 35)], fill=(40, 42, 48, 255))
            # Lower cabinets & tile floor
            draw.rectangle([(0, counter_y + 35), (self.width, self.height)], fill=(130, 90, 60, 255))

        elif style == "library_books":
            # Scholarly library packed with towering bookshelves
            bg = Image.new("RGBA", (self.width, self.height), (28, 20, 16, 255))
            draw = ImageDraw.Draw(bg)
            floor_y = int(self.height * 0.78)
            # Massive wooden bookshelves
            shelf_h = floor_y // 4
            for s_idx in range(4):
                sy = s_idx * shelf_h
                draw.line([(0, sy), (self.width, sy)], fill=(120, 80, 50, 255), width=8)
                # Colorful book spines
                rng = random.Random(s_idx * 17)
                bx = 20
                while bx < self.width - 40:
                    bw = rng.randint(22, 50)
                    bh = rng.randint(int(shelf_h * 0.65), int(shelf_h * 0.95))
                    b_col = rng.choice([(140, 40, 40), (40, 80, 140), (40, 120, 60), (180, 130, 40), (90, 60, 110)])
                    draw.rectangle([(bx, sy + shelf_h - bh), (bx + bw, sy + shelf_h)], fill=b_col)
                    bx += bw + 3
            # Library Floor
            draw.rectangle([(0, floor_y), (self.width, self.height)], fill=(55, 38, 28, 255))
            draw.line([(0, floor_y), (self.width, floor_y)], fill=(140, 95, 60, 255), width=4)

        elif style == "bank_vault":
            # High-security steel bank vault with golden treasures
            bg = Image.new("RGBA", (self.width, self.height), (24, 28, 35, 255))
            draw = ImageDraw.Draw(bg)
            floor_y = int(self.height * 0.75)
            # Steel panel walls with rivets
            for rx in range(0, self.width, 180):
                draw.line([(rx, 0), (rx, floor_y)], fill=(45, 52, 65, 255), width=2)
            # Massive circular steel vault door
            door_cx = int(self.width * 0.5)
            door_cy = int(self.height * 0.42)
            door_r = int(self.height * 0.32)
            draw.ellipse([door_cx - door_r, door_cy - door_r, door_cx + door_r, door_cy + door_r], fill=(70, 80, 95, 255), outline=(140, 155, 175), width=8)
            draw.ellipse([door_cx - int(door_r * 0.7), door_cy - int(door_r * 0.7), door_cx + int(door_r * 0.7), door_cy + int(door_r * 0.7)], fill=(50, 58, 70, 255))
            # Vault lock wheel
            draw.ellipse([door_cx - 45, door_cy - 45, door_cx + 45, door_cy + 45], fill=(210, 175, 50, 255))
            # Polished steel floor with golden sheen
            draw.rectangle([(0, floor_y), (self.width, self.height)], fill=(32, 36, 44, 255))
            draw.line([(0, floor_y), (self.width, floor_y)], fill=(210, 175, 50, 200), width=3)

        elif style == "mountain_peak":
            # Dramatic mountain summit above clouds under alpine sunrise
            bg = Image.new("RGBA", (self.width, self.height))
            draw = ImageDraw.Draw(bg)
            # Sunrise sky
            for y in range(int(self.height * 0.65)):
                t = y / (self.height * 0.65)
                r = int(235 - 90 * t)
                g = int(140 - 20 * t)
                b = int(120 + 70 * t)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))
            # Majestic mountain peaks
            draw.polygon([(0, int(self.height * 0.65)), (int(self.width * 0.35), int(self.height * 0.25)), (int(self.width * 0.7), int(self.height * 0.65))], fill=(60, 68, 82, 255))
            # Snow cap
            draw.polygon([(int(self.width * 0.28), int(self.height * 0.33)), (int(self.width * 0.35), int(self.height * 0.25)), (int(self.width * 0.42), int(self.height * 0.33))], fill=(240, 245, 255, 255))
            # Foreground rocky ridge
            draw.polygon([(0, int(self.height * 0.72)), (int(self.width * 0.6), int(self.height * 0.58)), (self.width, int(self.height * 0.70)), (self.width, self.height), (0, self.height)], fill=(35, 40, 48, 255))

        elif style == "tech_server_room":
            # Futuristic cyber datacenter with pulsing server racks
            bg = Image.new("RGBA", (self.width, self.height), (10, 12, 18, 255))
            draw = ImageDraw.Draw(bg)
            floor_y = int(self.height * 0.76)
            # Server rack corridors
            for rx in range(40, self.width, 160):
                draw.rectangle([(rx, 60), (rx + 120, floor_y)], fill=(20, 25, 36, 255), outline=(35, 45, 65), width=2)
                # LED blinking status lights
                for ly in range(90, floor_y - 20, 30):
                    draw.ellipse([rx + 18, ly, rx + 24, ly + 6], fill=(0, 240, 140, 255))
                    draw.ellipse([rx + 36, ly, rx + 42, ly + 6], fill=(40, 180, 255, 255))
            # Raised datacenter floor tiles
            draw.rectangle([(0, floor_y), (self.width, self.height)], fill=(16, 20, 28, 255))
            draw.line([(0, floor_y), (self.width, floor_y)], fill=(0, 220, 255, 180), width=3)

        else:
            bg = Image.new("RGBA", (self.width, self.height), (18, 19, 25, 255))

        return bg

    def draw_prop(
        self,
        img: Image.Image,
        prop_name: str,
        cx: int,
        cy: int,
        scale: float = 1.0,
        rotation: float = 0.0
    ):
        """Draws procedural props (Sun, Vanished Sun, Earth, Frozen Earth, Moon, Thermometer, Clock, Atom)."""
        draw = ImageDraw.Draw(img)
        s = scale

        if prop_name == "sun":
            r = int(105 * s)
            # Radiant corona rays
            for angle_deg in range(0, 360, 30):
                rad = math.radians(angle_deg)
                x1 = cx + math.cos(rad) * (r + 10)
                y1 = cy + math.sin(rad) * (r + 10)
                x2 = cx + math.cos(rad) * (r + 38)
                y2 = cy + math.sin(rad) * (r + 38)
                draw.line([(x1, y1), (x2, y2)], fill=(255, 180, 20), width=max(3, int(6 * s)))
            # Outer glow
            draw.ellipse([cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12], fill=(255, 150, 0, 90))
            # Core
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 210, 30), outline=(230, 100, 10), width=5)

        elif prop_name == "vanished_sun":
            # Dotted disappearing outline with a red cross or question
            r = int(95 * s)
            for angle_deg in range(0, 360, 15):
                rad = math.radians(angle_deg)
                px = cx + math.cos(rad) * r
                py = cy + math.sin(rad) * r
                draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(120, 120, 140))
            # Ghost question mark
            draw.text((cx - 15, cy - 35), "?", fill=(180, 180, 200), stroke_width=3, stroke_fill=(30, 30, 40))

        elif prop_name == "earth":
            r = int(90 * s)
            draw.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8], fill=(60, 140, 255, 80))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(40, 110, 230), outline=(20, 40, 80), width=4)
            draw.ellipse([cx - int(r*0.6), cy - int(r*0.5), cx + int(r*0.2), cy + int(r*0.1)], fill=(70, 180, 90))
            draw.ellipse([cx + int(r*0.1), cy - int(r*0.7), cx + int(r*0.7), cy - int(r*0.2)], fill=(70, 180, 90))
            draw.ellipse([cx - int(r*0.2), cy + int(r*0.2), cx + int(r*0.5), cy + int(r*0.7)], fill=(70, 180, 90))

        elif prop_name == "frozen_earth":
            r = int(90 * s)
            # Icy white and cyan frozen sphere
            draw.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8], fill=(160, 230, 255, 80))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(210, 240, 255), outline=(100, 160, 210), width=5)
            # Glaciers and frozen continents
            draw.ellipse([cx - int(r*0.6), cy - int(r*0.5), cx + int(r*0.2), cy + int(r*0.1)], fill=(150, 210, 240))
            draw.ellipse([cx + int(r*0.1), cy - int(r*0.7), cx + int(r*0.7), cy - int(r*0.2)], fill=(150, 210, 240))
            draw.ellipse([cx - int(r*0.2), cy + int(r*0.2), cx + int(r*0.5), cy + int(r*0.7)], fill=(150, 210, 240))

        elif prop_name == "thermometer":
            # Tall vertical glass thermometer dropping into negative degrees
            tw = int(32 * s)
            th = int(180 * s)
            top_y = cy - th // 2
            bot_y = cy + th // 2

            # Glass body
            draw.rounded_rectangle([cx - tw // 2, top_y, cx + tw // 2, bot_y - 20], radius=15, fill=(240, 245, 250), outline=(40, 45, 55), width=4)
            # Bulb at bottom
            bulb_r = int(30 * s)
            draw.ellipse([cx - bulb_r, bot_y - bulb_r, cx + bulb_r, bot_y + bulb_r], fill=(60, 140, 240), outline=(40, 45, 55), width=4)
            # Blue freezing mercury level
            mercury_h = int(50 * s)
            draw.rectangle([cx - tw // 4, bot_y - 20 - mercury_h, cx + tw // 4, bot_y - 20], fill=(60, 140, 240))
            # Minus sign / degree text
            draw.text((cx + tw // 2 + 8, bot_y - 60), "-40°C", fill=(80, 200, 255), stroke_width=3, stroke_fill=(10, 10, 20))

        elif prop_name == "moon":
            r = int(75 * s)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 220, 230), outline=(100, 100, 120), width=4)
            for dx, dy, cr in [(-25, -20, 14), (20, -15, 18), (-10, 25, 20), (30, 20, 10)]:
                draw.ellipse([cx + int(dx*s) - int(cr*s), cy + int(dy*s) - int(cr*s),
                              cx + int(dx*s) + int(cr*s), cy + int(dy*s) + int(cr*s)],
                             fill=(180, 180, 195))

        elif prop_name == "clock":
            r = int(65 * s)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255), outline=(30, 30, 40), width=5)
            draw.line([(cx, cy - r + 8), (cx, cy - r + 20)], fill=(30, 30, 40), width=4)
            draw.line([(cx, cy + r - 8), (cx, cy + r - 20)], fill=(30, 30, 40), width=4)
            draw.line([(cx - r + 8, cy), (cx - r + 20, cy)], fill=(30, 30, 40), width=4)
            draw.line([(cx + r - 8, cy), (cx + r - 20, cy)], fill=(30, 30, 40), width=4)
            draw.line([(cx, cy), (cx + int(28 * s), cy - int(10 * s))], fill=(220, 40, 40), width=4)
            draw.line([(cx, cy), (cx - int(15 * s), cy - int(35 * s))], fill=(30, 30, 40), width=5)
            draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(30, 30, 40))

        elif prop_name == "tree":
            # Stylized tall jungle tree with leafy canopy reaching ground
            trunk_w = int(40 * s)
            trunk_h = int(380 * s)
            top_y = cy - int(120 * s)
            base_y = top_y + trunk_h
            # Trunk
            draw.rectangle([cx - trunk_w // 2, top_y + 40, cx + trunk_w // 2, base_y], fill=(70, 45, 25), outline=(35, 20, 10), width=3)
            # Foliage clusters (3 overlapping dark green circles)
            foliage_r = int(110 * s)
            draw.ellipse([cx - foliage_r - 20, top_y - 20, cx + 30, top_y + foliage_r + 20], fill=(25, 80, 35), outline=(15, 45, 20), width=4)
            draw.ellipse([cx - 20, top_y - 35, cx + foliage_r + 30, top_y + foliage_r + 15], fill=(35, 100, 45), outline=(15, 45, 20), width=4)
            draw.ellipse([cx - foliage_r // 2 - 15, top_y - foliage_r - 15, cx + foliage_r // 2 + 15, top_y + 15], fill=(45, 120, 55), outline=(20, 55, 25), width=4)

        elif prop_name == "campfire":
            # Burning survival campfire on wooden logs
            # Cross logs
            log_w = int(70 * s)
            draw.line([(cx - log_w, cy + 30), (cx + log_w, cy + 45)], fill=(90, 50, 20), width=max(4, int(10 * s)))
            draw.line([(cx - log_w + 10, cy + 45), (cx + log_w - 10, cy + 30)], fill=(75, 40, 15), width=max(4, int(10 * s)))
            # Outer flame
            flame_r = int(50 * s)
            draw.ellipse([cx - flame_r, cy - flame_r + 10, cx + flame_r, cy + flame_r + 25], fill=(255, 100, 0, 210))
            # Inner core flame
            core_r = int(30 * s)
            draw.ellipse([cx - core_r, cy - core_r + 20, cx + core_r, cy + core_r + 25], fill=(255, 220, 40, 240))
            # Smoke puff above
            draw.ellipse([cx - 15, cy - flame_r - 25, cx + 15, cy - flame_r - 5], fill=(120, 120, 120, 120))
            draw.ellipse([cx - 10, cy - flame_r - 55, cx + 25, cy - flame_r - 30], fill=(140, 140, 140, 90))

        elif prop_name == "compass":
            r = int(70 * s)
            # Gold/brass outer casing
            draw.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6], fill=(210, 160, 40), outline=(140, 100, 20), width=4)
            # White dial face
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 245, 245), outline=(50, 50, 50), width=3)
            # North/South needle
            needle_len = int(50 * s)
            # North (Red triangle)
            draw.polygon([(cx, cy - needle_len), (cx - 10, cy), (cx + 10, cy)], fill=(220, 35, 35))
            # South (Blue/Dark triangle)
            draw.polygon([(cx, cy + needle_len), (cx - 10, cy), (cx + 10, cy)], fill=(50, 60, 80))
            # Center pin
            draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(210, 160, 40), outline=(50, 50, 50), width=2)
            # N letter
            draw.text((cx - 6, cy - r + 8), "N", fill=(200, 30, 30), stroke_width=2, stroke_fill=(255, 255, 255))

        elif prop_name == "water_drop":
            # Warning water drop / flask
            r = int(55 * s)
            draw.ellipse([cx - r, cy - r + 15, cx + r, cy + r + 25], fill=(45, 140, 245), outline=(20, 80, 170), width=4)
            draw.polygon([(cx, cy - r - 20), (cx - r + 8, cy + 5), (cx + r - 8, cy + 5)], fill=(45, 140, 245))
            # Danger skull or exclamation mark inside water
            draw.text((cx - 8, cy - 10), "!", fill=(255, 255, 255), stroke_width=3, stroke_fill=(180, 20, 20))

        elif prop_name == "robot_ai":
            # Futuristic AI cyborg head
            w = int(120 * s)
            h = int(110 * s)
            # Antenna
            draw.line([(cx, cy - h // 2), (cx, cy - h // 2 - int(35 * s))], fill=(160, 170, 185), width=4)
            draw.ellipse([cx - 8, cy - h // 2 - int(45 * s), cx + 8, cy - h // 2 - int(29 * s)], fill=(255, 40, 40))
            # Head chassis
            draw.rounded_rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], radius=15, fill=(190, 200, 215), outline=(40, 50, 65), width=4)
            # Glowing cyan visor
            draw.rounded_rectangle([cx - int(w * 0.4), cy - int(h * 0.2), cx + int(w * 0.4), cy + int(h * 0.15)], radius=8, fill=(0, 240, 255), outline=(0, 140, 180), width=2)
            # Grid mouth / speaker grill
            for mx in range(cx - 25, cx + 30, 12):
                draw.line([(mx, cy + int(h * 0.3)), (mx, cy + int(h * 0.42))], fill=(60, 70, 85), width=2)

        elif prop_name == "dinosaur":
            # Stylized prehistoric T-Rex skull / predator
            r = int(90 * s)
            # Dark green head
            draw.ellipse([cx - r, cy - int(r * 0.7), cx + r, cy + int(r * 0.6)], fill=(45, 90, 55), outline=(20, 50, 30), width=4)
            # Open jaws snout
            draw.polygon([(cx - r, cy), (cx - int(r * 1.5), cy - 20), (cx - int(r * 1.4), cy + 30)], fill=(40, 80, 50), outline=(20, 50, 30))
            # Sharp white teeth
            for tx in range(cx - int(r * 1.4), cx - int(r * 0.9), 16):
                draw.polygon([(tx, cy - 8), (tx + 8, cy - 8), (tx + 4, cy + 4)], fill=(255, 255, 255))
            # Glowing yellow eye
            draw.ellipse([cx - 20, cy - 35, cx - 6, cy - 21], fill=(255, 220, 0), outline=(20, 50, 30), width=2)

        elif prop_name == "money_bag":
            # Bulging dollar money sack with spilled gold coins
            r = int(75 * s)
            # Sack body
            draw.ellipse([cx - r, cy - int(r * 0.4), cx + r, cy + r], fill=(225, 195, 130), outline=(130, 95, 45), width=4)
            # Tied neck
            draw.polygon([(cx - 25, cy - int(r * 0.3)), (cx + 25, cy - int(r * 0.3)), (cx, cy - int(r * 0.8))], fill=(210, 180, 115), outline=(130, 95, 45))
            draw.line([(cx - 28, cy - int(r * 0.3)), (cx + 28, cy - int(r * 0.3))], fill=(160, 40, 30), width=6)
            # Big Green Dollar Sign
            draw.text((cx - 16, cy + 5), "$", fill=(25, 135, 45), stroke_width=3, stroke_fill=(255, 255, 255))
            # Gold coins on ground
            for ox in [-40, -15, 20, 45]:
                draw.ellipse([cx + ox - 12, cy + r - 8, cx + ox + 12, cy + r + 12], fill=(255, 215, 0), outline=(180, 130, 0), width=2)

        elif prop_name == "skull_danger":
            # Fatal danger skull with crossbones
            r = int(65 * s)
            # Crossbones behind
            draw.line([(cx - r - 20, cy - r), (cx + r + 20, cy + r)], fill=(220, 220, 230), width=max(4, int(10 * s)))
            draw.line([(cx - r - 20, cy + r), (cx + r + 20, cy - r)], fill=(220, 220, 230), width=max(4, int(10 * s)))
            # Skull cranium
            draw.ellipse([cx - r, cy - r, cx + r, cy + int(r * 0.4)], fill=(245, 245, 250), outline=(40, 40, 50), width=4)
            # Teeth / jaw
            draw.rectangle([cx - int(r * 0.5), cy + int(r * 0.2), cx + int(r * 0.5), cy + int(r * 0.8)], fill=(245, 245, 250), outline=(40, 40, 50), width=3)
            # Hollow dark eye sockets
            draw.ellipse([cx - int(r * 0.55), cy - int(r * 0.25), cx - int(r * 0.15), cy + int(r * 0.15)], fill=(30, 30, 40))
            draw.ellipse([cx + int(r * 0.15), cy - int(r * 0.25), cx + int(r * 0.55), cy + int(r * 0.15)], fill=(30, 30, 40))

        elif prop_name == "dna_strand":
            # Biological double-helix DNA
            h = int(180 * s)
            for dy in range(-h // 2, h // 2, 22):
                phase = dy * 0.05
                x_left = cx + int(math.sin(phase) * 50 * s)
                x_right = cx + int(math.sin(phase + math.pi) * 50 * s)
                # Connecting bond
                draw.line([(x_left, cy + dy), (x_right, cy + dy)], fill=(180, 180, 200), width=2)
                # Cyan and Magenta base spheres
                draw.ellipse([x_left - 8, cy + dy - 8, x_left + 8, cy + dy + 8], fill=(0, 230, 255), outline=(0, 120, 160), width=2)
                draw.ellipse([x_right - 8, cy + dy - 8, x_right + 8, cy + dy + 8], fill=(255, 40, 160), outline=(160, 20, 90), width=2)

        elif prop_name == "volcano":
            # Erupting volcano with red/orange lava
            vw = int(140 * s)
            vh = int(110 * s)
            # Mountain cone
            draw.polygon([(cx - vw, cy + vh), (cx + vw, cy + vh), (cx + int(vw * 0.35), cy - vh), (cx - int(vw * 0.35), cy - vh)], fill=(65, 45, 40), outline=(30, 20, 20), width=4)
            # Magma eruption burst
            draw.ellipse([cx - int(vw * 0.45), cy - vh - 30, cx + int(vw * 0.45), cy - vh + 15], fill=(255, 60, 0))
            draw.ellipse([cx - int(vw * 0.25), cy - vh - 20, cx + int(vw * 0.25), cy - vh + 5], fill=(255, 210, 0))
            # Dripping lava lines
            draw.line([(cx - 15, cy - vh + 5), (cx - 25, cy + 20)], fill=(255, 80, 0), width=max(2, int(4 * s)))
            draw.line([(cx + 10, cy - vh + 5), (cx + 35, cy + 30)], fill=(255, 140, 0), width=max(2, int(4 * s)))

        elif prop_name == "phone_device":
            # Modern smartphone with notification pill
            pw = int(60 * s)
            ph = int(120 * s)
            draw.rounded_rectangle([cx - pw, cy - ph, cx + pw, cy + ph], radius=16, fill=(30, 35, 45), outline=(15, 20, 25), width=4)
            # Screen
            draw.rounded_rectangle([cx - pw + 6, cy - ph + 12, cx + pw - 6, cy + ph - 12], radius=10, fill=(235, 240, 250))
            # Red alert dot / notification badge
            draw.ellipse([cx + pw - 18, cy - ph + 18, cx + pw + 2, cy - ph + 38], fill=(255, 30, 50))

        elif prop_name == "alarm_clock":
            # Bedside glowing digital alarm clock
            cw = int(75 * s)
            ch = int(50 * s)
            draw.rounded_rectangle([cx - cw, cy - ch, cx + cw, cy + ch], radius=8, fill=(20, 22, 30), outline=(50, 55, 70), width=3)
            # Digital LED red glowing time 07:00
            draw.text((cx - 38, cy - 14), "07:00", fill=(255, 45, 60))
            # Ring bells on top
            draw.ellipse([cx - cw + 5, cy - ch - 12, cx - cw + 25, cy - ch + 8], fill=(160, 165, 180), outline=(40, 45, 55), width=2)
            draw.ellipse([cx + cw - 25, cy - ch - 12, cx + cw - 5, cy - ch + 8], fill=(160, 165, 180), outline=(40, 45, 55), width=2)

        elif prop_name == "pizza_box":
            # Pizza delivery box and slice
            bw = int(80 * s)
            bh = int(35 * s)
            draw.rectangle([cx - bw, cy - bh, cx + bw, cy + bh], fill=(225, 210, 185), outline=(140, 110, 75), width=3)
            draw.text((cx - 25, cy - 10), "PIZZA", fill=(180, 40, 30))
            # Floating cheesy pizza slice
            draw.polygon([(cx + bw + 10, cy - 20), (cx + bw + 60, cy - 40), (cx + bw + 55, cy + 15)], fill=(245, 190, 45), outline=(180, 110, 20), width=2)

        elif prop_name == "vending_machine":
            # School / office snack vending machine
            vw = int(70 * s)
            vh = int(140 * s)
            draw.rounded_rectangle([cx - vw, cy - vh, cx + vw, cy + vh], radius=6, fill=(45, 50, 65), outline=(20, 25, 35), width=4)
            # Glass display area with snacks
            draw.rectangle([cx - vw + 10, cy - vh + 15, cx + vw - 10, cy + 10], fill=(20, 25, 38))
            draw.text((cx - 28, cy - vh + 30), "SNACKS", fill=(255, 210, 0))
            # Coin slot & keypad
            draw.rectangle([cx - vw + 15, cy + 30, cx + vw - 15, cy + 60], fill=(25, 30, 40))
            draw.text((cx - 20, cy + 35), "84 ITEMS", fill=(0, 230, 120))

        elif prop_name == "question_mark":
            draw.text((cx - 20, cy - 40), "?", fill=(255, 210, 0), stroke_width=4, stroke_fill=(20, 20, 20))

        elif prop_name in ["dumbbell", "weights"]:
            # Hexagonal fitness dumbbell with knurled bar
            dw = int(55 * s)
            dh = int(35 * s)
            # Left weight plate
            draw.polygon([(cx - dw - 20, cy - dh), (cx - dw, cy - dh), (cx - dw + 10, cy), (cx - dw, cy + dh), (cx - dw - 20, cy + dh), (cx - dw - 30, cy)], fill=(45, 50, 60), outline=(20, 22, 28), width=3)
            # Right weight plate
            draw.polygon([(cx + dw, cy - dh), (cx + dw + 20, cy - dh), (cx + dw + 30, cy), (cx + dw + 20, cy + dh), (cx + dw, cy + dh), (cx + dw - 10, cy)], fill=(45, 50, 60), outline=(20, 22, 28), width=3)
            # Center metal barbell grip
            draw.rectangle([(cx - dw, cy - 8), (cx + dw, cy + 8)], fill=(180, 190, 205), outline=(70, 75, 85), width=2)

        elif prop_name in ["sports_ball", "football", "basketball", "soccer"]:
            # High-visibility athletic sports ball
            r = int(55 * s)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255), outline=(25, 28, 35), width=4)
            # Pentagonal classic soccer seam pattern
            draw.polygon([
                (cx, cy - int(18 * s)), (cx + int(18 * s), cy - int(5 * s)),
                (cx + int(11 * s), cy + int(16 * s)), (cx - int(11 * s), cy + int(16 * s)),
                (cx - int(18 * s), cy - int(5 * s))
            ], fill=(25, 28, 35))
            draw.line([(cx, cy - int(18 * s)), (cx, cy - r)], fill=(25, 28, 35), width=3)
            draw.line([(cx + int(18 * s), cy - int(5 * s)), (cx + int(r * 0.9), cy - int(r * 0.3))], fill=(25, 28, 35), width=3)
            draw.line([(cx - int(18 * s), cy - int(5 * s)), (cx - int(r * 0.9), cy - int(r * 0.3))], fill=(25, 28, 35), width=3)

        elif prop_name in ["trophy_cup", "trophy", "gold_trophy"]:
            # Gleaming golden championship trophy
            tw = int(45 * s)
            th = int(70 * s)
            # Pedestal Base
            draw.rectangle([(cx - tw, cy + th - 20), (cx + tw, cy + th)], fill=(35, 38, 48), outline=(15, 18, 24), width=3)
            draw.rectangle([(cx - int(tw * 0.6), cy + th - 35), (cx + int(tw * 0.6), cy + th - 20)], fill=(210, 175, 40))
            # Cup Stem
            draw.rectangle([(cx - 8, cy + int(th * 0.1)), (cx + 8, cy + th - 35)], fill=(230, 190, 45))
            # Golden Cup Body
            draw.polygon([(cx - tw, cy - th + 20), (cx + tw, cy - th + 20), (cx + int(tw * 0.6), cy + int(th * 0.1)), (cx - int(tw * 0.6), cy + int(th * 0.1))], fill=(255, 215, 50), outline=(200, 150, 20), width=3)
            # Cup Handles
            draw.arc([cx - tw - 25, cy - th + 25, cx - tw + 15, cy - 5], 90, 270, fill=(210, 160, 30), width=5)
            draw.arc([cx + tw - 15, cy - th + 25, cx + tw + 25, cy - 5], 270, 90, fill=(210, 160, 30), width=5)
            # Center Victory Star
            draw.ellipse([cx - 10, cy - th + 45, cx + 10, cy - th + 65], fill=(255, 245, 150))

        elif prop_name in ["running_shoes", "shoes", "sneakers"]:
            # Aerodynamic running sneaker
            sw = int(65 * s)
            sh = int(30 * s)
            # Sole
            draw.rounded_rectangle([cx - sw, cy + sh - 12, cx + sw, cy + sh], radius=6, fill=(245, 248, 255), outline=(30, 35, 45), width=2)
            # Shoe Upper
            draw.polygon([(cx - sw + 10, cy + sh - 12), (cx - sw + 25, cy - sh + 5), (cx + 10, cy - sh + 15), (cx + sw - 5, cy + sh - 12)], fill=(255, 75, 50), outline=(180, 40, 25), width=3)
            # Dynamic swoosh accent
            draw.line([(cx - sw + 30, cy + 5), (cx, cy - 5), (cx + sw - 20, cy + 2)], fill=(255, 255, 255), width=4)

        elif prop_name in ["heart_pulse", "heart", "health"]:
            # Glowing vibrant heart with ECG pulse line
            hr = int(45 * s)
            draw.ellipse([cx - hr, cy - hr, cx, cy], fill=(255, 45, 75))
            draw.ellipse([cx, cy - hr, cx + hr, cy], fill=(255, 45, 75))
            draw.polygon([(cx - hr + 4, cy - int(hr * 0.3)), (cx + hr - 4, cy - int(hr * 0.3)), (cx, cy + hr)], fill=(255, 45, 75))
            # Glowing pulse trace
            draw.line([(cx - hr - 30, cy), (cx - int(hr * 0.4), cy), (cx - int(hr * 0.1), cy - 25), (cx + int(hr * 0.2), cy + 25), (cx + int(hr * 0.5), cy), (cx + hr + 30, cy)], fill=(255, 255, 255), width=4)

        elif prop_name in ["brain_glow", "brain", "mind"]:
            # Glowing intellect brain icon
            br = int(50 * s)
            # Brain hemispheres
            draw.ellipse([cx - br - 10, cy - br, cx + 5, cy + br - 10], fill=(245, 140, 180), outline=(210, 90, 140), width=3)
            draw.ellipse([cx - 5, cy - br, cx + br + 10, cy + br - 10], fill=(245, 140, 180), outline=(210, 90, 140), width=3)
            # Synaptic electrical nodes
            for angle in [0, 60, 120, 180, 240, 300]:
                rad = math.radians(angle)
                nx = cx + int(math.cos(rad) * (br + 18))
                ny = cy + int(math.sin(rad) * (br + 18))
                draw.ellipse([nx - 5, ny - 5, nx + 5, ny + 5], fill=(255, 230, 80))
                draw.line([(cx, cy), (nx, ny)], fill=(255, 230, 80, 160), width=2)

        elif prop_name in ["laptop", "computer"]:
            # Modern silver clamshell laptop with glowing screen
            lw = int(70 * s)
            lh = int(45 * s)
            # Screen portion tilted up
            draw.rounded_rectangle([cx - lw + 10, cy - lh, cx + lw - 10, cy + 10], radius=5, fill=(35, 40, 50), outline=(20, 24, 32), width=3)
            draw.rectangle([cx - lw + 18, cy - lh + 8, cx + lw - 18, cy + 2], fill=(60, 150, 255))
            # Base keyboard portion
            draw.polygon([(cx - lw, cy + 22), (cx + lw, cy + 22), (cx + lw - 15, cy + 10), (cx - lw + 15, cy + 10)], fill=(190, 195, 205), outline=(70, 75, 85), width=2)

        elif prop_name in ["coffee_cup", "coffee"]:
            # Cozy ceramic coffee mug with rising steam
            cw = int(35 * s)
            ch = int(45 * s)
            draw.rounded_rectangle([cx - cw, cy - ch + 15, cx + cw, cy + ch], radius=8, fill=(240, 242, 248), outline=(50, 55, 68), width=3)
            draw.arc([cx + cw - 5, cy - ch + 25, cx + cw + 25, cy + 15], 270, 90, fill=(50, 55, 68), width=4)
            # Steam swirls
            for sx in [-12, 12]:
                draw.line([(cx + sx, cy - ch + 5), (cx + sx + 8, cy - ch - 15), (cx + sx, cy - ch - 35)], fill=(220, 225, 235, 180), width=3)

        elif prop_name in ["book", "notebook"]:
            # Open scholarly book with white pages
            bw = int(60 * s)
            bh = int(38 * s)
            draw.polygon([(cx - bw, cy + bh), (cx - bw + 5, cy - bh), (cx, cy - bh + 10), (cx, cy + bh)], fill=(245, 242, 235), outline=(40, 45, 55), width=3)
            draw.polygon([(cx + bw, cy + bh), (cx + bw - 5, cy - bh), (cx, cy - bh + 10), (cx, cy + bh)], fill=(245, 242, 235), outline=(40, 45, 55), width=3)
            # Spine
            draw.line([(cx, cy - bh + 10), (cx, cy + bh)], fill=(180, 50, 40), width=4)

        elif prop_name in ["target_bullseye", "target", "goal"]:
            # Concentric archery bullseye target
            r = int(55 * s)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 45, 45), outline=(30, 32, 40), width=3)
            draw.ellipse([cx - int(r * 0.7), cy - int(r * 0.7), cx + int(r * 0.7), cy + int(r * 0.7)], fill=(255, 255, 255))
            draw.ellipse([cx - int(r * 0.4), cy - int(r * 0.4), cx + int(r * 0.4), cy + int(r * 0.4)], fill=(240, 45, 45))
            draw.ellipse([cx - int(r * 0.15), cy - int(r * 0.15), cx + int(r * 0.15), cy + int(r * 0.15)], fill=(255, 215, 0))

        elif prop_name in ["lightbulb_idea", "lightbulb", "idea"]:
            # Radiant glowing idea lightbulb
            lr = int(35 * s)
            draw.ellipse([cx - lr, cy - lr - 10, cx + lr, cy + lr - 10], fill=(255, 235, 50), outline=(210, 160, 20), width=3)
            draw.rectangle([(cx - int(lr * 0.5), cy + lr - 15), (cx + int(lr * 0.5), cy + lr + 15)], fill=(160, 170, 185), outline=(60, 65, 75), width=2)
            # Idea rays
            for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
                rad = math.radians(angle)
                r1 = lr + 12
                r2 = lr + 28
                draw.line([(cx + int(math.cos(rad) * r1), cy - 10 + int(math.sin(rad) * r1)), (cx + int(math.cos(rad) * r2), cy - 10 + int(math.sin(rad) * r2))], fill=(255, 215, 0), width=3)

        elif prop_name in ["stopwatch", "timer"]:
            # Precision athletic stopwatch
            sr = int(45 * s)
            draw.ellipse([cx - sr, cy - sr + 10, cx + sr, cy + sr + 10], fill=(240, 245, 255), outline=(50, 55, 70), width=4)
            # Top crown button
            draw.rectangle([(cx - 8, cy - sr - 8), (cx + 8, cy - sr + 10)], fill=(70, 75, 90))
            # Stopwatch hand
            draw.line([(cx, cy + 10), (cx + int(sr * 0.6), cy - int(sr * 0.3))], fill=(230, 40, 40), width=3)
            draw.ellipse([cx - 4, cy + 6, cx + 4, cy + 14], fill=(30, 32, 40))

        elif prop_name in ["gold_medal", "medal"]:
            # Olympic gold victory medal with ribbon
            mr = int(40 * s)
            # Ribbon V-shape
            draw.polygon([(cx - 25, cy - 70), (cx, cy - mr), (cx - 10, cy - 70)], fill=(40, 90, 210))
            draw.polygon([(cx + 25, cy - 70), (cx, cy - mr), (cx + 10, cy - 70)], fill=(210, 40, 40))
            # Medal disc
            draw.ellipse([cx - mr, cy - mr, cx + mr, cy + mr], fill=(255, 215, 40), outline=(200, 150, 20), width=4)
            draw.text((cx - 8, cy - 16), "1", fill=(180, 120, 10))

        else:
            # Universal Procedural Fallback Badge for ANY arbitrary prop
            # Ensures ZERO missing graphics regardless of what topic or prop is requested
            clean_label = prop_name.replace("_", " ").title()[:12]
            pr = int(50 * s)
            draw.ellipse([cx - pr - 6, cy - pr - 6, cx + pr + 6, cy + pr + 6], fill=(40, 55, 80, 160))
            draw.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=(24, 28, 40), outline=(0, 220, 255), width=3)
            draw.text((cx - int(len(clean_label) * 4), cy - 8), clean_label, fill=(0, 240, 255))

    def compose_frame(
        self,
        scene_info: Dict[str, Any],
        t: float,
        is_speaking: bool = False,
        camera_zoom: float = 1.0,
        shake_intensity: float = 0.0
    ) -> Image.Image:
        """Renders a full scene frame for timestamp t."""
        bg_style = scene_info.get("bg_style", "dusk_space")
        base = self.render_background(bg_style)

        # Mouth flapping when speaking
        mouth_ratio = 0.0
        if is_speaking:
            mouth_ratio = 0.5 + 0.5 * math.sin(t * 18.0)

        # Character scaling and framing
        shot_type = scene_info.get("shot_type", "")
        if shot_type in ("big_face", "close_up"):
            char_scale = 1.35 if self.width >= self.height else 1.5
            base_y = int(self.height * 0.90)
        else:
            char_scale = scene_info.get("char_scale", 1.3 if self.width < self.height else 1.1)
            base_y = scene_info.get("char_y", int(self.height * 0.82))

        # Draw any scene props
        props = scene_info.get("props", [])
        for p in props:
            float_y = int(math.sin(t * 2.5) * 8)
            # Adapt coordinates to aspect ratio (Landscape 1920x1080 vs Vertical Shorts 1080x1920)
            if self.width < self.height:
                # Vertical Shorts mode: place prop at upper-right or relative
                px = p.get("x")
                px = int(self.width * 0.75) if px is None else int(px * (self.width / 1920.0))
                py = p.get("y")
                py = int(self.height * 0.35) if py is None else int(py * (self.height / 1080.0))
                pscale = p.get("scale", 1.0) * 1.1
            else:
                # Landscape standard mode
                px = p.get("x", 1400)
                py = p.get("y", 400)
                pscale = p.get("scale", 1.0)

            self.draw_prop(base, p.get("type", "sun"), px, py + float_y, pscale)

        # Character position & dynamic breathing
        char_x = scene_info.get("char_x", self.width // 2)
        pose_name = scene_info.get("pose") or scene_info.get("char_pose") or "idle"
        breathing = math.sin(t * 3.2) * 4 if pose_name != "running" else 0
        char_y = int(base_y + breathing)

        # 1. Floor Contact Drop Shadow (Grounded realism)
        shadow_w = int(130 * char_scale)
        shadow_h = int(24 * char_scale)
        shadow_overlay = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow_overlay)
        s_draw.ellipse([char_x - shadow_w, base_y - int(8 * char_scale), char_x + shadow_w, base_y + int(18 * char_scale)], fill=(0, 0, 0, 95))
        base = Image.alpha_composite(base, shadow_overlay)

        # 2. Draw Animated Character with procedural gait & gesture
        self.rig.draw_character(
            base,
            x=char_x,
            y=char_y,
            scale=char_scale,
            flip_x=scene_info.get("flip_x", False),
            expression=scene_info.get("expression", "normal"),
            pose=pose_name,
            mouth_open_ratio=mouth_ratio,
            t=t
        )

        # 3. Dynamic Action Speed Lines (for running or high shock)
        if pose_name == "running" or shake_intensity > 1.0:
            speed_overlay = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
            sp_draw = ImageDraw.Draw(speed_overlay)
            for s_idx in range(14):
                sy_line = int((s_idx * 80 + t * 350) % self.height)
                sx_line = int((self.width - ((t * 1400 + s_idx * 160) % (self.width + 400))))
                slen = int(160 + 90 * math.sin(s_idx * 2))
                sp_draw.line([(sx_line, sy_line), (sx_line + slen, sy_line)], fill=(255, 255, 255, 60), width=3)
            base = Image.alpha_composite(base, speed_overlay)

        # 4. Atmospheric Floating Light Motes / Ambient Particles
        ambient_overlay = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        a_draw = ImageDraw.Draw(ambient_overlay)
        rng = random.Random(101)
        for p_idx in range(24):
            px_b = rng.randint(40, self.width - 40)
            py_b = rng.randint(40, self.height - 40)
            drift_y = (py_b - int(t * 24 + p_idx * 18)) % self.height
            drift_x = px_b + int(math.sin(t * 1.6 + p_idx) * 16)
            alpha = int(70 + 60 * math.sin(t * 2.2 + p_idx))
            a_draw.ellipse([drift_x - 3, drift_y - 3, drift_x + 3, drift_y + 3], fill=(255, 245, 210, alpha))
        base = Image.alpha_composite(base, ambient_overlay)

        # 5. Cinematic Camera Push-In / Zoom
        if camera_zoom > 1.002:
            w_crop = int(self.width / camera_zoom)
            h_crop = int(self.height / camera_zoom)
            x1 = (self.width - w_crop) // 2
            # Push-in anchored towards upper torso/face
            anchor_y = int((char_y - self.height * 0.45) * (1.0 - 1.0 / camera_zoom))
            y1 = max(0, min(self.height - h_crop, anchor_y))
            base = base.crop((x1, y1, x1 + w_crop, y1 + h_crop)).resize((self.width, self.height), Image.Resampling.BILINEAR)

        # 6. Camera Shake
        if shake_intensity > 0:
            dx = int(random.uniform(-shake_intensity, shake_intensity))
            dy = int(random.uniform(-shake_intensity, shake_intensity))
            base = base.transform(base.size, Image.AFFINE, (1, 0, dx, 0, 1, dy))

        return base.convert("RGB")
