"""
Procedural 2D Stick-Figure Rig Engine — Cinematic What-If Edition
Matches the exact style bible of viral channels (Awaken, IMAGINE, Suddenly You):
- Pure dark ink figure (#0e0b12) with thick round-capped line limbs
- Warm cream facial features (#f4efe6)
- Warm amber/cream rim-light highlight edge (#ffc68a) on the lit side
- Signature colored garment (Deep blue jacket #1e56a0 for hero)
- Dynamic poses: idle, pointing, thinking, shrugging, panicking, hands_on_hips, slouching, lying, explaining, pointing_up
- Expressive acting expressions & kinetic lip-sync
- bigFace giant close-up shot generator
"""

import math
from typing import Tuple, Optional, Dict, Any
from PIL import Image, ImageDraw


class StickFigureRig:
    def __init__(
        self,
        ink_color: Tuple[int, int, int] = (14, 11, 18),        # Pure dark ink #0e0b12
        face_cream: Tuple[int, int, int] = (244, 239, 230),    # Warm cream #f4efe6
        rim_color: Tuple[int, int, int] = (255, 198, 138),     # Warm amber rim #ffc68a
        hero_jacket: Tuple[int, int, int] = (30, 86, 160),     # Signature blue #1e56a0
        line_width: int = 11,
    ):
        self.ink_color = ink_color
        self.face_cream = face_cream
        self.rim_color = rim_color
        self.hero_jacket = hero_jacket
        self.line_width = line_width

    def draw_character(
        self,
        img: Image.Image,
        x: int,
        y: int,
        scale: float = 1.0,
        flip_x: bool = False,
        expression: str = "normal",
        pose: str = "idle",
        mouth_open_ratio: float = 0.0,
        outfit_color: Optional[Tuple[int, int, int]] = None,
        rim_light: bool = True,
        rim_dir: Tuple[float, float] = (-0.8, -0.5),
        t: float = 0.0,
    ) -> Image.Image:
        """
        Draws the cinematic stick character centered at foot position (x, y).
        - x, y: Base foot level coordinate on canvas
        - scale: Character scaling factor (1.0 = ~450px height)
        - outfit_color: RGB tuple for jacket/shirt (defaults to hero blue #1e56a0)
        - rim_light: Whether to render the signature rim light edge glow
        - t: Timestamp for procedural motion cycles (running strides, lifting reps, speech gestures)
        """
        outfit = outfit_color or self.hero_jacket
        char_w = int(550 * scale)
        char_h = int(650 * scale)
        char_canvas = Image.new("RGBA", (char_w, char_h), (0, 0, 0, 0))

        cx = char_w // 2
        head_r = int(52 * scale)
        head_y = int(130 * scale)
        lw = max(4, int(self.line_width * scale))

        # 1. RENDER RIM LIGHT GLOW LAYER (Offset silhouette in amber)
        if rim_light:
            rim_canvas = Image.new("RGBA", (char_w, char_h), (0, 0, 0, 0))
            rim_draw = ImageDraw.Draw(rim_canvas)
            ox = int(rim_dir[0] * 5 * scale)
            oy = int(rim_dir[1] * 5 * scale)
            self._render_body_skeleton(
                rim_draw, cx + ox, head_y + oy, head_r, scale, lw + 4,
                pose, self.rim_color, self.rim_color, self.rim_color,
                t=t
            )
            # Alpha composite rim under character
            char_canvas = Image.alpha_composite(char_canvas, rim_canvas)

        # 2. RENDER MAIN INK BODY & SIGNATURE OUTFIT
        main_draw = ImageDraw.Draw(char_canvas)
        self._render_body_skeleton(
            main_draw, cx, head_y, head_r, scale, lw,
            pose, self.ink_color, outfit, self.face_cream,
            expression=expression, mouth_open=mouth_open_ratio,
            t=t
        )

        # Flip horizontally if requested
        if flip_x:
            char_canvas = char_canvas.transpose(Image.FLIP_LEFT_RIGHT)

        # Paste onto destination image at (x - cx, y - char_h)
        paste_x = x - (char_w // 2)
        paste_y = y - char_h + int(50 * scale)
        img.paste(char_canvas, (paste_x, paste_y), char_canvas)
        return img

    def _render_body_skeleton(
        self,
        draw: ImageDraw.Draw,
        cx: int,
        head_y: int,
        head_r: int,
        s: float,
        lw: int,
        pose: str,
        body_col: Tuple[int, int, int],
        jacket_col: Tuple[int, int, int],
        face_col: Tuple[int, int, int],
        expression: str = "normal",
        mouth_open: float = 0.0,
        t: float = 0.0,
    ):
        neck_y = head_y + head_r
        pelvis_y = neck_y + int(130 * s)
        knee_y = pelvis_y + int(95 * s)
        foot_y = knee_y + int(85 * s)

        # Poses: Handling sitting/slouching/lying/running/exhausted
        if pose == "slouching":
            # Slouched back on a couch/bed
            pelvis_x = cx + int(40 * s)
            pelvis_y = neck_y + int(100 * s)
            knee_y = pelvis_y + int(40 * s)
            foot_y = knee_y + int(60 * s)
            # Legs stretched forward
            draw.line([(pelvis_x, pelvis_y), (cx + int(90 * s), knee_y), (cx + int(140 * s), foot_y)], fill=body_col, width=lw, joint="curve")
            draw.line([(pelvis_x, pelvis_y), (cx + int(70 * s), knee_y + 10), (cx + int(120 * s), foot_y + 10)], fill=body_col, width=lw, joint="curve")
            # Torso leaning back
            draw.line([(cx, neck_y), (pelvis_x, pelvis_y)], fill=body_col, width=lw + 2)
            # Signature Jacket over torso
            draw.line([(cx, neck_y + int(10 * s)), (pelvis_x - int(10 * s), pelvis_y - int(20 * s))], fill=jacket_col, width=lw + 8)
            # Limbs hanging limp
            sy = neck_y + int(20 * s)
            draw.line([(cx, sy), (cx + int(25 * s), sy + int(60 * s)), (cx + int(40 * s), sy + int(110 * s))], fill=body_col, width=lw)
            draw.line([(cx, sy), (cx - int(20 * s), sy + int(60 * s)), (cx - int(30 * s), sy + int(100 * s))], fill=body_col, width=lw)

        elif pose == "lying":
            # Completely horizontal on bed or floor
            head_x = cx - int(140 * s)
            pelvis_x = cx
            pelvis_y = head_y + int(20 * s)
            foot_x = cx + int(150 * s)
            draw.line([(head_x, head_y + int(10 * s)), (pelvis_x, pelvis_y)], fill=body_col, width=lw + 2)
            # Jacket
            draw.line([(head_x + int(40 * s), head_y + int(10 * s)), (pelvis_x, pelvis_y)], fill=jacket_col, width=lw + 8)
            # Legs
            draw.line([(pelvis_x, pelvis_y), (pelvis_x + int(70 * s), pelvis_y + int(10 * s)), (foot_x, pelvis_y + int(15 * s))], fill=body_col, width=lw)
            # Arms on chest/belly
            draw.line([(head_x + int(45 * s), head_y + int(10 * s)), (cx - int(30 * s), head_y - int(15 * s)), (cx, head_y + int(5 * s))], fill=body_col, width=lw)
            # Head circle at head_x
            head_box = [head_x - head_r, head_y - head_r, head_x + head_r, head_y + head_r]
            draw.ellipse(head_box, fill=body_col)
            if body_col == self.ink_color:
                self._draw_face(draw, head_x, head_y, head_r, s, lw, expression or "sleepy", mouth_open)
            return

        elif pose == "running":
            # Procedural dynamic running cycle with alternating strides and foot contact
            stride = math.sin(t * 13.0)
            stride_cos = math.cos(t * 13.0)
            bounce = abs(stride) * int(8 * s)
            tilt_x = int(28 * s)
            pelvis_x = cx - tilt_x

            # Torso leaning forward with vertical athletic bounce
            draw.line([(cx + tilt_x, neck_y - bounce), (pelvis_x, pelvis_y - bounce)], fill=body_col, width=lw + 2)
            draw.line([(cx + tilt_x - int(5 * s), neck_y - bounce + int(10 * s)), (pelvis_x + int(5 * s), pelvis_y - bounce - int(10 * s))], fill=jacket_col, width=lw + 8)

            # Leg swing calculations (alternating front and back strides)
            leg_swing = int(stride * 65 * s)
            knee_bend = abs(int(stride_cos * 35 * s))

            # Leg 1
            l1_knee = (pelvis_x + int(30 * s) + leg_swing, pelvis_y - bounce + int(45 * s) - knee_bend)
            l1_foot = (pelvis_x + int(50 * s) + leg_swing * 2, foot_y - bounce)
            draw.line([(pelvis_x, pelvis_y - bounce), l1_knee, l1_foot], fill=body_col, width=lw, joint="curve")

            # Leg 2 (Opposite phase)
            l2_knee = (pelvis_x - int(20 * s) - leg_swing, pelvis_y - bounce + int(45 * s) - int((35 * s) - knee_bend))
            l2_foot = (pelvis_x - int(40 * s) - leg_swing * 2, foot_y - bounce - int(12 * s))
            draw.line([(pelvis_x, pelvis_y - bounce), l2_knee, l2_foot], fill=body_col, width=lw, joint="curve")

            # Head Circle (bobbing with bounce)
            head_box = [cx + tilt_x - head_r, head_y - bounce - head_r, cx + tilt_x + head_r, head_y - bounce + head_r]
            draw.ellipse(head_box, fill=body_col)
            if body_col == self.ink_color:
                self._draw_face(draw, cx + tilt_x, head_y - bounce, head_r, s, lw, expression, mouth_open)

            # Arms swing
            sy = neck_y - bounce + int(20 * s)
            arm_swing = int(stride_cos * 45 * s)
            draw.line([(cx + tilt_x, sy), (cx + tilt_x + int(35 * s) - arm_swing, sy + int(25 * s)), (cx + tilt_x + int(70 * s) - arm_swing * 2, sy - int(10 * s))], fill=body_col, width=lw, joint="curve")
            draw.line([(cx + tilt_x, sy), (cx + tilt_x - int(35 * s) + arm_swing, sy + int(30 * s)), (cx + tilt_x - int(75 * s) + arm_swing * 2, sy + int(15 * s))], fill=body_col, width=lw, joint="curve")
            return

        elif pose == "exhausted":
            # Bent over hands on knees, catching breath
            lean_x = cx + int(30 * s)
            draw.line([(cx - int(20 * s), neck_y + int(30 * s)), (cx - int(50 * s), pelvis_y)], fill=body_col, width=lw + 2)
            draw.line([(cx - int(25 * s), neck_y + int(40 * s)), (cx - int(45 * s), pelvis_y - int(15 * s))], fill=jacket_col, width=lw + 8)
            # Legs slightly bent
            draw.line([(cx - int(50 * s), pelvis_y), (cx - int(30 * s), knee_y), (cx - int(35 * s), foot_y)], fill=body_col, width=lw)
            draw.line([(cx - int(50 * s), pelvis_y), (cx + int(30 * s), knee_y), (cx + int(25 * s), foot_y)], fill=body_col, width=lw)
            # Arms resting on knees
            sy = neck_y + int(35 * s)
            draw.line([(cx - int(20 * s), sy), (cx - int(30 * s), knee_y)], fill=body_col, width=lw)
            draw.line([(cx - int(20 * s), sy), (cx + int(30 * s), knee_y)], fill=body_col, width=lw)
            # Sweat drop
            if body_col == self.ink_color:
                draw.ellipse([cx + int(15 * s), head_y - int(10 * s), cx + int(25 * s), head_y + int(5 * s)], fill=(80, 180, 255, 230))

        else:
            # Standard upright poses
            leg_spread = int(40 * s)
            left_foot = (cx - leg_spread, foot_y)
            right_foot = (cx + leg_spread, foot_y)

            # Draw Legs (Thick solid limbs)
            draw.line([(cx, pelvis_y), (cx - int(leg_spread * 0.7), knee_y), left_foot], fill=body_col, width=lw, joint="curve")
            draw.line([(cx, pelvis_y), (cx + int(leg_spread * 0.7), knee_y), right_foot], fill=body_col, width=lw, joint="curve")

            # Foot stubs
            draw.line([left_foot, (left_foot[0] - int(14 * s), left_foot[1])], fill=body_col, width=lw)
            draw.line([right_foot, (right_foot[0] + int(14 * s), right_foot[1])], fill=body_col, width=lw)

            # Draw Torso
            draw.line([(cx, neck_y), (cx, pelvis_y)], fill=body_col, width=lw + 2)

            # Draw Signature Jacket / Shirt
            jacket_top = neck_y + int(12 * s)
            jacket_bot = pelvis_y - int(15 * s)
            draw.line([(cx, jacket_top), (cx, jacket_bot)], fill=jacket_col, width=lw + 8)

            # Draw Arms based on pose
            shoulder_y = neck_y + int(25 * s)
            self._draw_arms(draw, cx, shoulder_y, s, lw, pose, body_col, t=t)

        # Draw Head Circle (Dark ink solid fill)
        head_box = [cx - head_r, head_y - head_r, cx + head_r, head_y + head_r]
        draw.ellipse(head_box, fill=body_col)

        # Only draw facial details on the main ink layer (not the rim layer)
        if body_col == self.ink_color:
            self._draw_face(draw, cx, head_y, head_r, s, lw, expression, mouth_open)

    def _draw_arms(self, draw: ImageDraw.Draw, cx: int, sy: int, s: float, lw: int, pose: str, col: Tuple[int, int, int], t: float = 0.0):
        arm_len = int(105 * s)

        if pose == "idle":
            # Subtle breathing sway in arms
            sway = int(math.sin(t * 3.0) * 3 * s)
            draw.line([(cx, sy), (cx - int(40 * s), sy + int(60 * s)), (cx - int(50 * s) + sway, sy + arm_len)], fill=col, width=lw, joint="curve")
            draw.line([(cx, sy), (cx + int(40 * s), sy + int(60 * s)), (cx + int(50 * s) - sway, sy + arm_len)], fill=col, width=lw, joint="curve")

        elif pose in ["pointing", "explaining"]:
            # Left arm down, right arm explaining/pointing with subtle gesture sway
            draw.line([(cx, sy), (cx - int(40 * s), sy + int(60 * s)), (cx - int(50 * s), sy + arm_len)], fill=col, width=lw, joint="curve")
            g_sway = int(math.sin(t * 4.0) * 6 * s)
            elbow_r = (cx + int(55 * s), sy - int(10 * s) + g_sway)
            hand_r = (cx + int(120 * s), sy - int(35 * s) + g_sway * 2)
            draw.line([(cx, sy), elbow_r, hand_r], fill=col, width=lw, joint="curve")
            if pose == "pointing":
                draw.line([hand_r, (hand_r[0] + int(18 * s), hand_r[1] - int(10 * s))], fill=col, width=max(2, int(lw * 0.7)))

        elif pose == "pointing_up":
            # Pointing straight up at sky/ceiling with gentle pulse
            pulse = int(math.sin(t * 3.5) * 4 * s)
            draw.line([(cx, sy), (cx - int(35 * s), sy + int(60 * s)), (cx - int(45 * s), sy + arm_len)], fill=col, width=lw, joint="curve")
            draw.line([(cx, sy), (cx + int(35 * s), sy - int(40 * s)), (cx + int(45 * s), sy - int(110 * s) + pulse)], fill=col, width=lw, joint="curve")

        elif pose in ["thinking", "shrugging"]:
            if pose == "thinking":
                # Left arm across chest, right hand on chin with slight head tilt
                draw.line([(cx, sy), (cx - int(45 * s), sy + int(50 * s)), (cx + int(10 * s), sy + int(50 * s))], fill=col, width=lw, joint="curve")
                draw.line([(cx, sy), (cx + int(50 * s), sy + int(35 * s)), (cx + int(20 * s), sy - int(25 * s))], fill=col, width=lw, joint="curve")
            else:
                # Shrugging palms up with bounce
                shrug_b = int(math.sin(t * 3.5) * 4 * s)
                draw.line([(cx, sy), (cx - int(60 * s), sy + int(20 * s)), (cx - int(90 * s), sy - int(20 * s) - shrug_b)], fill=col, width=lw, joint="curve")
                draw.line([(cx, sy), (cx + int(60 * s), sy + int(20 * s)), (cx + int(90 * s), sy - int(20 * s) - shrug_b)], fill=col, width=lw, joint="curve")

        elif pose in ["panicking", "hands_on_head"]:
            if pose == "hands_on_head":
                # Both hands clasping head in disbelief
                tremble = int(math.sin(t * 16.0) * 3 * s)
                draw.line([(cx, sy), (cx - int(55 * s) + tremble, sy - int(20 * s)), (cx - int(35 * s), sy - int(75 * s))], fill=col, width=lw, joint="curve")
                draw.line([(cx, sy), (cx + int(55 * s) - tremble, sy - int(20 * s)), (cx + int(35 * s), sy - int(75 * s))], fill=col, width=lw, joint="curve")
            else:
                # Panicking arms flailing up
                flail = int(math.sin(t * 10.0) * 12 * s)
                draw.line([(cx, sy), (cx - int(45 * s), sy - int(40 * s)), (cx - int(75 * s) + flail, sy - int(90 * s))], fill=col, width=lw, joint="curve")
                draw.line([(cx, sy), (cx + int(45 * s), sy - int(40 * s)), (cx + int(75 * s) - flail, sy - int(90 * s))], fill=col, width=lw, joint="curve")

        elif pose == "hands_on_hips":
            draw.line([(cx, sy), (cx - int(60 * s), sy + int(40 * s)), (cx - int(30 * s), sy + int(90 * s))], fill=col, width=lw, joint="curve")
            draw.line([(cx, sy), (cx + int(60 * s), sy + int(40 * s)), (cx + int(30 * s), sy + int(90 * s))], fill=col, width=lw, joint="curve")

        elif pose in ["celebrating", "celebrating_win"]:
            # Triumphant raised arms pumping in V-shape with clenched fists
            pump = int(abs(math.sin(t * 8.0)) * 22 * s)
            draw.line([(cx, sy), (cx - int(55 * s), sy - int(50 * s)), (cx - int(85 * s), sy - int(120 * s) - pump)], fill=col, width=lw, joint="curve")
            draw.line([(cx, sy), (cx + int(55 * s), sy - int(50 * s)), (cx + int(85 * s), sy - int(120 * s) - pump)], fill=col, width=lw, joint="curve")
            # Fists
            draw.ellipse([cx - int(95 * s), sy - int(130 * s) - pump, cx - int(75 * s), sy - int(110 * s) - pump], fill=col)
            draw.ellipse([cx + int(75 * s), sy - int(130 * s) - pump, cx + int(95 * s), sy - int(110 * s) - pump], fill=col)

        elif pose in ["lifting", "lifting_weights"]:
            # Animated athletic weight pressing reps up and down
            press = 0.5 + 0.5 * math.sin(t * 4.5)
            press_y = int(press * 45 * s)
            draw.line([(cx, sy), (cx - int(65 * s), sy - int(10 * s)), (cx - int(65 * s), sy - int(40 * s) - press_y)], fill=col, width=lw, joint="curve")
            draw.line([(cx, sy), (cx + int(65 * s), sy - int(10 * s)), (cx + int(65 * s), sy - int(40 * s) - press_y)], fill=col, width=lw, joint="curve")
            # Heavy Barbells / Weights in hands
            bar_y = sy - int(40 * s) - press_y
            draw.line([(cx - int(95 * s), bar_y), (cx + int(95 * s), bar_y)], fill=(185, 195, 210), width=max(3, int(lw * 0.7)))
            draw.rectangle([(cx - int(115 * s), bar_y - int(20 * s)), (cx - int(95 * s), bar_y + int(20 * s))], fill=(45, 50, 60), outline=(20, 22, 28), width=2)
            draw.rectangle([(cx + int(95 * s), bar_y - int(20 * s)), (cx + int(115 * s), bar_y + int(20 * s))], fill=(45, 50, 60), outline=(20, 22, 28), width=2)

        elif pose == "reading":
            # Both hands brought together holding a book at chest level
            draw.line([(cx, sy), (cx - int(35 * s), sy + int(45 * s)), (cx - int(15 * s), sy + int(45 * s))], fill=col, width=lw, joint="curve")
            draw.line([(cx, sy), (cx + int(35 * s), sy + int(45 * s)), (cx + int(15 * s), sy + int(45 * s))], fill=col, width=lw, joint="curve")

        elif pose == "typing":
            # Forearms stretched forward horizontally typing at desk level
            draw.line([(cx, sy), (cx - int(30 * s), sy + int(35 * s)), (cx - int(10 * s), sy + int(65 * s))], fill=col, width=lw, joint="curve")
            draw.line([(cx, sy), (cx + int(30 * s), sy + int(35 * s)), (cx + int(60 * s), sy + int(65 * s))], fill=col, width=lw, joint="curve")

        else:
            # Default
            draw.line([(cx, sy), (cx - int(40 * s), sy + int(60 * s)), (cx - int(50 * s), sy + arm_len)], fill=col, width=lw)
            draw.line([(cx, sy), (cx + int(40 * s), sy + int(60 * s)), (cx + int(50 * s), sy + arm_len)], fill=col, width=lw)

    def _draw_face(
        self,
        draw: ImageDraw.Draw,
        cx: int,
        cy: int,
        r: int,
        s: float,
        lw: int,
        expression: str,
        mouth_open: float,
    ):
        eye_y = cy - int(8 * s)
        eye_spacing = int(20 * s)
        eye_r = max(3, int(6 * s))
        face_col = self.face_cream

        # --- EYES ---
        if expression in ["shocked", "jaw_drop"]:
            # Big open shocked eyes
            big_r = int(14 * s)
            for ex in [cx - eye_spacing, cx + eye_spacing]:
                draw.ellipse([ex - big_r, eye_y - big_r, ex + big_r, eye_y + big_r], fill=face_col)
                draw.ellipse([ex - 3, eye_y - 3, ex + 3, eye_y + 3], fill=self.ink_color)
            # Sweat drop
            draw.polygon([(cx + int(28 * s), cy - int(32 * s)), (cx + int(36 * s), cy - int(18 * s)), (cx + int(22 * s), cy - int(18 * s))], fill=(100, 180, 255))

        elif expression in ["deadpan", "sleepy"]:
            # Flat closed sleepy lines
            for ex in [cx - eye_spacing, cx + eye_spacing]:
                draw.line([(ex - eye_r - 2, eye_y), (ex + eye_r + 2, eye_y)], fill=face_col, width=max(2, int(lw * 0.7)))

        elif expression == "thinking":
            for ex in [cx - eye_spacing, cx + eye_spacing]:
                draw.ellipse([ex - eye_r + 2, eye_y - eye_r - 3, ex + eye_r + 2, eye_y + eye_r - 3], fill=face_col)
            # One raised brow
            draw.line([(cx + eye_spacing - int(10 * s), eye_y - int(16 * s)), (cx + eye_spacing + int(12 * s), eye_y - int(22 * s))], fill=face_col, width=max(2, int(lw * 0.6)))

        elif expression == "screaming":
            big_r = int(16 * s)
            for ex in [cx - eye_spacing, cx + eye_spacing]:
                draw.ellipse([ex - big_r, eye_y - big_r, ex + big_r, eye_y + big_r], fill=face_col)
                draw.ellipse([ex - 4, eye_y - 4, ex + 4, eye_y + 4], fill=self.ink_color)

        elif expression == "smirk":
            # Confident half-closed eyes
            draw.ellipse([cx - eye_spacing - eye_r, eye_y - eye_r, cx - eye_spacing + eye_r, eye_y + eye_r], fill=face_col)
            draw.line([(cx + eye_spacing - eye_r - 1, eye_y), (cx + eye_spacing + eye_r + 1, eye_y)], fill=face_col, width=max(2, int(lw * 0.7)))

        else:
            # Default warm cream dot eyes
            draw.ellipse([cx - eye_spacing - eye_r, eye_y - eye_r, cx - eye_spacing + eye_r, eye_y + eye_r], fill=face_col)
            draw.ellipse([cx + eye_spacing - eye_r, eye_y - eye_r, cx + eye_spacing + eye_r, eye_y + eye_r], fill=face_col)

        # --- MOUTH (Cream stroke / open shape synced to audio) ---
        mouth_y = cy + int(20 * s)
        mw = int(16 * s)
        mh = int((5 + 16 * mouth_open) * s)

        if expression in ["shocked", "jaw_drop"]:
            # Big vertical open O mouth
            draw.ellipse([cx - int(10 * s), mouth_y - int(5 * s), cx + int(10 * s), mouth_y + int(18 * s)], fill=face_col)
            draw.ellipse([cx - int(7 * s), mouth_y - int(2 * s), cx + int(7 * s), mouth_y + int(15 * s)], fill=self.ink_color)

        elif expression == "screaming":
            box = [cx - int(18 * s), mouth_y - int(5 * s), cx + int(18 * s), mouth_y + int(24 * s)]
            draw.ellipse(box, fill=face_col)
            draw.ellipse([box[0] + 3, box[1] + 3, box[2] - 3, box[3] - 3], fill=(80, 20, 20))

        elif expression == "deadpan":
            draw.line([(cx - mw, mouth_y), (cx + mw, mouth_y)], fill=face_col, width=max(2, int(lw * 0.6)))

        elif expression == "smirk":
            # Asymmetric confident half-smile
            draw.arc([cx - int(8 * s), mouth_y - int(10 * s), cx + mw, mouth_y + int(8 * s)], start=20, end=150, fill=face_col, width=max(2, int(lw * 0.7)))

        elif mouth_open > 0.2:
            # Speaking dynamic mouth
            draw.ellipse([cx - mw, mouth_y - mh // 2, cx + mw, mouth_y + mh // 2], fill=face_col)
            inner_h = max(2, mh - int(4 * s))
            draw.ellipse([cx - mw + 3, mouth_y - inner_h // 2, cx + mw - 3, mouth_y + inner_h // 2], fill=self.ink_color)

        else:
            # Calm smile
            draw.arc([cx - mw, mouth_y - int(8 * s), cx + mw, mouth_y + int(6 * s)], start=20, end=160, fill=face_col, width=max(2, int(lw * 0.7)))

    # --- THE SIGNATURE bigFace SHOT (Giant head filling 65% of frame) ---
    def draw_big_face(
        self,
        img: Image.Image,
        cx: int,
        cy: int,
        radius: int = 240,
        expression: str = "normal",
        mouth_open_ratio: float = 0.0,
        rim_light: bool = True,
        rim_dir: Tuple[float, float] = (-0.8, -0.5),
    ) -> Image.Image:
        """
        Renders the signature bigFace shot: a giant stick figure close-up head
        used in Awaken / IMAGINE for extreme emotion, shock, and dramatic realization beats.
        """
        draw = ImageDraw.Draw(img)

        # 1. Warm Rim Crescent
        if rim_light:
            rox = int(rim_dir[0] * 12)
            roy = int(rim_dir[1] * 12)
            draw.ellipse([cx + rox - radius, cy + roy - radius, cx + rox + radius, cy + roy + radius], fill=self.rim_color)

        # 2. Main Ink Head Circle
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=self.ink_color)

        # 3. Large Facial Features
        scale = radius / 120.0
        lw = max(5, int(self.line_width * scale * 0.6))
        self._draw_face(draw, cx, cy, radius, scale, lw, expression, mouth_open_ratio)
        return img
