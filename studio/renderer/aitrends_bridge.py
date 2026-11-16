"""
AITrends Studio Engine Bridge — Universal Production Engine 3.0
Bridges CARTOON-JARVIS and AIDirector to the production-grade AITrends 2D Studio kit
(HTML Canvas + Three.js + Playwright Chromium + FFmpeg + -14 LUFS procedural DSP audio mastering).
Features:
- Dedicated per-prompt workspace folder (`e:\agent x\projects\<prompt_slug>/`) containing all assets:
  prompt.json, script.json, images/, audio/, timeline/, story/, final_video.mp4, and youtube_package.json.
- Dynamic prompt-specific storytelling: no hardcoded templates. Adapts to Fables, Survival, What-If, Science.
- Dedicated AI-generated scene illustrations per scene via Pollinations ($0 free, no API key required).
- Smooth Ken Burns camera motion (zoom in/out, pan left/right) and dusk lighting grade.
- Dynamic character acting (27 poses, expressions, dual characters, props, kinetic badges).
- Full synchronized karaoke captions from word-level audio alignment.
- Procedural audio mastering (-14 LUFS DSP with adaptive ducking and ambient soundscapes).
"""

import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from typing import Dict, Any, List, Optional

# Ensure workspace root is in path
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

# Ensure E: drive binaries and environments are set before anything else
VENV_SCRIPTS = r"E:\agent y\cartoon-jarvis\.venv\Scripts"
if VENV_SCRIPTS not in os.environ.get("PATH", ""):
    os.environ["PATH"] = f"{VENV_SCRIPTS};{os.environ.get('PATH', '')}"
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"e:\playwright_browsers"
os.environ["TEMP"] = r"e:\temp"
os.environ["TMP"] = r"e:\temp"
os.environ["npm_config_cache"] = r"e:\npm_cache"

from studio.brain.ai_director import AIDirector
from studio.audio.tts_engine import TTSEngine
from studio.visual.thumbnail_generator import ThumbnailGenerator


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    slug = re.sub(r"[-\s]+", "_", text)[:35]
    return slug or "viral_video"


class AITrendsBridge:
    def __init__(self, kit_dir: Optional[str] = None):
        self.kit_dir = kit_dir or os.path.join(WORKSPACE_ROOT, "studio", "renderer", "aitrends_kit")
        self.projects_dir = os.path.join(WORKSPACE_ROOT, "projects")
        os.makedirs(self.projects_dir, exist_ok=True)
        self.python_exe = r"E:\agent y\cartoon-jarvis\.venv\Scripts\python.exe"
        self.browsers_path = r"e:\playwright_browsers"
        self.temp_dir = r"e:\temp"
        os.makedirs(self.temp_dir, exist_ok=True)

    def _get_env(self) -> Dict[str, str]:
        env = os.environ.copy()
        venv_scripts = r"E:\agent y\cartoon-jarvis\.venv\Scripts"
        env["PATH"] = f"{venv_scripts};{env.get('PATH', '')}"
        env["PLAYWRIGHT_BROWSERS_PATH"] = self.browsers_path
        env["TEMP"] = self.temp_dir
        env["TMP"] = self.temp_dir
        env["npm_config_cache"] = r"e:\npm_cache"
        return env

    # -------------------------------------------------------------
    # 1. MAP POSE, EXPR, SET, SFX
    # -------------------------------------------------------------
    def _map_pose(self, pose: str) -> str:
        mapping = {
            "idle": "stand",
            "standing": "stand",
            "pointing": "point",
            "thinking": "think",
            "shrugging": "shrug",
            "panicking": "handsOnHead",
            "hands_on_hips": "relaxed",
            "slouching": "sit",
            "sitting": "sit",
            "lying": "lie",
            "lying_down": "lie",
            "explaining": "explain",
            "pointing_up": "pointUp",
            "hands_on_head": "handsOnHead",
            "typing": "holdFront",
            "phone": "phone",
            "running": "ready",
            "lifting": "reach",
            "celebrating": "cheer",
            "exhausted": "sad",
            "reading": "holdFront",
            "shocked": "handsOnHead",
            "happy": "cheer",
            "waving": "wave",
            "jumping": "jump",
            "falling": "fall",
            "kicking": "kick",
            "crouching": "crouch",
            "cross_arms": "crossArms",
            # Day One Films poses
            "run_motivated": "run_motivated",
            "run_disciplined": "run_disciplined",
            "bed_lying": "bed_lying",
            "bed_wakeup_fire": "bed_wakeup_fire",
            "bed_wakeup_disciplined": "bed_wakeup_disciplined",
            "curl_dumbbell": "curl_dumbbell",
            "desk_slump": "desk_slump",
            "drag_body": "drag_body"
        }
        return mapping.get(pose, "stand")

    def _map_expr(self, expr: str) -> str:
        mapping = {
            "normal": "neutral",
            "neutral": "neutral",
            "shocked": "shocked",
            "deadpan": "neutral",
            "thinking": "thinking",
            "screaming": "shocked",
            "happy": "happy",
            "smirk": "smirk",
            "jaw_drop": "shocked",
            "sleepy": "neutral",
            "motivated": "motivated",
            "disciplined": "disciplined",
            "exhausted": "exhausted"
        }
        return mapping.get(expr, "neutral")

    def _map_set(self, bg_style: str) -> tuple[str, str]:
        mapping = {
            "cozy_bedroom": ("bedroom", "interiorWarm"),
            "living_room_couch": ("bedroom", "interiorWarm"),
            "school_classroom": ("classroom", "coolDay"),
            "office_workspace": ("classroom", "coolDay"),
            "city_street": ("cityStreet", "dusk"),
            "outdoor_park": ("cityStreet", "dusk"),
            "sports_stadium": ("cityStreet", "dusk"),
            "running_track": ("cityStreet", "dusk"),
            "gym_fitness": ("classroom", "interiorWarm"),
            "ruins_wasteland": ("ruinsWasteland", "dusk"),
            "desert_dunes": ("ruinsWasteland", "golden"),
            "volcano_lava": ("ruinsWasteland", "crimson"),
            "dusk_space": ("spaceVoid", "midnight"),
            "frozen_ice": ("spaceVoid", "neon"),
            "nature_forest": ("natureForest", "dusk"),
            "jungle_forest": ("natureForest", "dusk"),
            "high_tech_server": ("highTechServer", "cyberpunk"),
            "tech_server_room": ("highTechServer", "cyberpunk"),
            "hospital_lab": ("lab", "coolDay"),
            "cafe": ("cafe", "interiorWarm"),
            "library_books": ("cafe", "interiorWarm"),
            "bank_vault": ("lab", "cyberpunk"),
            "mountain_peak": ("natureForest", "golden"),
            # Day One Films signature sets
            "dayone_bedroom": ("dayoneBedroom", "night"),
            "dayone_running_street": ("dayoneRunningStreet", "night"),
            "dayone_gym": ("dayoneGym", "interiorWarm"),
            "dayone_study_desk": ("dayoneStudyDesk", "interiorWarm"),
            "dayone_sunrise": ("dayoneSunrise", "dusk"),
            # Style 2A Modern Studio Tech
            "studio_tech": ("studioTech", "light"),
            "studio_tech_light": ("studioTech", "light"),
            "studio_tech_dark": ("studioTech", "dark_studio")
        }
        return mapping.get(bg_style, ("bedroom", "interiorWarm"))

    def _map_sfx(self, sfx: str) -> List[Dict[str, Any]]:
        sfx_lower = (sfx or "").lower()
        if "drone" in sfx_lower or "hit" in sfx_lower or "drop" in sfx_lower:
            return [{"at": 0.05, "name": "impact", "gain": -4}]
        elif "pop" in sfx_lower or "tap" in sfx_lower or "click" in sfx_lower:
            return [{"at": 0.1, "name": "pop", "gain": -6}]
        elif "shatter" in sfx_lower or "alarm" in sfx_lower or "crisis" in sfx_lower:
            return [{"at": 0.05, "name": "impact", "gain": -3}, {"at": 0.15, "name": "glitch", "gain": -5}]
        elif "whoosh" in sfx_lower or "transition" in sfx_lower or "cut" in sfx_lower:
            return [{"at": 0.0, "name": "whoosh", "gain": -7}]
        elif "ding" in sfx_lower or "bell" in sfx_lower or "idea" in sfx_lower:
            return [{"at": 0.1, "name": "ding", "gain": -5}]
        elif "boom" in sfx_lower or "title" in sfx_lower:
            return [{"at": 0.1, "name": "stinger", "gain": -5}]
        return []

    # -------------------------------------------------------------
    # 2. GENERATE AI SCENE ILLUSTRATIONS ($0 Free Pollinations API)
    # -------------------------------------------------------------
    def generate_scene_images(
        self,
        project_dir: str,
        scenes: List[Dict[str, Any]],
        topic: str,
        aspect_ratio: str = "9:16"
    ) -> List[str]:
        """
        Generates unique, high-aesthetic AI illustrations for each scene using Pollinations ($0 free tier).
        Saves images into project_dir/images/scene_001.png, scene_002.png, etc.
        """
        images_dir = os.path.join(project_dir, "images")
        os.makedirs(images_dir, exist_ok=True)

        is_vertical = (aspect_ratio == "9:16")
        w = 576 if is_vertical else 1024
        h = 1024 if is_vertical else 576
        ratio_tag = "9:16 vertical ratio, mobile wallpaper composition" if is_vertical else "16:9 widescreen cinematic composition"

        downloaded_paths = []

        def _fetch_one(idx: int, sc: Dict[str, Any]) -> Optional[str]:
            target_path = os.path.join(images_dir, f"scene_{idx:03d}.png")
            if os.path.exists(target_path) and os.path.getsize(target_path) > 5000:
                print(f"  🎨 [Scene Image {idx}/{len(scenes)}] Cached -> {os.path.basename(target_path)}")
                return target_path

            base_prompt = sc.get("image_prompt")
            if not base_prompt:
                visual = sc.get("visual_description", "")
                narr = sc.get("narration", "")
                bg = sc.get("bg_style", "cinematic atmosphere")
                base_prompt = f"{visual or narr}, setting {bg}, topic {topic}"

            clean_prompt = re.sub(r'["\']', '', base_prompt).strip()
            enhanced_prompt = (
                f"cinematic dusk-lit 2D illustration of {clean_prompt}, "
                f"minimalist anime vector art style, dark atmospheric moody lighting, warm amber rim light, "
                f"soft cinematic volumetric glow, high contrast, clean shapes, no text, no watermark, {ratio_tag}"
            )

            encoded = urllib.parse.quote(enhanced_prompt)
            seed = abs(hash(f"{topic}_{idx}")) % 100000
            url = f"https://image.pollinations.ai/prompt/{encoded}?width={w}&height={h}&nologo=true&seed={seed}"

            for attempt in range(3):
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
                    with urllib.request.urlopen(req, timeout=25) as resp:
                        data = resp.read()
                        if len(data) > 1000:
                            with open(target_path, "wb") as f:
                                f.write(data)
                            print(f"  🎨 [Scene Image {idx}/{len(scenes)}] Generated ({round(len(data)/1024, 1)} KB) -> {os.path.basename(target_path)}")
                            return target_path
                except Exception as e:
                    err_str = str(e)
                    if "402" in err_str or "401" in err_str or "403" in err_str or "404" in err_str:
                        print(f"  ⚠️ [Scene Image {idx}] {err_str} (Engine instantly using procedural vector set)")
                        break
                    if attempt < 2:
                        time.sleep(1)
                    else:
                        print(f"  ⚠️ [Scene Image {idx}] Download note: {e} (Engine will fallback to procedural vector set)")
            return None

        print(f"\n🎨 [AITrends Bridge] Generating {len(scenes)} unique scene illustrations via Pollinations AI...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            futures = {pool.submit(_fetch_one, idx, sc): idx for idx, sc in enumerate(scenes, start=1)}
            for fut in concurrent.futures.as_completed(futures):
                res_path = fut.result()
                if res_path:
                    downloaded_paths.append(res_path)

        downloaded_paths.sort()
        return downloaded_paths

    # -------------------------------------------------------------
    # 3. BUILD DEDICATED PROJECT FOLDER & TIMELINE
    # -------------------------------------------------------------
    def build_project(
        self,
        blueprint: Dict[str, Any],
        lang: str = "hi",
        duration_mode: str = "1min",
        aspect_ratio: str = "16:9",
        resolution: str = "720p",
        style: str = "dusk"
    ) -> Dict[str, Any]:
        title = blueprint.get("title", "What If Animation")
        slug = slugify(title)

        # 1. Dedicated isolated project folder in workspace root
        project_dir = os.path.join(self.projects_dir, slug)
        for d in ["input", "audio", "timeline", "story", "scenes/sets", "scenes/shots", "images", "build", "out"]:
            os.makedirs(os.path.join(project_dir, d), exist_ok=True)

        # Ensure directory junction in aitrends_kit/projects for seamless Playwright rendering
        kit_proj = os.path.join(self.kit_dir, "projects", slug)
        if not os.path.exists(kit_proj):
            try:
                subprocess.run(["cmd.exe", "/c", "mklink", "/J", kit_proj, project_dir], capture_output=True)
            except Exception:
                pass

        # Save prompt.json and script.json directly in the project directory
        prompt_data = {
            "topic": blueprint.get("topic", title),
            "title": title,
            "language": lang,
            "duration_mode": duration_mode,
            "aspect_ratio": aspect_ratio,
            "style": style,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(os.path.join(project_dir, "prompt.json"), "w", encoding="utf-8") as f:
            json.dump(prompt_data, f, indent=2, ensure_ascii=False)

        with open(os.path.join(project_dir, "script.json"), "w", encoding="utf-8") as f:
            json.dump(blueprint, f, indent=2, ensure_ascii=False)

        # Copy universal sets to project
        sets_src = os.path.join(self.kit_dir, "scenes", "sets")
        sets_dst = os.path.join(project_dir, "scenes", "sets")
        for fn in ["universal_sets.js", "dayone_sets.js", "style2a_sets.js", "cafe.js", "lab.js"]:
            src_file = os.path.join(sets_src, fn)
            if os.path.exists(src_file):
                shutil.copy2(src_file, os.path.join(sets_dst, fn))

        # Synthesize audio per scene & build contiguous timeline
        tts = TTSEngine(default_lang=lang)
        scenes = blueprint.get("scenes", [])
        chunk_audios = []
        shots_json_list = []
        all_words = []
        full_script_lines = []

        current_time = 0.0
        audio_dir = os.path.join(project_dir, "audio")
        os.makedirs(audio_dir, exist_ok=True)

        print(f"🎙️ [AITrends Bridge] Synthesizing voiceover for {len(scenes)} scenes...")
        for idx, sc in enumerate(scenes, start=1):
            narration = sc.get("narration", "").strip()
            full_script_lines.append(narration)
            chunk_file = os.path.join(audio_dir, f"scene_{idx:03d}.mp3")

            words, dur = tts.synthesize(narration, chunk_file, lang=lang)
            chunk_audios.append(chunk_file)

            shot_id = f"s{idx:03d}"
            shot_start = round(current_time, 3)
            shot_end = round(current_time + dur + 0.35, 3)
            current_time = shot_end

            # Adjust word timestamps to global timeline
            for w in words:
                all_words.append({
                    "word": w["word"],
                    "start": round(shot_start + w["start"], 3),
                    "end": round(shot_start + w["end"], 3)
                })

            set_name, mood_name = self._map_set(sc.get("bg_style", "cozy_bedroom"))
            shot_type = sc.get("shot_type", "standard")
            is_big_face = (shot_type == "big_face")
            sfx_cues = self._map_sfx(sc.get("sfx", ""))

            shots_json_list.append({
                "id": shot_id,
                "start": shot_start,
                "end": shot_end,
                "line": narration,
                "scene": f"{sc.get('beat', '')} - {set_name}",
                "set": set_name,
                "bars": "scope" if (is_big_face or idx == 1) else None,
                "in": {"type": "flash" if idx in [3, 5] else "cut", "dur": 0.35},
                "sfx": sfx_cues,
                "amb": {"name": "murmur" if set_name in ["classroom", "cityStreet", "cafe"] else "roomtone", "gain": -26},
                "notes": f"beat: {sc.get('beat', '')}"
            })

        total_duration = round(current_time + 1.2, 3)

        # Lossless audio concatenation via FFmpeg
        voiceover_dst = os.path.join(project_dir, "input", "voiceover.mp3")
        concat_txt = os.path.join(audio_dir, "concat.txt")
        with open(concat_txt, "w", encoding="utf-8") as f:
            for ca in chunk_audios:
                f.write(f"file '{os.path.abspath(ca).replace(chr(92), '/')}'\n")

        ff_bin = shutil.which("ffmpeg") or "ffmpeg"
        ffmpeg_cmd = [
            ff_bin, "-y", "-v", "error",
            "-f", "concat", "-safe", "0",
            "-i", concat_txt,
            "-c:a", "libmp3lame", "-q:a", "2",
            voiceover_dst
        ]
        res_ff = subprocess.run(ffmpeg_cmd, capture_output=True, env=self._get_env())
        if res_ff.returncode != 0:
            print(f"⚠️ [AITrends Bridge] FFmpeg concat warning: {res_ff.stderr.decode()[:400]}")

        # Write script.txt
        script_dst = os.path.join(project_dir, "input", "script.txt")
        with open(script_dst, "w", encoding="utf-8") as f:
            f.write("\n\n".join(full_script_lines))

        # Write config.json
        cfg = {
            "title": title,
            "aspect": aspect_ratio,
            "resolution": resolution,
            "fps": 24,
            "style": style,
            "voiceover": "input/voiceover.mp3",
            "script": "input/script.txt",
            "duration": total_duration,
            "captions": True,
            "captionStyle": {
                "color": "#ffffff",
                "hi": "#ffd54f",
                "size": 56 if aspect_ratio == "9:16" else 44
            },
            "bars": None,
            "fadeIn": 0.5,
            "fadeOut": 0.8,
            "music": {"enabled": True, "gainDb": -18},
            "sfx": {"enabled": True, "gainDb": -6},
            "loudness": -14
        }
        with open(os.path.join(project_dir, "config.json"), "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)

        # Write timeline/words.json
        with open(os.path.join(project_dir, "timeline", "words.json"), "w", encoding="utf-8") as f:
            json.dump({"words": all_words}, f, indent=2)

        # Write story/shots.json with music plan
        music_plan = [
            {"start": 0, "end": round(total_duration * 0.35, 2), "mood": "mystery", "intensity": 0.45},
            {"start": round(total_duration * 0.35, 2), "end": round(total_duration * 0.75, 2), "mood": "tension", "intensity": 0.65},
            {"start": round(total_duration * 0.75, 2), "end": total_duration, "mood": "wonder", "intensity": 0.75}
        ]
        story_shots = {
            "title": title,
            "duration": total_duration,
            "shots": shots_json_list,
            "music": music_plan
        }
        with open(os.path.join(project_dir, "story", "shots.json"), "w", encoding="utf-8") as f:
            json.dump(story_shots, f, indent=2)

        # Generate unique AI illustrations for each scene
        scene_images = self.generate_scene_images(
            project_dir=project_dir,
            scenes=scenes,
            topic=blueprint.get("topic", title),
            aspect_ratio=aspect_ratio
        )

        # Write scenes/cast.js
        cast_js_content = """// scenes/cast.js — Character wardrobe with signature colours
export const HERO = { top: 'hoodie', color: '#1e56a0', head: 'none' };
export const SECONDARY = { top: 'hoodie', color: '#9b59b6', head: 'ponytail', headColor: '#f4efe6' };
export const FRIEND = { top: 'tshirt', color: '#3a6ea5', head: 'cap', headColor: '#f2c21a' };
export const DOC = { top: 'labcoat', face: 'glasses', head: 'none' };
export const CAST = [HERO, SECONDARY, FRIEND, DOC];
"""
        with open(os.path.join(project_dir, "scenes", "cast.js"), "w", encoding="utf-8") as f:
            f.write(cast_js_content)

        # Write scenes/shots/01_scenes.js
        self._write_shots_code(project_dir, scenes, shots_json_list, blueprint)

        print(f"✅ [AITrends Bridge] Dedicated project created: {project_dir}")
        print(f"   ({len(shots_json_list)} shots, {len(scene_images)} custom images, {total_duration}s)")
        return {
            "project_dir": project_dir,
            "slug": slug,
            "total_duration": total_duration,
            "num_shots": len(shots_json_list),
            "scene_images": scene_images
        }

    # -------------------------------------------------------------
    # 4. WRITE DYNAMIC SHOTS CODE (scenes/shots/01_scenes.js)
    # -------------------------------------------------------------
    def _write_shots_code(
        self,
        project_dir: str,
        scenes: List[Dict[str, Any]],
        shots_meta: List[Dict[str, Any]],
        blueprint: Dict[str, Any]
    ):
        shots_file = os.path.join(project_dir, "scenes", "shots", "01_scenes.js")
        title = blueprint.get("title", "What If?")
        clean_title = re.sub(r'["\']', '', title)

        title_words = clean_title.split()
        if len(title_words) > 3:
            t_line1 = " ".join(title_words[:3]).upper()
            t_line2 = " ".join(title_words[3:]).upper()
        else:
            t_line1 = "WHAT IF"
            t_line2 = clean_title.upper()

        primary_prop = blueprint.get("primary_prop") or "earth"
        youtube_kit = blueprint.get("youtube_kit", {})
        pinned_q = youtube_kit.get("pinned_comment", "What would YOU do? Tell us below!")
        clean_q = re.sub(r"[👇?!'\"#]+", "", pinned_q).strip()[:42] + "?"

        q_words = clean_q.split()
        if len(q_words) > 3:
            q_line1 = " ".join(q_words[:3]).upper()
            q_line2 = " ".join(q_words[3:]).upper()
        else:
            q_line1 = "WHAT WOULD"
            q_line2 = "YOU DO?"

        # Preload promises for all scene images
        preload_entries = []
        for idx in range(1, len(scenes) + 1):
            shot_id = f"s{idx:03d}"
            preload_entries.append(f"  preloadImg('{shot_id}', '/project/images/scene_{idx:03d}.png')")
        preload_js = ",\n".join(preload_entries)

        code_lines = [
            "// scenes/shots/01_scenes.js — Universal Dynamic Story Engine for aiTrends Studio",
            "import { E, V, registerShot, mood, layer, blurLayer, veil, ease, prog, clamp, lerp, shake, seg, circle, ring, rr, poly, glow, alpha, shade, linGrad, radGrad, FONTS, text, measure } from '/engine/core.js';",
            "import { drawFigure, POSES, posesAt, breathe, bigFace, headPos } from '/engine/rig2d.js';",
            "import { drawBeanCharacter, drawShadowDemon, drawFatigueFigure, drawMotivationMeter, drawDayBanner, drawDisciplineGraph, drawInSceneText } from '/engine/dayone_rig.js';",
            "import * as FX from '/engine/fx2d.js';",
            "import * as UI from '/engine/ui2d.js';",
            "import { bedroom, classroom, cityStreet, ruinsWasteland, spaceVoid, natureForest, highTechServer, cafe, lab, dayoneBedroom, dayoneRunningStreet, dayoneGym, dayoneStudyDesk, dayoneSunrise, studioTech, holoGlassCard, holoBarChart, holoCircularGauge, holoComparisonSplit, holoStageBadge } from '../sets/universal_sets.js';",
            "import { HERO, SECONDARY, FRIEND, DOC, CAST } from '../cast.js';",
            "",
            "const SETS = { bedroom, classroom, cityStreet, ruinsWasteland, spaceVoid, natureForest, highTechServer, cafe, lab, dayoneBedroom, dayoneRunningStreet, dayoneGym, dayoneStudyDesk, dayoneSunrise, studioTech };",
            "function getSet(name) { return SETS[name] || SETS.bedroom; }",
            "",
            "// Universal Image Preloader",
            "const SCENE_IMAGES = {};",
            "async function preloadImg(id, url) {",
            "  return new Promise((resolve) => {",
            "    const img = new Image();",
            "    const timer = setTimeout(() => {",
            "      console.warn('Image timeout for ' + id + ': ' + url);",
            "      resolve(null);",
            "    }, 8000);",
            "    img.crossOrigin = 'anonymous';",
            "    img.onload = () => { clearTimeout(timer); SCENE_IMAGES[id] = img; resolve(img); };",
            "    img.onerror = () => { clearTimeout(timer); console.warn('Image load error for ' + id + ': ' + url); resolve(null); };",
            "    img.src = url;",
            "  });",
            "}",
            "",
            "// Top-level await preloads all scene illustrations before Playwright captures frames",
            "await Promise.all([",
            preload_js,
            "]);",
            "",
            "// Universal Ken Burns Canvas Drawing Function",
            "function drawSceneBackground(g, img, t, dur, cameraMode = 'zoom_in') {",
            "  if (!img || !img.complete || img.naturalWidth === 0) return false;",
            "  g.save();",
            "  const p = clamp(t / Math.max(0.1, dur));",
            "  let scale = 1.0;",
            "  let tx = 0, ty = 0;",
            "  if (cameraMode === 'zoom_in') {",
            "    scale = 1.0 + 0.12 * ease.inOut(p);",
            "  } else if (cameraMode === 'zoom_out') {",
            "    scale = 1.12 - 0.12 * ease.inOut(p);",
            "  } else if (cameraMode === 'pan_right') {",
            "    scale = 1.08;",
            "    tx = -35 * ease.inOut(p);",
            "  } else if (cameraMode === 'pan_left') {",
            "    scale = 1.08;",
            "    tx = 35 * ease.inOut(p);",
            "  } else {",
            "    scale = 1.05 + 0.05 * Math.sin(p * Math.PI);",
            "  }",
            "  const cx = E.W / 2;",
            "  const cy = E.H / 2;",
            "  g.translate(cx, cy);",
            "  g.scale(scale, scale);",
            "  g.translate(-cx + tx, -cy + ty);",
            "  g.drawImage(img, 0, 0, E.W, E.H);",
            "  // Cinematic dusk atmosphere vignette",
            "  const vig = g.createRadialGradient(cx, cy, E.W * 0.35, cx, cy, E.W * 0.85);",
            "  vig.addColorStop(0, 'rgba(0, 0, 0, 0)');",
            "  vig.addColorStop(1, 'rgba(10, 8, 20, 0.40)');",
            "  g.fillStyle = vig; g.fillRect(0, 0, E.W, E.H);",
            "  g.restore();",
            "  return true;",
            "}",
            "",
            "// Universal procedural prop generator",
            "function drawTopicProp(g, type, x, y, scale = 1, t = 0, opts = {}) {",
            "  g.save();",
            "  g.translate(x, y);",
            "  g.scale(scale, scale);",
            "  const p = (type || '').toLowerCase();",
            "  if (p.includes('dna') || p.includes('genetic') || p.includes('strand')) {",
            "    const steps = 9, h = 90; glow(g, 0, 0, 75, '#38bdf8', 0.45);",
            "    for (let i = 0; i < steps; i++) {",
            "      const u = (i / (steps - 1)) * 2 - 1, py = u * (h / 2), phase = t * 3.2 + i * 0.7;",
            "      const x1 = Math.sin(phase) * 32, x2 = -x1, rungColor = i % 2 === 0 ? '#38bdf8' : '#ec4899';",
            "      seg(g, [[x1, py], [x2, py]], 3.5, alpha(rungColor, 0.75));",
            "      circle(g, x1, py, 5, '#38bdf8'); circle(g, x2, py, 5, '#ec4899');",
            "    }",
            "  } else if (p.includes('earth') || p.includes('planet') || p.includes('globe') || p.includes('world')) {",
            "    glow(g, 0, 0, 85, '#38bdf8', 0.55); circle(g, 0, 0, 38, '#1e3a8a'); ring(g, 0, 0, 39, 4, 'rgba(125,211,252,0.85)');",
            "    poly(g, [[-20, -18], [-6, -26], [8, -16], [2, -2], [-14, -4]], '#10b981');",
            "    poly(g, [[-12, 6], [16, 2], [22, 22], [4, 26], [-6, 16]], '#10b981');",
            "  } else if (p.includes('phone') || p.includes('mobile') || p.includes('screen')) {",
            "    const pw = 48, ph = 96;",
            "    rr(g, -pw/2 - 2, -ph/2 - 2, pw + 4, ph + 4, 10); g.fillStyle = '#1c1b22'; g.fill();",
            "    rr(g, -pw/2, -ph/2, pw, ph, 8); g.fillStyle = '#0a0f1d'; g.fill();",
            "    glow(g, 0, 0, 80, '#38bdf8', 0.6);",
            "    for (let r = 0; r < 3; r++) {",
            "      for (let c = 0; c < 2; c++) {",
            "        rr(g, -16 + c * 20, -34 + r * 20, 13, 13, 3);",
            "        g.fillStyle = c === 0 ? '#38bdf8' : '#fbbf24'; g.fill();",
            "      }",
            "    }",
            "    circle(g, pw/2 - 7, -ph/2 + 7, 4.5, '#ef4444');",
            "  } else if (p.includes('clock') || p.includes('alarm') || p.includes('time')) {",
            "    circle(g, 0, 0, 28, '#1e293b'); ring(g, 0, 0, 30, 4, '#f59e0b');",
            "    const ang = t * 7; seg(g, [[0, 0], [Math.sin(ang) * 20, -Math.cos(ang) * 20]], 3.5, '#f59e0b');",
            "    glow(g, 0, 0, 42, '#fbbf24', 0.55);",
            "  } else if (p.includes('money') || p.includes('gold') || p.includes('cash')) {",
            "    circle(g, 0, 0, 26, '#f59e0b'); ring(g, 0, 0, 26, 3.5, '#fbbf24');",
            "    text(g, '$', 0, 9, { size: 28, color: '#78350f', font: FONTS.ui, weight: 900 });",
            "    glow(g, 0, 0, 45, '#fbbf24', 0.65);",
            "  } else if (p.includes('dumbbell') || p.includes('gym')) {",
            "    g.fillStyle = '#94a3b8'; g.fillRect(-36, -5, 72, 10);",
            "    rr(g, -48, -26, 14, 52, 5); g.fillStyle = '#334155'; g.fill();",
            "    rr(g, 34, -26, 14, 52, 5); g.fillStyle = '#334155'; g.fill();",
            "  } else {",
            "    circle(g, 0, 0, 24, '#6366f1'); ring(g, 0, 0, 27, 3, '#a5b4fc');",
            "    glow(g, 0, 0, 45, '#818cf8', 0.65); text(g, '★', 0, 8, { size: 22, color: '#ffffff', font: FONTS.ui, weight: 900 });",
            "  }",
            "  g.restore();",
            "}",
            ""
        ]

        total_scenes = len(scenes)
        camera_motions = ["zoom_in", "pan_right", "zoom_out", "pan_left", "zoom_in", "zoom_out"]

        for idx, (sc, meta) in enumerate(zip(scenes, shots_meta), start=1):
            shot_id = meta["id"]
            set_name, mood_name = self._map_set(sc.get("bg_style", "cozy_bedroom"))
            pose_name = self._map_pose(sc.get("char_pose", "idle"))
            expr_name = self._map_expr(sc.get("expression", "normal"))
            is_last = (idx == total_scenes)
            is_first = (idx == 1)

            motion = camera_motions[(idx - 1) % len(camera_motions)]
            chars = sc.get("characters") or ["HERO"]
            badge_text = sc.get("badge") or (f"BEAT 0{idx}" if idx > 1 else "FOCUS")
            clean_badge = re.sub(r'["\']', '', str(badge_text))
            scene_prop = (sc.get("props") or [{}])[0].get("type") or primary_prop

            is_dayone = bool(
                sc.get("day_banner") or 
                sc.get("motivation_pct") is not None or 
                blueprint.get("style") == "dayone" or 
                "dayone" in str(sc.get("bg_style", "")) or
                sc.get("shadow_demon")
            )

            is_studio_tech = bool(
                "studio_tech" in str(sc.get("bg_style", "")) or
                sc.get("bar_chart") or
                sc.get("circular_gauge") or
                sc.get("comparison_split") or
                sc.get("stage_badge") or
                sc.get("glass_card")
            )

            if is_dayone and not is_studio_tech:
                has_demon = sc.get("shadow_demon", False)
                whisper = re.sub(r'["\']', '', sc.get("whisper_text", ""))
                has_fatigue = sc.get("fatigue_figure", False)
                has_graph = sc.get("discipline_graph", False)
                in_scene_text = re.sub(r'["\']', '', sc.get("in_scene_text", ""))
                day_banner = sc.get("day_banner", "")
                clock_time = sc.get("clock_time", "")
                mot_pct = sc.get("motivation_pct")
                char_offset = "- V(120, 90)" if has_demon else ""

                demon_code = f"drawShadowDemon(g, {{ x: CX + V(280, 220), y: GY - 10, s: V(1.3, 1.42), facing: -1, whisperText: '{whisper}', t: t }});" if has_demon else ""
                fatigue_code = f"drawFatigueFigure(g, {{ x: CX - V(190, 150), y: GY, s: V(0.95, 1.05), t: t }});" if has_fatigue else ""
                quote_code = f"drawInSceneText(g, {{ text: '{in_scene_text}', x: CX, y: GY - V(280, 320), size: 28 }});" if in_scene_text else ""
                graph_code = f"drawDisciplineGraph(g, {{ x: E.W / 2 - V(380, 320), y: V(220, 280), w: V(760, 640), h: V(420, 380), t: t, dur: info.dur }});" if has_graph else ""
                banner_code = f"drawDayBanner(g, {{ text: '{day_banner}', subtext: '{clock_time}', x: E.W / 2, y: V(70, 115) }});" if day_banner else ""
                meter_code = f"drawMotivationMeter(g, {{ pct: {mot_pct}, x: V(60, 40), y: V(60, 110), w: V(280, 230), h: 36, t: t }});" if mot_pct is not None else ""

                code_lines.append(f"""// {shot_id} — Day One Films Shot ({sc.get('beat', '')})
registerShot('{shot_id}', {{
  draw(g, t, info) {{
    const cam = {{ z: 1.0, x: 0 }};
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['{shot_id}'], t, info.dur, '{motion}');
    if (!hasBg) {{
      getSet('{set_name}')(g, t, cam, {{ mood: '{mood_name}', clockTime: '{clock_time}' }});
    }}
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    layer(g, cam, 1, (g) => {{
      {demon_code}
      {fatigue_code}
      drawBeanCharacter(g, {{
        x: CX {char_offset},
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        pose: '{sc.get("char_pose", "stand")}',
        expr: '{sc.get("expression", "motivated")}',
        aura: {sc.get("aura", 0.0)},
        darkBags: {str(sc.get("dark_bags", False)).lower()},
        t: t
      }});
      {quote_code}
      {graph_code}
    }});
    {banner_code}
    {meter_code}
    FX.dust(g, t, {{ count: 25, color: '#fed7aa', a: 0.3 }});
  }}
}});
""")
            elif is_studio_tech:
                # Style 2A: Modern Studio Tech Shot with Holographic UI
                bc = sc.get("bar_chart")
                cg = sc.get("circular_gauge")
                cs = sc.get("comparison_split")
                gc = sc.get("glass_card")
                sb = sc.get("stage_badge")

                bar_chart_code = ""
                if bc:
                    bars_json = json.dumps(bc.get("bars", []))
                    b_title = re.sub(r'["\']', '', bc.get('title', 'ANALYTICS'))
                    bar_chart_code = f"holoBarChart(g, CX - V(80, 20), GY - V(460, 480), V(480, 400), V(380, 340), {bars_json}, {{ title: '{b_title}', t, progress: Math.min(1.0, t / 1.5) }});"

                gauge_code = ""
                if cg:
                    g_lbl = re.sub(r'["\']', '', cg.get('label', 'EFFICIENCY'))
                    gauge_code = f"holoCircularGauge(g, CX + V(160, 100), GY - V(280, 300), V(110, 95), {cg.get('value', 80)}, {{ label: '{g_lbl}', unit: '{cg.get('unit', '%')}', t }});"

                comparison_code = ""
                if cs:
                    left_json = json.dumps(cs.get("left", {"title": "AMATEUR", "points": ["Feelings-driven"]}))
                    right_json = json.dumps(cs.get("right", {"title": "MASTER", "points": ["System-driven"]}))
                    comparison_code = f"holoComparisonSplit(g, CX - V(340, 280), GY - V(450, 480), V(700, 580), V(360, 340), {left_json}, {right_json}, {{ t }});"

                glass_card_code = ""
                if gc:
                    gc_title = re.sub(r'["\']', '', gc.get('title', 'DATA'))
                    gc_sub = re.sub(r'["\']', '', gc.get('subtitle', ''))
                    glass_card_code = f"holoGlassCard(g, CX - V(120, 40), GY - V(420, 440), V(440, 360), V(280, 260), {{ title: '{gc_title}', subtitle: '{gc_sub}', t }});"

                stage_badge_code = ""
                if sb:
                    sb_title = re.sub(r'["\']', '', sb.get('title', 'STAGE'))
                    stage_badge_code = f"holoStageBadge(g, V(60, 40), V(60, 110), {sb.get('num', 1)}, '{sb_title}');"

                studio_theme = 'dark_studio' if 'dark' in str(sc.get('bg_style', '')) else 'light'

                code_lines.append(f"""// {shot_id} — Style 2A Modern Studio Tech Shot ({sc.get('beat', '')})
registerShot('{shot_id}', {{
  draw(g, t, info) {{
    const cam = {{ z: 1.0, x: 0 }};
    studioTech(g, t, cam, {{ theme: '{studio_theme}' }});
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    layer(g, cam, 1, (g) => {{
      drawBeanCharacter(g, {{
        x: CX - V(360, 240),
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        pose: '{sc.get("char_pose", "point")}',
        expr: '{sc.get("expression", "motivated")}',
        t: t
      }});
      {bar_chart_code}
      {gauge_code}
      {comparison_code}
      {glass_card_code}
    }});
    {stage_badge_code}
    FX.dust(g, t, {{ count: 20, color: '#38bdf8', a: 0.25 }});
  }}
}});
""")
            elif is_first:
                # Shot 1: Cold Hook Opening Shot
                code_lines.append(f"""// {shot_id} — Cold Hook Opening Shot
registerShot('{shot_id}', {{
  draw(g, t, info) {{
    const cam = {{ z: 1.05 + 0.05 * ease.inOut(t / info.dur), x: -15 * ease.inOut(t / info.dur) }};
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['{shot_id}'], t, info.dur, 'zoom_in');
    if (!hasBg) {{
      getSet('{set_name}')(g, t, cam, {{ mood: '{mood_name}' }});
    }}
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    const rim = {{ color: '#ffb070', dir: [0, -1], w: 4.5 }};
    layer(g, cam, 1, (g) => {{
      drawFigure(g, {{
        x: CX,
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.{pose_name} || POSES.stand, t),
        expr: '{expr_name}',
        rim: rim
      }});
      drawTopicProp(g, '{scene_prop}', CX + V(30, 22), GY - V(140, 150), 1.2, t);
    }});
    UI.titleCard(g, t, {{
      lines: ['{t_line1}', '{t_line2}'],
      dur: Math.min(3.4, info.dur * 0.75),
      y: E.H * V(0.36, 0.30)
    }});
    UI.badge(g, {{ str: '{clean_badge}', color: '#ffd54f', x: E.W - V(90, 70), y: V(120, 160) }});
    FX.dust(g, t, {{ count: 35, color: '#ffe4c4', a: 0.3 }});
  }}
}});
""")
            elif is_last:
                # Last Shot: Climax & Discussion CTA
                code_lines.append(f"""// {shot_id} — Climax & Engagement CTA
registerShot('{shot_id}', {{
  draw(g, t, info) {{
    const cam = {{ z: 1.0, x: 0 }};
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['{shot_id}'], t, info.dur, 'zoom_out');
    if (!hasBg) {{
      getSet('{set_name}')(g, t, cam, {{ mood: '{mood_name}' }});
    }}
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    const rim = {{ color: '#ffd54f', dir: [0, -1], w: 5 }};
    layer(g, cam, 1, (g) => {{
      drawFigure(g, {{
        x: CX,
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.point || POSES.relaxed, t),
        expr: 'happy',
        rim: rim
      }});
    }});
    UI.titleCard(g, t, {{
      lines: ['{q_line1}', '{q_line2}'],
      dur: info.dur,
      y: E.H * V(0.32, 0.26)
    }});
    UI.badge(g, {{ str: '{clean_badge}', color: '#ffb070', x: E.W - V(90, 70), y: V(120, 160) }});
    FX.dust(g, t, {{ count: 35, color: '#ffd54f', a: 0.35 }});
  }}
}});
""")
            else:
                # Intermediate Narrative Shots (Unique to this scene's story)
                if len(chars) > 1:
                    code_lines.append(f"""// {shot_id} — Narrative Scene {idx} (Dual Characters)
registerShot('{shot_id}', {{
  draw(g, t, info) {{
    const cam = {{ z: 1.0, x: 0 }};
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['{shot_id}'], t, info.dur, '{motion}');
    if (!hasBg) {{
      getSet('{set_name}')(g, t, cam, {{ mood: '{mood_name}' }});
    }}
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    const rim = {{ color: '#ffb070', dir: [0, -1], w: 4.5 }};
    layer(g, cam, 1, (g) => {{
      drawFigure(g, {{
        x: CX - V(120, 90),
        y: GY,
        s: V(1.35, 1.48),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.{pose_name} || POSES.stand, t),
        expr: '{expr_name}',
        rim: rim
      }});
      drawFigure(g, {{
        x: CX + V(120, 90),
        y: GY,
        s: V(1.35, 1.48),
        facing: -1,
        outfit: SECONDARY,
        pose: breathe(POSES.relaxed, t + 0.3),
        expr: 'neutral',
        rim: {{ color: '#38bdf8', dir: [0, -1], w: 4.5 }}
      }});
      drawTopicProp(g, '{scene_prop}', CX, GY - V(140, 150), 1.2, t);
    }});
    UI.badge(g, {{ str: '{clean_badge}', color: '#7ee787', x: E.W - V(90, 70), y: V(120, 160) }});
    FX.dust(g, t, {{ count: 30, color: '#ffdfb8', a: 0.3 }});
  }}
}});
""")
                else:
                    code_lines.append(f"""// {shot_id} — Narrative Scene {idx} (Solo Hero)
registerShot('{shot_id}', {{
  draw(g, t, info) {{
    const cam = {{ z: 1.0, x: 0 }};
    const hasBg = drawSceneBackground(g, SCENE_IMAGES['{shot_id}'], t, info.dur, '{motion}');
    if (!hasBg) {{
      getSet('{set_name}')(g, t, cam, {{ mood: '{mood_name}' }});
    }}
    const CX = E.W / 2, GY = E.H * V(0.82, 0.68);
    const rim = {{ color: '#ffb070', dir: [0, -1], w: 4.5 }};
    layer(g, cam, 1, (g) => {{
      drawFigure(g, {{
        x: CX,
        y: GY,
        s: V(1.4, 1.55),
        facing: 1,
        outfit: HERO,
        pose: breathe(POSES.{pose_name} || POSES.stand, t),
        expr: '{expr_name}',
        rim: rim
      }});
      drawTopicProp(g, '{scene_prop}', CX + V(30, 22), GY - V(140, 150), 1.2, t);
    }});
    UI.badge(g, {{ str: '{clean_badge}', color: '#7ee787', x: E.W - V(90, 70), y: V(120, 160) }});
    FX.dust(g, t, {{ count: 30, color: '#ffdfb8', a: 0.3 }});
  }}
}});
""")

        with open(shots_file, "w", encoding="utf-8") as f:
            f.write("\n".join(code_lines))

    # -------------------------------------------------------------
    # 5. RENDER & AUDIO MASTER PIPELINE
    # -------------------------------------------------------------
    def render_and_master(
        self,
        project_dir: str,
        scale: float = 1.0,
        workers: int = 2
    ) -> str:
        """
        Executes render.mjs to generate silent video, then runs audio/mix.py to master sound.
        Returns final mastered MP4 path.
        """
        # Determine relative project path for aitrends_kit
        slug = os.path.basename(project_dir)
        kit_proj = os.path.join(self.kit_dir, "projects", slug)
        if os.path.exists(kit_proj):
            rel_proj = f"projects/{slug}"
        else:
            rel_proj = os.path.relpath(project_dir, self.kit_dir).replace("\\", "/")

        print(f"\n🎬 [AITrends Bridge] Starting Playwright Chromium frame renderer...")
        print(f"   Project: {rel_proj} (workers: {workers}, scale: {scale})")

        t0 = time.time()
        render_cmd = [
            "node", "render.mjs",
            "--project", rel_proj,
            "--workers", str(workers),
            "--scale", str(scale)
        ]

        p = subprocess.run(
            render_cmd,
            cwd=self.kit_dir,
            capture_output=True,
            text=True,
            env=self._get_env()
        )

        if p.returncode != 0:
            print(f"❌ [AITrends Bridge] Frame rendering failed:\n{p.stderr[-2000:]}")
            raise RuntimeError(f"Playwright rendering failed: {p.stderr[-500:]}")

        print(f"✅ [AITrends Bridge] Video frames rendered in {round(time.time() - t0, 1)}s")

        # Run procedural audio mastering (-14 LUFS DSP)
        print(f"\n🎵 [AITrends Bridge] Mastering soundtrack (-14 LUFS, procedural music + SFX + ducking)...")
        mix_cmd = [
            self.python_exe,
            "audio/mix.py",
            "--project", rel_proj
        ]

        p2 = subprocess.run(
            mix_cmd,
            cwd=self.kit_dir,
            capture_output=True,
            text=True,
            env=self._get_env()
        )

        if p2.returncode != 0:
            print(f"❌ [AITrends Bridge] Audio mixing failed:\n{p2.stderr[-2000:]}")
            raise RuntimeError(f"Audio mixing failed: {p2.stderr[-500:]}")

        # Locate output file
        out_dir = os.path.join(project_dir, "out")
        mp4_files = [os.path.join(out_dir, f) for f in os.listdir(out_dir) if f.endswith(".mp4")] if os.path.exists(out_dir) else []
        if not mp4_files:
            build_silent = os.path.join(project_dir, "build", "video_silent.mp4")
            if os.path.exists(build_silent):
                return build_silent
            raise FileNotFoundError("Could not find final rendered MP4 in project out/ folder.")

        final_mp4 = mp4_files[0]
        print(f"🎉 [AITrends Bridge] Mastered MP4 generated -> {final_mp4}")
        return final_mp4


# -----------------------------------------------------------------
# 6. COMPLETE END-TO-END PIPELINE FUNCTION
# -----------------------------------------------------------------
def generate_viral_video_aitrends(
    topic: str,
    lang: str = "hi",
    duration_mode: str = "1min",
    aspect_ratio: str = "16:9",
    style: str = "dusk",
    scale: float = 1.0,
    gemini_api_key: Optional[str] = None
) -> Dict[str, Any]:
    start_time = time.time()
    bridge = AITrendsBridge()

    print("\n" + "=" * 65)
    print("🌟 AITrends 2D Studio — Universal Production Engine 3.0")
    print("=" * 65)
    print(f"📌 Topic: {topic}")
    print(f"🌐 Language: {lang}")
    print(f"⏱️ Duration: {duration_mode}")
    print(f"📐 Format: {aspect_ratio}")
    print(f"🎨 Visual Style: {style}")
    print("-" * 65)

    # Step 1: AI Director Script & Package
    director = AIDirector(api_key=gemini_api_key)
    blueprint = director.generate_full_package(
        topic=topic,
        lang=lang,
        duration_mode=duration_mode,
        aspect_ratio=aspect_ratio
    )
    blueprint["style"] = style

    slug = slugify(blueprint.get("title", topic))
    youtube_kit = blueprint.get("youtube_kit", {})

    # Step 2: Build Dedicated Project Files, Timeline & Unique AI Illustrations
    built = bridge.build_project(
        blueprint=blueprint,
        lang=lang,
        duration_mode=duration_mode,
        aspect_ratio=aspect_ratio,
        resolution="720p",
        style=style
    )

    project_dir = built["project_dir"]

    # Step 3: Render Frames & Master Audio
    rendered_mp4 = bridge.render_and_master(project_dir, scale=scale, workers=2)

    # Copy mastered video to root of project folder
    proj_video_path = os.path.join(project_dir, "final_video.mp4")
    shutil.copy2(rendered_mp4, proj_video_path)

    # Step 4: Also copy to output_videos/ for global gallery
    out_dir = os.path.join(WORKSPACE_ROOT, "output_videos")
    os.makedirs(out_dir, exist_ok=True)
    final_video_name = f"{slug}_{lang}_aitrends.mp4"
    final_video_path = os.path.join(out_dir, final_video_name)
    shutil.copy2(rendered_mp4, final_video_path)

    # Step 5: Generate High-CTR Thumbnail
    thumb_gen = ThumbnailGenerator(width=1280, height=720)
    thumb_name = f"{slug}_{lang}_thumbnail.jpg"
    thumb_path = os.path.join(out_dir, thumb_name)
    proj_thumb_path = os.path.join(project_dir, "images", "thumbnail.jpg")

    first_bg = blueprint["scenes"][0].get("bg_style", "cozy_bedroom") if blueprint.get("scenes") else "cozy_bedroom"
    thumb_gen.generate_thumbnail(
        hook_text=youtube_kit.get("thumbnail_hook", "SACH DEKHO?!"),
        bg_style=first_bg,
        prop_type=youtube_kit.get("thumbnail_prop", "question_mark"),
        char_pose="panicking",
        char_expression="screaming",
        output_path=thumb_path
    )
    shutil.copy2(thumb_path, proj_thumb_path)

    # Step 6: Save YouTube Metadata Kit
    kit_data = {
        "topic": topic,
        "title": blueprint.get("title"),
        "language": lang,
        "aspect_ratio": aspect_ratio,
        "youtube_kit": youtube_kit,
        "video_file": final_video_name,
        "thumbnail_file": thumb_name,
        "engine": "aitrends_universal_engine_3.0",
        "style": style,
        "project_folder": os.path.abspath(project_dir)
    }

    kit_name = f"{slug}_{lang}_youtube_kit.json"
    kit_path = os.path.join(out_dir, kit_name)
    with open(kit_path, "w", encoding="utf-8") as f:
        json.dump(kit_data, f, indent=2, ensure_ascii=False)

    proj_kit_path = os.path.join(project_dir, "youtube_package.json")
    with open(proj_kit_path, "w", encoding="utf-8") as f:
        json.dump(kit_data, f, indent=2, ensure_ascii=False)

    elapsed = round(time.time() - start_time, 1)
    file_size_mb = round(os.path.getsize(final_video_path) / (1024 * 1024), 2)

    print("\n" + "=" * 65)
    print(f"🎉 SUCCESS! Masterpiece Generated in {elapsed}s")
    print(f"📁 Project Folder: {os.path.abspath(project_dir)}")
    print(f"🎬 Video:          {os.path.abspath(final_video_path)} ({file_size_mb} MB)")
    print(f"🖼️ Thumbnail:      {os.path.abspath(thumb_path)}")
    print(f"📋 Kit:            {os.path.abspath(kit_path)}")
    print("=" * 65 + "\n")

    return {
        "project_dir": project_dir,
        "video_path": final_video_path,
        "thumbnail_path": thumb_path,
        "kit_path": kit_path,
        "scene_images": built.get("scene_images", []),
        "blueprint": blueprint
    }
