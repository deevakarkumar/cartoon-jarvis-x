"""
AI Director & Universal Story Engine — What-If & Viral Animation Edition
Crafted using the exact storytelling formulas of top viral animation channels:
- Awaken (5.3M views): Second-person "You" perspective, rapid escalation, benchmark contrasts.
- IMAGINE (1.1M views): Emotional stakes, personal survival, cinematic world-building.
- Suddenly You (284K views): Strict Day-by-Day survival timeline (Day 1 -> Day 3 -> Day 21).

Supports:
1. Character Tales (e.g. "Story of a lazy man", habit & motivation lessons)
2. Survival Scenarios (e.g. "Locked in school for 30 days with crush", "Only man left on Earth")
3. Thought Experiments & Extreme Science (e.g. "Reaction time 10x", "500 IQ", "Can 2 people restart humanity")
4. Planetary Apocalypses (e.g. "Sun vanished", "Moon disappeared")

Timing Math:
- 10 to 13 words per 6-second clip.
- Ultra-short sentences (4-5 words average).
- Ellipses (...) for cinematic delivery pauses.
"""

import json
import os
import re
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from pathlib import Path
from dotenv import load_dotenv

# Automatically load .env from workspace root
_workspace_env = Path(__file__).resolve().parent.parent.parent / ".env"
if _workspace_env.exists():
    load_dotenv(str(_workspace_env))
else:
    load_dotenv()


class AIDirector:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = os.environ.get("GEMINI_API_KEY", "") if api_key is None else api_key

    def generate_full_package(
        self,
        topic: str,
        lang: str = "hi",
        duration_mode: str = "1min",
        aspect_ratio: str = "16:9"
    ) -> Dict[str, Any]:
        """
        Creates complete video script + YouTube metadata package.
        """
        lang = "hi" if "hi" in lang.lower() else "en"
        is_5min = ("5min" in duration_mode or "5" in str(duration_mode))

        # 1. Try Gemini API if key is present
        res = None
        if self.api_key:
            try:
                print(f"🧠 [AI Director] Querying Gemini for topic: '{topic}'...")
                res = self._call_gemini(topic, lang, is_5min, aspect_ratio)
                if res and "scenes" in res and len(res["scenes"]) > 0:
                    res["source"] = "gemini_ai"
            except Exception as e:
                print(f"⚠️ [AI Director] Gemini API call failed ({e}), falling back to Smart Offline Director.")

        # 2. Offline Smart Director fallback
        if not res or "scenes" not in res or len(res["scenes"]) == 0:
            res = self._generate_smart_offline(topic, lang, is_5min, aspect_ratio)

        # 3. Ensure universal defaults for primary_prop, science_metric, comparison_bars, crisis_alert
        if not res.get("primary_prop"):
            res["primary_prop"] = self._infer_primary_prop(topic)
        if not res.get("science_metric"):
            res["science_metric"] = self._infer_science_metric(topic)
        if not res.get("comparison_bars"):
            res["comparison_bars"] = self._infer_comparison_bars(topic)
        if not res.get("crisis_alert"):
            res["crisis_alert"] = self._infer_crisis_alert(topic)

        return res

    def _infer_primary_prop(self, topic: str) -> str:
        t = topic.lower()
        if any(w in t for w in ["dna", "genetic", "humanity", "restart", "repopulate", "species", "biology", "mutation", "2 people", "two people", "adam", "eve"]):
            return "dna_strand"
        elif any(w in t for w in ["planet", "world", "earth", "alone on earth", "last man", "space", "asteroid", "gravity", "cosmos"]):
            return "earth"
        elif any(w in t for w in ["phone", "mobile", "screen", "media", "scroll", "social", "instagram", "reels"]):
            return "phone_device"
        elif any(w in t for w in ["sport", "gym", "fitness", "run", "lift", "workout", "stamina"]):
            return "dumbbell"
        elif any(w in t for w in ["discipline", "motivation", "day one", "ready", "habit", "mindset"]):
            return "stopwatch"
        elif any(w in t for w in ["laptop", "code", "ai", "tech", "computer", "hack", "robot", "software"]):
            return "laptop"
        elif any(w in t for w in ["coffee", "tea", "drink", "cup", "caffeine", "morning"]):
            return "coffee_cup"
        elif any(w in t for w in ["money", "rich", "dollar", "cash", "gold", "bank", "wealth", "economy", "paisa"]):
            return "money_bag"
        elif any(w in t for w in ["sleep", "night", "alarm", "clock", "time", "hour", "rewind", "second"]):
            return "stopwatch"
        elif any(w in t for w in ["brain", "think", "mind", "iq", "memory", "psychology", "dimaag"]):
            return "brain_glow"
        elif any(w in t for w in ["heart", "cardio", "life", "pulse", "health", "blood"]):
            return "heart_pulse"
        elif any(w in t for w in ["read", "study", "exam", "school", "book", "learn", "padhai"]):
            return "book"
        elif any(w in t for w in ["poison", "toxic", "radiation", "danger", "deadly", "nuclear", "skull"]):
            return "skull_danger"
        elif any(w in t for w in ["fire", "volcano", "lava", "burn", "heat", "sun", "solar"]):
            return "flame"
        elif any(w in t for w in ["quantum", "physics", "element", "atom", "molecule", "science"]):
            return "atom"
        return "dna_strand" if "people" in t else "earth"

    def _infer_science_metric(self, topic: str) -> Dict[str, Any]:
        t = topic.lower()
        if any(w in t for w in ["dna", "genetic", "humanity", "restart", "repopulate", "2 people", "two people", "mutation"]):
            return {
                "title": "GENETIC DIVERSITY THRESHOLD",
                "subtitle": "INBREEDING DEPRESSION RISK",
                "from": 2.0,
                "to": 99.4,
                "unit": "%",
                "label_start": "Gen 1 (2%)",
                "label_mid": "Gen 2 (48%)",
                "label_end": "Gen 4 (99.4%)"
            }
        elif any(w in t for w in ["discipline", "motivation", "day one", "ready", "habit", "mindset"]):
            return {
                "title": "NEURAL MOTIVATION DECAY",
                "subtitle": "DOPAMINE NOVELTY vs HABIT FORMATION",
                "from": 100.0,
                "to": 0.0,
                "unit": "%",
                "label_start": "Day 1 (100%)",
                "label_mid": "Day 8 (16%)",
                "label_end": "Day 10 (0%)"
            }
        elif any(w in t for w in ["phone", "mobile", "screen", "scrolling", "social"]):
            return {
                "title": "CERVICAL SPINE STRESS",
                "subtitle": "HEAD TILT vs WEIGHT ON NECK",
                "from": 5.0,
                "to": 27.0,
                "unit": "kg",
                "label_start": "0 deg (5 kg)",
                "label_mid": "30 deg (18 kg)",
                "label_end": "60 deg (27 kg)"
            }
        elif any(w in t for w in ["sleep", "insomnia", "night", "wake"]):
            return {
                "title": "NEURO-TOXIN ACCUMULATION",
                "subtitle": "BETA-AMYLOID IN BRAIN TISSUE",
                "from": 5.0,
                "to": 92.0,
                "unit": "%",
                "label_start": "Day 1 (5%)",
                "label_mid": "Day 3 (45%)",
                "label_end": "Day 7 (92%)"
            }
        elif any(w in t for w in ["sport", "fitness", "gym", "run", "workout"]):
            return {
                "title": "MITOCHONDRIAL ATP OUTPUT",
                "subtitle": "CELLULAR ENERGY SYNTHESIS",
                "from": 100.0,
                "to": 260.0,
                "unit": "%",
                "label_start": "Base (100%)",
                "label_mid": "Week 2 (180%)",
                "label_end": "Week 4 (260%)"
            }
        elif any(w in t for w in ["money", "wealth", "economy", "bank", "dollar"]):
            return {
                "title": "CURRENCY PURCHASING POWER",
                "subtitle": "GLOBAL HYPER-INFLATION RATE",
                "from": 100.0,
                "to": 0.1,
                "unit": "%",
                "label_start": "Day 1 (100%)",
                "label_mid": "Day 10 (25%)",
                "label_end": "Day 30 (0.1%)"
            }
        elif any(w in t for w in ["alone", "only man", "last man", "isolation"]):
            return {
                "title": "PSYCHOLOGICAL ISOLATION INDEX",
                "subtitle": "CORTISOL vs COGNITIVE DECLINE",
                "from": 12.0,
                "to": 95.0,
                "unit": "pts",
                "label_start": "Week 1 (12)",
                "label_mid": "Month 1 (55)",
                "label_end": "Year 1 (95)"
            }
        elif any(w in t for w in ["space", "sun", "gravity", "orbit", "planet"]):
            return {
                "title": "GRAVITATIONAL FORCE EXPONENT",
                "subtitle": "ATMOSPHERIC ESCAPE VELOCITY",
                "from": 1.0,
                "to": 28.0,
                "unit": "G",
                "label_start": "1.0 G (11 km/s)",
                "label_mid": "8.0 G (32 km/s)",
                "label_end": "28.0 G (60 km/s)"
            }
        else:
            return {
                "title": "SYSTEM DEVIATION LIMIT",
                "subtitle": "CRITICAL HOMEOSTASIS INDEX",
                "from": 1.0,
                "to": 10.0,
                "unit": "x",
                "label_start": "Normal (1x)",
                "label_mid": "Threshold (4x)",
                "label_end": "Critical (10x)"
            }

    def _infer_comparison_bars(self, topic: str) -> List[Dict[str, Any]]:
        t = topic.lower()
        if any(w in t for w in ["dna", "genetic", "humanity", "restart", "repopulate", "2 people", "two people"]):
            return [
                {"label": "MINIMUM (50/500)", "v": 0.88, "color": "#7ee787"},
                {"label": "SURVIVORS (2)", "v": 0.04, "color": "#ff5555"}
            ]
        elif any(w in t for w in ["phone", "mobile", "screen", "scrolling"]):
            return [
                {"label": "UPRIGHT (0°)", "v": 0.18, "color": "#7ee787"},
                {"label": "BENT DOWN (60°)", "v": 0.95, "color": "#ff5555"}
            ]
        elif any(w in t for w in ["sleep", "insomnia", "night"]):
            return [
                {"label": "RESTED (8H)", "v": 0.15, "color": "#7ee787"},
                {"label": "NO SLEEP (72H)", "v": 0.92, "color": "#ff5555"}
            ]
        elif any(w in t for w in ["money", "wealth", "economy"]):
            return [
                {"label": "BASE STABILITY", "v": 0.90, "color": "#7ee787"},
                {"label": "HYPERINFLATION", "v": 0.02, "color": "#ff5555"}
            ]
        elif any(w in t for w in ["sport", "fitness", "gym"]):
            return [
                {"label": "SEDENTARY", "v": 0.25, "color": "#ffaa44"},
                {"label": "ATHLETIC", "v": 0.90, "color": "#7ee787"}
            ]
        else:
            return [
                {"label": "NORMAL RANGE", "v": 0.28, "color": "#7ee787"},
                {"label": "CRITICAL RISK", "v": 0.95, "color": "#ff5555"}
            ]

    def _infer_crisis_alert(self, topic: str) -> Dict[str, str]:
        t = topic.lower()
        if any(w in t for w in ["dna", "genetic", "humanity", "restart", "repopulate", "2 people", "two people"]):
            return {"label": "GENETIC BOTTLENECK", "value": "INBREEDING DEPRESSION"}
        elif any(w in t for w in ["phone", "mobile", "screen", "scrolling"]):
            return {"label": "NEURAL BURNOUT", "value": "DOPAMINE DYSFUNCTION"}
        elif any(w in t for w in ["sleep", "insomnia", "night"]):
            return {"label": "PSYCHOSIS THRESHOLD", "value": "HALLUCINATION ONSET"}
        elif any(w in t for w in ["money", "wealth", "economy"]):
            return {"label": "ECONOMIC ZERO", "value": "SYSTEM COLLAPSE"}
        elif any(w in t for w in ["alone", "only man", "last man"]):
            return {"label": "ISOLATION LIMIT", "value": "COGNITIVE DETACHMENT"}
        else:
            return {"label": "CRITICAL ALERT", "value": "LIMIT EXCEEDED"}

    # -------------------------------------------------------------
    # 1. ONLINE GEMINI 2.5 FLASH ENGINE ($0 Free Tier)
    # -------------------------------------------------------------
    def _call_gemini(self, topic: str, lang: str, is_5min: bool, aspect_ratio: str) -> Optional[Dict[str, Any]]:
        num_scenes = 16 if is_5min else 6
        target_lang_str = "Hindi (written in conversational Hinglish, punchy and engaging)" if lang == "hi" else "100% natural conversational English (zero Hindi or foreign words)"

        system_prompt = f"""
You are the master viral storyteller and cinematic director for top 2D stick-figure animation channels (like Awaken, IMAGINE, Suddenly You, What If, Ifverse).
Topic: "{topic}"
Target Language: {target_lang_str}
Scenes required: exactly {num_scenes} scenes.

CORE DIRECTING PRINCIPLES:
1. DYNAMIC NARRATIVE ARCHETYPES (DO NOT USE A COOKIE-CUTTER TEMPLATE!):
   Analyze the genre of "{topic}" and craft an authentic, captivating story structure:
   - FABLE / TRANSFORMATION (e.g., "Story of...", habit, success, failure):
     Scene 1: Inciting Reality (the relatable protagonist in their ordinary struggle)
     Scene 2: The Turning Point / Decision (the catalyst event)
     Scene 3: The Compounding Struggle (funny, painful, or inspiring small steps)
     Scene 4: The Critical Test / Breakthrough insight
     Scene 5: The Transformed Reality (victory, wealth, or newfound strength)
     Scene 6: The Powerful Moral & Call to Action (forces viewer into comments)
   - SURVIVAL / TIMELINE (e.g., "Locked in...", "Alone on Earth", "Restart humanity"):
     Scene 1: Day 1: The Shocking Event & Instant Isolation
     Scene 2: Day 3: The Scramble & New Rules of Survival
     Scene 3: Day 10: Compounding Challenge & Human Adaptation
     Scene 4: The Turning Point / Hidden Scientific Reality
     Scene 5: The Critical Crisis / Breaking Point
     Scene 6: The Climax Resolution & High-Stakes Question
   - HYPOTHETICAL WHAT-IF / SCIENCE (e.g., "What if no sleep", "What if dinosaurs lived"):
     Scene 1: Instant Shock (Hour 1)
     Scene 2: Immediate Escalation & Global Effect
     Scene 3: Compounding Chaos & Unforeseen Consequences
     Scene 4: The Hidden Science / Arithmetic Calculation
     Scene 5: The Extreme Climax / System Overload
     Scene 6: Mind-Blowing Dilemma Question

2. SCENE-BY-SCENE VISUAL & IMAGE DIRECTIVES:
   - For every single scene, write a distinct, rich "image_prompt" describing the background illustration.
   - Example image_prompt: "dusk city skyline with broken overgrown towers, warm orange sunset rays, two survivors standing on a rocky overlook, minimalist 2d vector anime style, 9:16 vertical".
   - Specify "characters": ["HERO"] for solo scenes, or ["HERO", "SECONDARY"] for dual interactions, or ["HERO", "DOC"] for science/medical scenes.
   - Specify "badge": Context-relevant on-screen stat (e.g. "DAY 01", "DOPAMINE: 0%", "POPULATION: 2", "100x HABIT", "12:00 AM").

3. PACING & SCRIPT RULES:
   - EXACTLY 10 to 14 words per scene narration! Never exceed 15 words.
   - Ultra-short punchy sentences (3-5 words each). Cut pauses to 2.7 words/second.
   - Second-person "You" or direct character narrative ("You wake up...", "What if you could...").
   - Concrete numbers, time benchmarks, or statistics.

4. STRICT LANGUAGE INTEGRITY:
   - If Target Language is English: 100% pure, natural, idiomatic English across ALL fields (titles, narration, SEO description, hashtags, pinned comment, thumbnail text). Absolutely NO Hindi words allowed!
   - If Target Language is Hindi: Natural conversational Hinglish YouTube style.

Allowed bg_styles:
"sports_stadium", "running_track", "gym_fitness", "outdoor_park", "office_workspace", "kitchen_cooking", "library_books", "bank_vault", "tech_server_room", "mountain_peak", "city_street", "cozy_bedroom", "living_room_couch", "school_classroom", "hospital_lab", "jungle_forest", "ocean_depths", "desert_dunes", "volcano_lava", "frozen_ice", "neon_city", "ruins_wasteland", "dusk_space", "nature_forest"

Allowed char_poses:
"running", "lifting", "celebrating", "exhausted", "reading", "typing", "idle", "pointing", "pointing_up", "thinking", "shrugging", "panicking", "hands_on_hips", "slouching", "lying", "explaining", "hands_on_head", "relaxed", "look_up"

Allowed expressions:
"normal", "shocked", "deadpan", "thinking", "screaming", "happy", "smirk", "jaw_drop", "sleepy"

Allowed props:
"dumbbell", "sports_ball", "trophy_cup", "running_shoes", "heart_pulse", "brain_glow", "laptop", "coffee_cup", "book", "target_bullseye", "lightbulb_idea", "stopwatch", "gold_medal", "phone_device", "money_bag", "alarm_clock", "sun", "earth", "moon", "clock", "campfire", "compass", "water_drop", "robot_ai", "dinosaur", "skull_danger", "dna_strand", "volcano", "question_mark"

Allowed sfx:
"drone_hit", "pop", "shatter", "ding", "whoosh", "title_boom", "power_down"

JSON Schema required:
{{
  "title": "Viral YouTube Video Title directly related to the topic",
  "language": "{lang}",
  "is_5min": {str(is_5min).lower()},
  "aspect_ratio": "{aspect_ratio}",
  "bg_style": "best primary background for the topic",
  "primary_prop": "dna_strand | earth | phone_device | laptop | dumbbell | coffee_cup | money_bag | stopwatch | brain_glow | heart_pulse | book | skull_danger | flame | atom",
  "science_metric": {{
    "title": "EXACT TECHNICAL METRIC (e.g. CERVICAL SPINE LOAD or INBREEDING DEPRESSION RISK)",
    "subtitle": "SUBTITLE (e.g. HEAD TILT vs PRESSURE or REPRODUCTIVE VIABILITY)",
    "from": 2.0,
    "to": 99.4,
    "unit": "%",
    "label_start": "Start (2%)",
    "label_mid": "Mid (48%)",
    "label_end": "Max (99.4%)"
  }},
  "comparison_bars": [
    {{"label": "SAFE / NORMAL", "v": 0.85, "color": "#7ee787"}},
    {{"label": "CRITICAL / CURRENT", "v": 0.05, "color": "#ff5555"}}
  ],
  "crisis_alert": {{
    "label": "CRISIS CODE (e.g. GENETIC BOTTLENECK or NEURAL OVERLOAD)",
    "value": "CRISIS DESCRIPTION (e.g. INBREEDING DEPRESSION or DOPAMINE BURNOUT)"
  }},
  "youtube_kit": {{
    "viral_titles": ["Title 1 (High CTR)", "Title 2 (Curiosity Gap)", "Title 3 (Shock Value)"],
    "seo_description": "2 paragraphs with high-ranking keywords, summary, and call to action",
    "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag9", "tag10"],
    "hashtags": ["#Shorts", "#Viral", "#Animation", "#Story"],
    "pinned_comment": "Engaging question in the target language asking viewers for their opinion",
    "thumbnail_hook": "2-4 WORDS CLICKBAIT TEXT",
    "thumbnail_prop": "prop_name"
  }},
  "scenes": [
    {{
      "scene_id": 1,
      "beat": "scene_beat_name",
      "narration": "Exact 10-14 words hook with dramatic pause...",
      "visual_description": "Clear cinematic description of the visual scene",
      "image_prompt": "cinematic illustration of [scene setting], [character action], [lighting], minimalist 2d vector anime style, 9:16 vertical",
      "char_pose": "active pose matching scene",
      "expression": "matching expression",
      "bg_style": "topic_matched_background",
      "characters": ["HERO"] or ["HERO", "SECONDARY"] or ["HERO", "DOC"],
      "badge": "2-4 words contextual stat e.g. POPULATION: 2 or SCREEN: 8.5H or DAY 01",
      "shake": 0.0,
      "props": [{{"type": "topic_matched_prop", "scale": 1.2}}],
      "sfx": "drone_hit"
    }}
  ]
}}
Return ONLY valid JSON.
"""
        payload = {
            "contents": [{"parts": [{"text": system_prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "responseMimeType": "application/json"
            }
        }

        # Candidate models ordered by speed and free quota reliability
        candidate_models = [
            "gemini-flash-lite-latest",
            "gemini-flash-latest",
            "gemini-2.5-flash",
            "gemini-pro-latest"
        ]

        for model_name in candidate_models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = json.loads(response.read().decode("utf-8"))
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    res = json.loads(text)
                    print(f"✅ [AI Director] Gemini model '{model_name}' successfully generated script!")
                    return res
            except Exception as e:
                print(f"⚠️ [AI Director] Gemini model '{model_name}' failed ({e}), trying next candidate...")
                continue

        return None

    # -------------------------------------------------------------
    # 2. SMART OFFLINE ENGINE ($0, 100% Local & Fast)
    # -------------------------------------------------------------
    def _generate_smart_offline(
        self,
        topic: str,
        lang: str,
        is_5min: bool,
        aspect_ratio: str
    ) -> Dict[str, Any]:
        t_low = topic.lower()

        # Archetype: Day One Films (Discipline, Mindset, Habit Transformation, Motivation)
        if any(w in t_low for w in ["discipline", "motivation", "day one", "dayone", "ready", "feel ready", "will fail you", "5 am", "5:00", "wake up early", "routine", "consistency", "grind", "mindset", "self-improvement", "subah uthna"]):
            niche = "dayone_transformation"
        # Archetype: Sports & Physical Fitness
        elif any(w in t_low for w in ["sport", "fitness", "exercise", "running", "gym", "workout", "athlete", "athletic", "football", "cricket", "basketball", "cardio", "stamina", "bodybuilding", "swimming", "game", "khel", "doudna", "vyayam"]):
            niche = "sports_fitness"
        # Archetype: Study, Learning, Exams & Focus
        elif any(w in t_low for w in ["study", "exam", "student", "learn", "padhai", "focus", "concentration", "book", "revision", "score", "grades"]):
            niche = "study_education"
        # Archetype: Food, Diet, Nutrition & Cooking
        elif any(w in t_low for w in ["food", "diet", "cooking", "eat", "nutrition", "sugar", "fast food", "junk food", "khana", "meal"]):
            niche = "food_nutrition"
        # Archetype: Work, Career, Office & Business
        elif any(w in t_low for w in ["office", "career", "job", "business", "boss", "interview", "salary", "startup", "colleague"]):
            niche = "work_career"
        # Archetype 1: Restart Humanity & Repopulation (Awaken style: 5.3M views)
        elif any(w in t_low for w in ["restart humanity", "2 people", "two people", "repopulate", "adam and eve", "restarting humanity"]):
            niche = "restart_humanity"
        # Archetype 2: Only Man / Solitude Survival (IMAGINE style: 1.1M views)
        elif any(w in t_low for w in ["only man", "only person", "alone on earth", "last man", "last human", "last person"]):
            niche = "only_man_earth"
        # Archetype 3: Character Tales & Everyday Stories (Lazy man, habits, success)
        elif any(w in t_low for w in ["lazy", "procrastinat", "aalsi", "habit", "routine", "story of a", "story of the", "broke", "motivation"]):
            niche = "character_story"
        # Archetype: Mobile Phone, Smartphone & Screen Addiction (Highly Viral)
        elif any(w in t_low for w in ["phone", "mobile", "smartphone", "screen", "scrolling", "social media", "instagram", "tiktok", "reels", "device", "cellphone", "screen time"]):
            niche = "mobile_phone"
        # Archetype 4: Survival Timelines & High-Stakes Relatable Drama (School lock-in, 30 Days)
        elif any(w in t_low for w in ["locked", "crush", "school", "30 days", "elevator", "bunker", "trapped"]):
            niche = "survival_scenario"
        # Archetype 3: Dinosaurs
        elif any(w in t_low for w in ["dinosaur", "t-rex", "jurassic", "extinct"]):
            niche = "dinosaurs"
        # Archetype 4: AI & Future Tech
        elif any(w in t_low for w in ["robot", "ai", "artificial intelligence", "tech", "computer", "future"]):
            niche = "tech_ai"
        # Archetype 5: Money & Wealth
        elif any(w in t_low for w in ["money", "rich", "paisa", "billionaire", "gold", "rupee", "dollar"]):
            niche = "money_economy"
        # Archetype 6: Ocean Abyss
        elif any(w in t_low for w in ["ocean", "sea", "underwater", "shark", "samundar", "deep sea"]):
            niche = "ocean"
        # Archetype 7: Biology & Emotions
        elif any(w in t_low for w in ["weep", "cry", "tear", "aansu", "rona"]):
            niche = "crying"
        elif any(w in t_low for w in ["sleep", "neend", "insomnia", "soye"]):
            niche = "sleep"
        # Archetype 8: Planetary / Space
        elif any(w in t_low for w in ["sun", "suraj", "solar"]):
            niche = "sun"
        elif any(w in t_low for w in ["moon", "chand", "lunar"]):
            niche = "moon"
        elif any(w in t_low for w in ["gravity", "gurutva", "earthquake", "volcano", "lava"]):
            niche = "physics"
        else:
            niche = "universal_what_if"

        builder = getattr(self, f"_build_{niche}", self._build_universal_what_if)
        result = builder(topic, lang, is_5min, aspect_ratio)
        result["source"] = "smart_offline_engine"
        return result

    # --- ARCHETYPE: SPORTS & ATHLETICS ---
    def _build_sports_fitness(self, topic: str, lang: str, is_5min: bool, aspect_ratio: str) -> Dict[str, Any]:
        if lang == "hi":
            title = "Khelne Se Dimaag Aur Shareer Me Kya Hota Hai?"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "Insaan ka shareer roz baara ghante baithe rehne ke liye nahi bana tha.",
                    "char_pose": "slouching",
                    "expression": "deadpan",
                    "shot_type": "standard",
                    "bg_style": "city_street",
                    "shake": 0.0,
                    "props": [{"type": "phone_device", "scale": 1.1}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "action_burst",
                    "narration": "Jaise hi aap track par daudte hain... aapka heart rate achanak tezi se badhta hai!",
                    "char_pose": "running",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "running_track",
                    "shake": 0.0,
                    "props": [{"type": "running_shoes", "scale": 1.1}],
                    "sfx": "whoosh"
                },
                {
                    "scene_id": 3,
                    "beat": "brain_science",
                    "narration": "Bees minute ke andar... dimaag me dopamine aur BDNF memory proteins release hote hain.",
                    "char_pose": "pointing_up",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "outdoor_park",
                    "shake": 0.0,
                    "props": [{"type": "brain_glow", "scale": 1.2}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 4,
                    "beat": "muscle_power",
                    "narration": "Aapki muscle fibers toot-ti hain... aur shareer unhe pehle se do guna mazboot banata hai.",
                    "char_pose": "lifting",
                    "expression": "thinking",
                    "shot_type": "standard",
                    "bg_style": "gym_fitness",
                    "shake": 1.0,
                    "props": [{"type": "dumbbell", "scale": 1.2}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 5,
                    "beat": "vitality_shift",
                    "narration": "Thakan khatam ho jaati hai. Stress gayab, aur energy poore din high rehti hai.",
                    "char_pose": "exhausted",
                    "expression": "normal",
                    "shot_type": "standard",
                    "bg_style": "sports_stadium",
                    "shake": 0.0,
                    "props": [{"type": "heart_pulse", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 6,
                    "beat": "victory_cta",
                    "narration": "Sports sirf game nahi, jeetne ki aadat hai. Aaj hi ground me kadam rakhein!",
                    "char_pose": "celebrating",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "sports_stadium",
                    "shake": 0.0,
                    "props": [{"type": "trophy_cup", "scale": 1.2}],
                    "sfx": "title_boom"
                }
            ]
            viral_titles = [
                "Sports Se Dimaag Me Kya Hota Hai?! 🏃",
                "Khelne Ke 30 Minute Baad Ka Sach 😱",
                "Why Athletes Brains Work 2x Faster!"
            ]
            thumb_hook = "KHEL KA ASLI SACH?!"
            thumb_prop = "trophy_cup"
            pinned = "Aapka sabse favorite sport kaun sa hai? Niche comment karein! 👇"
            seo_desc = "Janiye kaise daily 30 minute sports ya exercise aapke dimaag aur energy ko poori tarah badal deti hai.\n\n#Sports #Fitness #Motivation #Health #HindiShorts"
        else:
            title = "What 30 Minutes of Sports Does to Your Brain"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "Your body was never designed to sit in a chair twelve hours every day.",
                    "char_pose": "slouching",
                    "expression": "deadpan",
                    "shot_type": "standard",
                    "bg_style": "city_street",
                    "shake": 0.0,
                    "props": [{"type": "phone_device", "scale": 1.1}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "action_burst",
                    "narration": "The moment you sprint on the track... your heart rate surges immediately!",
                    "char_pose": "running",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "running_track",
                    "shake": 0.0,
                    "props": [{"type": "running_shoes", "scale": 1.1}],
                    "sfx": "whoosh"
                },
                {
                    "scene_id": 3,
                    "beat": "brain_science",
                    "narration": "Within twenty minutes, your brain releases massive dopamine and BDNF neuro-growth proteins.",
                    "char_pose": "pointing_up",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "outdoor_park",
                    "shake": 0.0,
                    "props": [{"type": "brain_glow", "scale": 1.2}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 4,
                    "beat": "muscle_power",
                    "narration": "Microscopic muscle fibers break down... forcing your entire body to rebuild stronger.",
                    "char_pose": "lifting",
                    "expression": "thinking",
                    "shot_type": "standard",
                    "bg_style": "gym_fitness",
                    "shake": 1.0,
                    "props": [{"type": "dumbbell", "scale": 1.2}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 5,
                    "beat": "vitality_shift",
                    "narration": "Exhaustion melts away. Your focus doubles, and your daily stress collapses.",
                    "char_pose": "exhausted",
                    "expression": "normal",
                    "shot_type": "standard",
                    "bg_style": "sports_stadium",
                    "shake": 0.0,
                    "props": [{"type": "heart_pulse", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 6,
                    "beat": "victory_cta",
                    "narration": "Discipline beats motivation every time. Step onto the field today!",
                    "char_pose": "celebrating",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "sports_stadium",
                    "shake": 0.0,
                    "props": [{"type": "trophy_cup", "scale": 1.2}],
                    "sfx": "title_boom"
                }
            ]
            viral_titles = [
                "What 30 Minutes of Sports Does to Your Brain?! 🏃",
                "The Body Transformation 99% of People Ignore",
                "Why Highly Successful People Play Sports Every Day"
            ]
            thumb_hook = "30 MIN TRANSFORM?!"
            thumb_prop = "trophy_cup"
            pinned = "What is your favorite sport or activity to stay active? Comment below! 👇"
            seo_desc = "Discover how 30 minutes of physical sports transforms your brain chemistry, heart health, and energy levels.\n\n#Sports #Fitness #Motivation #Health #ViralShorts"

        return {
            "title": title,
            "topic": topic,
            "language": lang,
            "is_5min": is_5min,
            "aspect_ratio": aspect_ratio,
            "bg_style": "sports_stadium",
            "youtube_kit": {
                "viral_titles": viral_titles,
                "seo_description": seo_desc,
                "tags": ["importance of sports", "sports motivation", "fitness benefits", "brain on sports", "workout transformation"],
                "hashtags": ["#Shorts", "#Sports", "#Fitness", "#Motivation"],
                "pinned_comment": pinned,
                "thumbnail_hook": thumb_hook,
                "thumbnail_prop": thumb_prop
            },
            "scenes": scenes
        }

    # --- ARCHETYPE: DAY ONE FILMS (Discipline Over Motivation / Mindset) ---
    def _build_dayone_transformation(self, topic: str, lang: str, is_5min: bool, aspect_ratio: str) -> Dict[str, Any]:
        if lang == "hi":
            title = "Motivation Will Fail You: Discipline Is Everything"
            if is_5min:
                # 16-Scene 5-Minute Epic Narrative (Day One Films + Style 2A Studio Tech)
                scenes = [
                    # CHAPTER 1: THE NOVELTY SPARK & THE DOPAMINE TRAP
                    {
                        "scene_id": 1,
                        "beat": "the_spark",
                        "narration": "Raat ke 1:00 baje. Ek motivational video dekhte hi dopamine 100% ho gaya... Kal subah 5:00!",
                        "char_pose": "lying",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "dayone_bedroom",
                        "props": [{"type": "alarm_clock", "scale": 1.2}],
                        "sfx": "drone_hit",
                        "day_banner": "NIGHT 0",
                        "motivation_pct": 100,
                        "aura": 1.0,
                        "clock_time": "01:00",
                        "in_scene_text": "tomorrow. 5:00."
                    },
                    {
                        "scene_id": 2,
                        "beat": "the_honeymoon_run",
                        "narration": "Day 1. 5:00 AM baji aur aap sadak par tezi se daud pade... aag jaisi sunheri energy ke sath.",
                        "char_pose": "running",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "dayone_running_street",
                        "sfx": "whoosh",
                        "day_banner": "DAY 1",
                        "motivation_pct": 100,
                        "aura": 1.0,
                        "in_scene_text": "5:00 RUN"
                    },
                    {
                        "scene_id": 3,
                        "beat": "studio_dopamine_curve",
                        "narration": "Lekin neuro-science ka ek kadwa sach hai: Dopamine ka yeh high-spike agle 7 din me 84% gir jata hai.",
                        "char_pose": "pointing",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "sfx": "ding",
                        "bar_chart": {
                            "title": "NEURAL MOTIVATION DECAY",
                            "bars": [
                                {"label": "Day 1", "value": 100, "color": "#06b6d4"},
                                {"label": "Day 3", "value": 75, "color": "#38bdf8"},
                                {"label": "Day 8", "value": 16, "color": "#f59e0b"},
                                {"label": "Day 10", "value": 0, "color": "#ef4444"}
                            ]
                        },
                        "stage_badge": {"num": 1, "title": "THE DOPAMINE DELUSION"}
                    },
                    {
                        "scene_id": 4,
                        "beat": "the_gym_high",
                        "narration": "Day 3. Gym me heavy weights uthate hue aisa laga ki duniya ki koi taakat aapko nahi rok sakti.",
                        "char_pose": "lifting",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "dayone_gym",
                        "props": [{"type": "dumbbell", "scale": 1.3}],
                        "sfx": "pop",
                        "day_banner": "DAY 3",
                        "motivation_pct": 75,
                        "aura": 0.75,
                        "in_scene_text": "NO EXCUSES"
                    },
                    # CHAPTER 2: THE CRASH & THE RESISTANCE DEMON
                    {
                        "scene_id": 5,
                        "beat": "the_depletion_slump",
                        "narration": "Day 8. Motivation gir kar 16% reh gaya. Desk par padhai karna geeli mitti me chalne jaisa laga.",
                        "char_pose": "slouching",
                        "expression": "exhausted",
                        "shot_type": "standard",
                        "bg_style": "dayone_study_desk",
                        "props": [{"type": "book", "scale": 1.1}],
                        "sfx": "pop",
                        "day_banner": "DAY 8",
                        "motivation_pct": 16,
                        "aura": 0.0,
                        "dark_bags": True,
                        "in_scene_text": "MOTIVATION 16%"
                    },
                    {
                        "scene_id": 6,
                        "beat": "studio_amateur_trap",
                        "narration": "Yahi 99 percent log haar maante hain: Kyunki wo 'ready feel' hone ka intezaar karte hain.",
                        "char_pose": "explaining",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "sfx": "shatter",
                        "comparison_split": {
                            "left": {"title": "99% AMATEUR TRAP", "points": ["Wait for inspiration", "Feelings dictate action", "Quit when excitement fades"]},
                            "right": {"title": "1% DISCIPLINE FORMULA", "points": ["Scheduled execution", "Feelings follow action", "Identity-driven daily system"]}
                        },
                        "stage_badge": {"num": 2, "title": "DISRUPTING THE ILLUSION"}
                    },
                    {
                        "scene_id": 7,
                        "beat": "the_crash_and_demon",
                        "narration": "Day 10. Alarm 5:07. Motivation zero. Andhere se Shadow Demon bola: Kal jab feel hoga tab shuru karna...",
                        "char_pose": "lying",
                        "expression": "exhausted",
                        "shot_type": "standard",
                        "bg_style": "dayone_bedroom",
                        "sfx": "shatter",
                        "day_banner": "DAY 10",
                        "motivation_pct": 0,
                        "aura": 0.0,
                        "dark_bags": True,
                        "clock_time": "05:07",
                        "shadow_demon": True,
                        "whisper_text": "wait till you feel it again..."
                    },
                    {
                        "scene_id": 8,
                        "beat": "studio_resistance_gauge",
                        "narration": "Psychology isse Resistance kehti hai—jab dimag energy bachane ke liye sabse zyada jhooth bolta hai.",
                        "char_pose": "thinking",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_dark",
                        "sfx": "ding",
                        "circular_gauge": {"value": 98, "label": "RESISTANCE PEAK", "unit": "%"},
                        "stage_badge": {"num": 3, "title": "UNVEILING THE MECHANISM"}
                    },
                    # CHAPTER 3: THE COLD PIVOT (THE 5:01 AM DECISION)
                    {
                        "scene_id": 9,
                        "beat": "the_discipline_decision",
                        "narration": "5:01 AM. Bina kisi aura ya excitement ke... aap bistar se uth khade hue. Demon dekhta hi reh gaya!",
                        "char_pose": "standing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "dayone_bedroom",
                        "sfx": "ding",
                        "day_banner": "5:01 AM",
                        "motivation_pct": 0,
                        "aura": 0.0,
                        "clock_time": "05:01",
                        "shadow_demon": True,
                        "whisper_text": "...what are you doing?"
                    },
                    {
                        "scene_id": 10,
                        "beat": "the_dragging_grind",
                        "narration": "Day 11. Thake hue shareer ko kheenchkar sadak par le gaye. Discipline wahi hai jab motivation mar jata hai.",
                        "char_pose": "running",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "dayone_running_street",
                        "sfx": "whoosh",
                        "day_banner": "DAY 11",
                        "motivation_pct": 10,
                        "aura": 0.0,
                        "fatigue_figure": True,
                        "in_scene_text": "Discipline is what keeps you going"
                    },
                    {
                        "scene_id": 11,
                        "beat": "studio_identity_shift",
                        "narration": "Discipline feelings par nahi chalta—yeh ek contract hai jo aapne khud se kiya tha.",
                        "char_pose": "pointing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "sfx": "pop",
                        "glass_card": {
                            "title": "THE IDENTITY CONTRACT",
                            "subtitle": "You do not rise to your goals; you fall to the level of your daily systems."
                        }
                    },
                    # CHAPTER 4: THE COMPOUNDING MACHINE
                    {
                        "scene_id": 12,
                        "beat": "the_automatic_routine",
                        "narration": "Day 21. Subah uthna ab jang nahi rahi. Routine dimaag ke neural pathways me lock ho chuka tha.",
                        "char_pose": "typing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "dayone_study_desk",
                        "day_banner": "DAY 21",
                        "motivation_pct": 25,
                        "aura": 0.2,
                        "in_scene_text": "AUTOMATIC ROUTINE"
                    },
                    {
                        "scene_id": 13,
                        "beat": "the_gym_compound",
                        "narration": "Day 45. Gym me weights bina soch-vichaar ke uthne lage. Thakan ab shakti me badal chuki thi.",
                        "char_pose": "lifting",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "dayone_gym",
                        "props": [{"type": "dumbbell", "scale": 1.3}],
                        "sfx": "pop",
                        "day_banner": "DAY 45",
                        "motivation_pct": 38,
                        "aura": 0.35,
                        "in_scene_text": "COMPOUND POWER"
                    },
                    {
                        "scene_id": 14,
                        "beat": "the_breakthrough_graph",
                        "narration": "Day 62. Suraj nikalte hi motivation khud laut aaya. Kyunki aap 'ready' hone ka intezaar nahi karte!",
                        "char_pose": "standing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "dayone_sunrise",
                        "sfx": "title_boom",
                        "day_banner": "DAY 62",
                        "motivation_pct": 47,
                        "aura": 0.5,
                        "discipline_graph": True
                    },
                    # CHAPTER 5: THE ULTIMATE TRUTH & DISCUSSION ELEVATION
                    {
                        "scene_id": 15,
                        "beat": "studio_master_transformation",
                        "narration": "Motivation ek mehman hai jo aakar chala jata hai. Lekin Discipline wo malik hai jo ghar banata hai.",
                        "char_pose": "cheer",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "sfx": "ding",
                        "stage_badge": {"num": 4, "title": "THE ULTIMATE TRUTH"}
                    },
                    {
                        "scene_id": 16,
                        "beat": "the_discussion_cta",
                        "narration": "Aapki life ki aisi kaunsi aadat hai jo aapne Day 8 par chhod di? Niche comment me zaroor batayein!",
                        "char_pose": "pointing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_dark",
                        "sfx": "title_boom",
                        "stage_badge": {"num": 5, "title": "THE COMMUNITY CHALLENGE"}
                    }
                ]
            else:
                # 8-Scene Benchmark Short (60s)
                scenes = [
                    {
                        "scene_id": 1,
                        "beat": "the_spark",
                        "narration": "Raat ke 1:00 baje. Ek motivational video dekhte hi dopamine 100% ho gaya... Kal subah 5:00!",
                        "char_pose": "lying",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "dayone_bedroom",
                        "props": [{"type": "alarm_clock", "scale": 1.2}],
                        "sfx": "drone_hit",
                        "day_banner": "NIGHT 0",
                        "motivation_pct": 100,
                        "aura": 1.0,
                        "clock_time": "01:00",
                        "in_scene_text": "tomorrow. 5:00."
                    },
                    {
                        "scene_id": 2,
                        "beat": "the_honeymoon_run",
                        "narration": "Day 1. 5:00 AM baji aur aap sadak par tezi se daud pade... aag jaisi sunheri energy ke sath.",
                        "char_pose": "running",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "dayone_running_street",
                        "sfx": "whoosh",
                        "day_banner": "DAY 1",
                        "motivation_pct": 100,
                        "aura": 1.0,
                        "in_scene_text": "5:00 RUN"
                    },
                    {
                        "scene_id": 3,
                        "beat": "the_gym_high",
                        "narration": "Day 3. Gym me heavy weights uthate hue aisa laga ki duniya ki koi taakat aapko nahi rok sakti.",
                        "char_pose": "lifting",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "dayone_gym",
                        "props": [{"type": "dumbbell", "scale": 1.3}],
                        "sfx": "pop",
                        "day_banner": "DAY 3",
                        "motivation_pct": 75,
                        "aura": 0.75,
                        "in_scene_text": "NO EXCUSES"
                    },
                    {
                        "scene_id": 4,
                        "beat": "the_depletion_slump",
                        "narration": "Day 8. Motivation gir kar 16% reh gaya. Desk par padhai karna geeli mitti me chalne jaisa laga.",
                        "char_pose": "slouching",
                        "expression": "exhausted",
                        "shot_type": "standard",
                        "bg_style": "dayone_study_desk",
                        "props": [{"type": "book", "scale": 1.1}],
                        "sfx": "pop",
                        "day_banner": "DAY 8",
                        "motivation_pct": 16,
                        "aura": 0.0,
                        "dark_bags": True,
                        "in_scene_text": "MOTIVATION 16%"
                    },
                    {
                        "scene_id": 5,
                        "beat": "the_crash_and_demon",
                        "narration": "Day 10. Alarm 5:07. Motivation zero. Andhere se Shadow Demon bola: Kal jab feel hoga tab shuru karna...",
                        "char_pose": "lying",
                        "expression": "exhausted",
                        "shot_type": "standard",
                        "bg_style": "dayone_bedroom",
                        "sfx": "shatter",
                        "day_banner": "DAY 10",
                        "motivation_pct": 0,
                        "aura": 0.0,
                        "dark_bags": True,
                        "clock_time": "05:07",
                        "shadow_demon": True,
                        "whisper_text": "wait till you feel it again..."
                    },
                    {
                        "scene_id": 6,
                        "beat": "the_discipline_decision",
                        "narration": "5:01 AM. Bina kisi aura ya excitement ke... aap bistar se uth khade hue. Demon dekhta hi reh gaya!",
                        "char_pose": "standing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "dayone_bedroom",
                        "sfx": "ding",
                        "day_banner": "5:01 AM",
                        "motivation_pct": 0,
                        "aura": 0.0,
                        "clock_time": "05:01",
                        "shadow_demon": True,
                        "whisper_text": "...what are you doing?"
                    },
                    {
                        "scene_id": 7,
                        "beat": "the_dragging_grind",
                        "narration": "Day 11. Thake hue shareer ko kheenchkar sadak par le gaye. Discipline wahi hai jab motivation mar jata hai.",
                        "char_pose": "running",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "dayone_running_street",
                        "sfx": "whoosh",
                        "day_banner": "DAY 11",
                        "motivation_pct": 10,
                        "aura": 0.0,
                        "fatigue_figure": True,
                        "in_scene_text": "Discipline is what keeps you going"
                    },
                    {
                        "scene_id": 8,
                        "beat": "the_breakthrough_graph",
                        "narration": "Day 62. Suraj nikalte hi motivation khud laut aaya. Kyunki aap 'ready' hone ka intezaar nahi karte!",
                        "char_pose": "standing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "dayone_sunrise",
                        "sfx": "title_boom",
                        "day_banner": "DAY 62",
                        "motivation_pct": 47,
                        "aura": 0.5,
                        "discipline_graph": True
                    }
                ]
            seo_desc = "Why waiting for motivation will ruin your life. The true psychology of self-discipline explained through Day One Films animation style. Discover how to push through resistance when motivation drops to 0%."
            pinned = "Kya aap bhi 'ready feel' hone ka intezaar karte hain? Comment me batayein!"
            thumb_hook = "MOTIVATION LIES!"
            thumb_prop = "stopwatch"
        else:
            title = "Motivation Will Fail You: Discipline Is Everything"
            if is_5min:
                # 16-Scene 5-Minute Epic Narrative (English)
                scenes = [
                    {
                        "scene_id": 1,
                        "beat": "the_spark",
                        "narration": "1:00 AM. A late-night speech hits your screen. Dopamine spikes to 100%. Tomorrow. 5:00 AM.",
                        "char_pose": "lying",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "dayone_bedroom",
                        "props": [{"type": "alarm_clock", "scale": 1.2}],
                        "sfx": "drone_hit",
                        "day_banner": "NIGHT 0",
                        "motivation_pct": 100,
                        "aura": 1.0,
                        "clock_time": "01:00",
                        "in_scene_text": "tomorrow. 5:00."
                    },
                    {
                        "scene_id": 2,
                        "beat": "the_honeymoon_run",
                        "narration": "Day 1. The alarm rings and you fly into the dark streets... glowing with pure golden motivation.",
                        "char_pose": "running",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "dayone_running_street",
                        "sfx": "whoosh",
                        "day_banner": "DAY 1",
                        "motivation_pct": 100,
                        "aura": 1.0,
                        "in_scene_text": "5:00 RUN"
                    },
                    {
                        "scene_id": 3,
                        "beat": "studio_dopamine_curve",
                        "narration": "Neuroscience reveals a brutal truth: Dopamine spikes crash by 84% within the first seven days.",
                        "char_pose": "pointing",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "sfx": "ding",
                        "bar_chart": {
                            "title": "NEURAL MOTIVATION DECAY",
                            "bars": [
                                {"label": "Day 1", "value": 100, "color": "#06b6d4"},
                                {"label": "Day 3", "value": 75, "color": "#38bdf8"},
                                {"label": "Day 8", "value": 16, "color": "#f59e0b"},
                                {"label": "Day 10", "value": 0, "color": "#ef4444"}
                            ]
                        },
                        "stage_badge": {"num": 1, "title": "THE NOVELTY ILLUSION"}
                    },
                    {
                        "scene_id": 4,
                        "beat": "the_gym_high",
                        "narration": "Day 3. Crushing iron at the gym. You feel completely invincible, like nothing can ever stop you.",
                        "char_pose": "lifting",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "dayone_gym",
                        "props": [{"type": "dumbbell", "scale": 1.3}],
                        "sfx": "pop",
                        "day_banner": "DAY 3",
                        "motivation_pct": 75,
                        "aura": 0.75,
                        "in_scene_text": "NO EXCUSES"
                    },
                    {
                        "scene_id": 5,
                        "beat": "the_depletion_slump",
                        "narration": "Day 8. Motivation plummets to 16%. Studying feels like dragging heavy bricks through wet cement.",
                        "char_pose": "slouching",
                        "expression": "exhausted",
                        "shot_type": "standard",
                        "bg_style": "dayone_study_desk",
                        "props": [{"type": "book", "scale": 1.1}],
                        "sfx": "pop",
                        "day_banner": "DAY 8",
                        "motivation_pct": 16,
                        "aura": 0.0,
                        "dark_bags": True,
                        "in_scene_text": "MOTIVATION 16%"
                    },
                    {
                        "scene_id": 6,
                        "beat": "studio_amateur_trap",
                        "narration": "This is where ninety-nine percent fail: They wait until they 'feel like it' to take action.",
                        "char_pose": "explaining",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "sfx": "shatter",
                        "comparison_split": {
                            "left": {"title": "99% AMATEUR TRAP", "points": ["Wait for inspiration", "Feelings dictate action", "Quit when excitement dies"]},
                            "right": {"title": "1% DISCIPLINE FORMULA", "points": ["Scheduled execution", "Action creates feeling", "Identity-driven daily system"]}
                        },
                        "stage_badge": {"num": 2, "title": "SHATTERING ASSUMPTIONS"}
                    },
                    {
                        "scene_id": 7,
                        "beat": "the_crash_and_demon",
                        "narration": "Day 10. Alarm 5:07. Motivation 0%. From the shadows, the Demon whispers: Wait till you feel ready...",
                        "char_pose": "lying",
                        "expression": "exhausted",
                        "shot_type": "standard",
                        "bg_style": "dayone_bedroom",
                        "sfx": "shatter",
                        "day_banner": "DAY 10",
                        "motivation_pct": 0,
                        "aura": 0.0,
                        "dark_bags": True,
                        "clock_time": "05:07",
                        "shadow_demon": True,
                        "whisper_text": "wait till you feel it again..."
                    },
                    {
                        "scene_id": 8,
                        "beat": "studio_resistance_gauge",
                        "narration": "Psychologists call this Resistance—the friction your brain generates when dopamine runs completely dry.",
                        "char_pose": "thinking",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_dark",
                        "sfx": "ding",
                        "circular_gauge": {"value": 98, "label": "RESISTANCE PEAK", "unit": "%"},
                        "stage_badge": {"num": 3, "title": "UNVEILING THE FRICTION"}
                    },
                    {
                        "scene_id": 9,
                        "beat": "the_discipline_decision",
                        "narration": "5:01 AM. Without feeling ready, without any excitement... you step out of bed. The Demon freezes.",
                        "char_pose": "standing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "dayone_bedroom",
                        "sfx": "ding",
                        "day_banner": "5:01 AM",
                        "motivation_pct": 0,
                        "aura": 0.0,
                        "clock_time": "05:01",
                        "shadow_demon": True,
                        "whisper_text": "...what are you doing?"
                    },
                    {
                        "scene_id": 10,
                        "beat": "the_dragging_grind",
                        "narration": "Day 11. Dragging your exhausted body into the dawn. Discipline is moving forward when motivation is dead.",
                        "char_pose": "running",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "dayone_running_street",
                        "sfx": "whoosh",
                        "day_banner": "DAY 11",
                        "motivation_pct": 10,
                        "aura": 0.0,
                        "fatigue_figure": True,
                        "in_scene_text": "Discipline is what keeps you going"
                    },
                    {
                        "scene_id": 11,
                        "beat": "studio_identity_shift",
                        "narration": "Discipline doesn't consult your feelings. It is an unbreakable contract made with your future self.",
                        "char_pose": "pointing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "sfx": "pop",
                        "glass_card": {
                            "title": "THE IDENTITY CONTRACT",
                            "subtitle": "You do not rise to your goals; you fall to the level of your daily systems."
                        }
                    },
                    {
                        "scene_id": 12,
                        "beat": "the_automatic_routine",
                        "narration": "Day 21. Waking up is no longer a battle. The habit has hardwired directly into your nervous system.",
                        "char_pose": "typing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "dayone_study_desk",
                        "day_banner": "DAY 21",
                        "motivation_pct": 25,
                        "aura": 0.2,
                        "in_scene_text": "AUTOMATIC ROUTINE"
                    },
                    {
                        "scene_id": 13,
                        "beat": "the_gym_compound",
                        "narration": "Day 45. Moving iron with effortless execution. Fatigue has compounded into unbreakable resilience.",
                        "char_pose": "lifting",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "dayone_gym",
                        "props": [{"type": "dumbbell", "scale": 1.3}],
                        "sfx": "pop",
                        "day_banner": "DAY 45",
                        "motivation_pct": 38,
                        "aura": 0.35,
                        "in_scene_text": "COMPOUND POWER"
                    },
                    {
                        "scene_id": 14,
                        "beat": "the_breakthrough_graph",
                        "narration": "Day 62. The sunrise hits the road. Motivation returned... because you stopped waiting to feel like it.",
                        "char_pose": "standing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "dayone_sunrise",
                        "sfx": "title_boom",
                        "day_banner": "DAY 62",
                        "motivation_pct": 47,
                        "aura": 0.5,
                        "discipline_graph": True
                    },
                    {
                        "scene_id": 15,
                        "beat": "studio_master_transformation",
                        "narration": "Motivation is an unreliable visitor. Discipline is the master that builds the empire.",
                        "char_pose": "cheer",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "sfx": "ding",
                        "stage_badge": {"num": 4, "title": "THE ULTIMATE TRUTH"}
                    },
                    {
                        "scene_id": 16,
                        "beat": "the_discussion_cta",
                        "narration": "What is the ONE habit you quit on Day 8 because you didn't feel ready? Tell us below.",
                        "char_pose": "pointing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_dark",
                        "sfx": "title_boom",
                        "stage_badge": {"num": 5, "title": "COMMUNITY DEBATE"}
                    }
                ]
            else:
                scenes = [
                    {
                        "scene_id": 1,
                        "beat": "the_spark",
                        "narration": "1:00 AM. A late-night motivational speech hits your screen. Dopamine spikes to 100%. Tomorrow. 5:00 AM.",
                        "char_pose": "lying",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "dayone_bedroom",
                        "props": [{"type": "alarm_clock", "scale": 1.2}],
                        "sfx": "drone_hit",
                        "day_banner": "NIGHT 0",
                        "motivation_pct": 100,
                        "aura": 1.0,
                        "clock_time": "01:00",
                        "in_scene_text": "tomorrow. 5:00."
                    },
                    {
                        "scene_id": 2,
                        "beat": "the_honeymoon_run",
                        "narration": "Day 1. The alarm rings and you fly into the dark streets... glowing with pure motivation.",
                        "char_pose": "running",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "dayone_running_street",
                        "sfx": "whoosh",
                        "day_banner": "DAY 1",
                        "motivation_pct": 100,
                        "aura": 1.0,
                        "in_scene_text": "5:00 RUN"
                    },
                    {
                        "scene_id": 3,
                        "beat": "the_gym_high",
                        "narration": "Day 3. Crushing iron at the gym. You feel completely invincible, like nothing can stop you.",
                        "char_pose": "lifting",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "dayone_gym",
                        "props": [{"type": "dumbbell", "scale": 1.3}],
                        "sfx": "pop",
                        "day_banner": "DAY 3",
                        "motivation_pct": 75,
                        "aura": 0.75,
                        "in_scene_text": "NO EXCUSES"
                    },
                    {
                        "scene_id": 4,
                        "beat": "the_depletion_slump",
                        "narration": "Day 8. Motivation plummets to 16%. Studying feels like dragging heavy bricks through wet cement.",
                        "char_pose": "slouching",
                        "expression": "exhausted",
                        "shot_type": "standard",
                        "bg_style": "dayone_study_desk",
                        "props": [{"type": "book", "scale": 1.1}],
                        "sfx": "pop",
                        "day_banner": "DAY 8",
                        "motivation_pct": 16,
                        "aura": 0.0,
                        "dark_bags": True,
                        "in_scene_text": "MOTIVATION 16%"
                    },
                    {
                        "scene_id": 5,
                        "beat": "the_crash_and_demon",
                        "narration": "Day 10. Alarm 5:07. Motivation 0%. From the shadows, the Demon whispers: Wait till you feel ready...",
                        "char_pose": "lying",
                        "expression": "exhausted",
                        "shot_type": "standard",
                        "bg_style": "dayone_bedroom",
                        "sfx": "shatter",
                        "day_banner": "DAY 10",
                        "motivation_pct": 0,
                        "aura": 0.0,
                        "dark_bags": True,
                        "clock_time": "05:07",
                        "shadow_demon": True,
                        "whisper_text": "wait till you feel it again..."
                    },
                    {
                        "scene_id": 6,
                        "beat": "the_discipline_decision",
                        "narration": "5:01 AM. Without feeling ready, without any excitement... you step out of bed. The Demon freezes.",
                        "char_pose": "standing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "dayone_bedroom",
                        "sfx": "ding",
                        "day_banner": "5:01 AM",
                        "motivation_pct": 0,
                        "aura": 0.0,
                        "clock_time": "05:01",
                        "shadow_demon": True,
                        "whisper_text": "...what are you doing?"
                    },
                    {
                        "scene_id": 7,
                        "beat": "the_dragging_grind",
                        "narration": "Day 11. Dragging your exhausted body into the dawn. Discipline is moving forward when motivation is dead.",
                        "char_pose": "running",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "dayone_running_street",
                        "sfx": "whoosh",
                        "day_banner": "DAY 11",
                        "motivation_pct": 10,
                        "aura": 0.0,
                        "fatigue_figure": True,
                        "in_scene_text": "Discipline is what keeps you going"
                    },
                    {
                        "scene_id": 8,
                        "beat": "the_breakthrough_graph",
                        "narration": "Day 62. The sunrise hits the road. Motivation returned... because you stopped waiting to feel like it.",
                        "char_pose": "standing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "dayone_sunrise",
                        "sfx": "title_boom",
                        "day_banner": "DAY 62",
                        "motivation_pct": 47,
                        "aura": 0.5,
                        "discipline_graph": True
                    }
                ]
            seo_desc = "Why waiting for motivation will fail you. Master the compound formula of discipline over motivation. A frame-accurate breakdown inspired by Day One Films."
            pinned = "Do you wait until you 'feel ready'? Drop your thoughts below."
            thumb_hook = "MOTIVATION LIES!"
            thumb_prop = "stopwatch"
            seo_desc = "Why waiting for motivation will fail you. Master the compound formula of discipline over motivation. A frame-accurate breakdown inspired by Day One Films."
            pinned = "Do you wait until you 'feel ready'? Drop your thoughts below."
            thumb_hook = "MOTIVATION LIES!"
            thumb_prop = "stopwatch"

        return {
            "title": title,
            "topic": topic,
            "language": lang,
            "is_5min": is_5min,
            "aspect_ratio": aspect_ratio,
            "bg_style": "dayone_bedroom",
            "primary_prop": "stopwatch",
            "science_metric": {
                "title": "NEURAL MOTIVATION DECAY",
                "subtitle": "DOPAMINE NOVELTY vs HABIT FORMATION",
                "from": 100.0,
                "to": 0.0,
                "unit": "%",
                "label_start": "Day 1 (100%)",
                "label_mid": "Day 8 (16%)",
                "label_end": "Day 10 (0%)"
            },
            "comparison_bars": [
                {"label": "DISCIPLINE (HABIT)", "v": 0.94, "color": "#10b981"},
                {"label": "MOTIVATION (FEELING)", "v": 0.06, "color": "#ef4444"}
            ],
            "crisis_alert": {
                "label": "MOTIVATION COLLAPSE",
                "value": "RESISTANCE PEAK"
            },
            "youtube_kit": {
                "viral_titles": [
                    "Motivation Will Fail You. Discipline Won't.",
                    "Why Waiting To Feel Ready Destroys You",
                    "The Day You Stop Relying On Motivation"
                ],
                "seo_description": seo_desc,
                "tags": ["DayOneFilms", "Discipline", "Motivation", "Productivity", "Mindset", "SelfImprovement", "Habits", "ShortFilm", "Animation"],
                "hashtags": ["#Shorts", "#Discipline", "#Motivation", "#Mindset", "#DayOneFilms"],
                "pinned_comment": pinned,
                "thumbnail_hook": thumb_hook,
                "thumbnail_prop": thumb_prop
            },
            "scenes": scenes
        }

    # --- ARCHETYPE 1: CHARACTER STORY (e.g. Story of a Lazy Man) ---
    def _build_character_story(self, topic: str, lang: str, is_5min: bool, aspect_ratio: str) -> Dict[str, Any]:
        if lang == "hi":
            title = "The Secret Power of a Lazy Man"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "Subah 7:00 baje. Alarm 40 minute se baj raha hai... par aap hile bhi nahi.",
                    "char_pose": "lying",
                    "expression": "sleepy",
                    "shot_type": "standard",
                    "bg_style": "cozy_bedroom",
                    "shake": 0.0,
                    "props": [{"type": "alarm_clock", "scale": 1.2}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "character_flaw",
                    "narration": "Duniya aapko aalsi kehti hai. Par sach yeh hai... aapka dimaag energy bacha raha hai.",
                    "char_pose": "slouching",
                    "expression": "smirk",
                    "shot_type": "standard",
                    "bg_style": "cozy_bedroom",
                    "shake": 0.0,
                    "props": [{"type": "phone_device", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "the_crisis",
                    "narration": "Pahaad jaisa pending kaam. Aur sudden deadline... jo aapki neend uda deti hai!",
                    "char_pose": "panicking",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "living_room_couch",
                    "shake": 4.0,
                    "props": [],
                    "sfx": "shatter"
                },
                {
                    "scene_id": 4,
                    "beat": "the_lazy_genius",
                    "narration": "Kyunki aalsi log mehnat nahi karte... wo 5 ghante ka kaam 10 minute me nipatate hain.",
                    "char_pose": "explaining",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "living_room_couch",
                    "shake": 0.0,
                    "props": [{"type": "clock", "scale": 1.1}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 5,
                    "beat": "the_twist",
                    "narration": "Bill Gates ne ek baar kaha tha: Mushkil kaam ke liye hamesha ek aalsi insaan chuno.",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "shot_type": "standard",
                    "bg_style": "webcomic_light",
                    "shake": 0.0,
                    "props": [{"type": "money_bag", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 6,
                    "beat": "climax_cta",
                    "narration": "Toh kya aap aalsi hain... ya smart? Comment me sach batayein aur subscribe karein!",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "webcomic_light",
                    "shake": 0.0,
                    "props": [],
                    "sfx": "title_boom"
                }
            ]
            viral_titles = [
                "The Shocking Truth About Lazy People! 🛋️",
                "Why Being Lazy Might Mean You're a Genius!",
                "Story of a Lazy Man: The Ultimate Brain Hack"
            ]
            thumb_hook = "LAZY YA GENIUS?!"
            thumb_prop = "alarm_clock"
        else:
            title = "Story of a Lazy Man: The Genius Hack"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "Friday, 7:00 a.m. Your alarm has been ringing for 40 minutes... you haven't moved.",
                    "char_pose": "lying",
                    "expression": "sleepy",
                    "shot_type": "standard",
                    "bg_style": "cozy_bedroom",
                    "shake": 0.0,
                    "props": [{"type": "alarm_clock", "scale": 1.2}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "character_flaw",
                    "narration": "Everyone calls you lazy. But your brain has secretly discovered... the ultimate shortcut.",
                    "char_pose": "slouching",
                    "expression": "smirk",
                    "shot_type": "standard",
                    "bg_style": "cozy_bedroom",
                    "shake": 0.0,
                    "props": [{"type": "phone_device", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "the_crisis",
                    "narration": "Suddenly, a critical deadline drops. And for the first time... panic strikes!",
                    "char_pose": "panicking",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "living_room_couch",
                    "shake": 4.0,
                    "props": [],
                    "sfx": "shatter"
                },
                {
                    "scene_id": 4,
                    "beat": "the_lazy_genius",
                    "narration": "When forced to move... a lazy mind solves a five-hour task in twelve minutes.",
                    "char_pose": "explaining",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "living_room_couch",
                    "shake": 0.0,
                    "props": [{"type": "clock", "scale": 1.1}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 5,
                    "beat": "the_twist",
                    "narration": "Bill Gates famously said: Always hire a lazy person to do a difficult job.",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "shot_type": "standard",
                    "bg_style": "webcomic_light",
                    "shake": 0.0,
                    "props": [{"type": "money_bag", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 6,
                    "beat": "climax_cta",
                    "narration": "Work smarter... not harder. Are you truly lazy, or just efficient? Tell us below!",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "webcomic_light",
                    "shake": 0.0,
                    "props": [],
                    "sfx": "title_boom"
                }
            ]
            viral_titles = [
                "Why Being Lazy Actually Makes You Smarter! 🧠",
                "Story of a Lazy Man: The Brain Hack Nobody Tells You",
                "Are You Truly Lazy... Or Just High IQ?"
            ]
            thumb_hook = "LAZY GENIUS?!"
            thumb_prop = "alarm_clock"

        return {
            "title": title,
            "topic": topic,
            "language": lang,
            "is_5min": is_5min,
            "aspect_ratio": aspect_ratio,
            "bg_style": "cozy_bedroom",
            "youtube_kit": {
                "viral_titles": viral_titles,
                "seo_description": "Is being lazy secretly a sign of high efficiency? We explore the evolutionary science and psychology behind procrastination and genius!\n\n#Story #Psychology #Animation #Productivity #Shorts",
                "tags": ["story of a lazy man", "procrastination psychology", "productivity hacks", "stick figure animation", "viral shorts", "educational animation"],
                "hashtags": ["#Shorts", "#Motivation", "#Psychology", "#Viral"],
                "pinned_comment": "Aap din me kitne ghante aalsi feel karte hain? Honest answer comment karein! 👇",
                "thumbnail_hook": thumb_hook,
                "thumbnail_prop": thumb_prop
            },
            "scenes": scenes
        }

    # --- ARCHETYPE: SMARTPHONE & SCREEN ADDICTION ---
    def _build_mobile_phone(self, topic: str, lang: str, is_5min: bool, aspect_ratio: str) -> Dict[str, Any]:
        if lang == "hi":
            title = "The Smartphone Trap: How Screens Stole Our Life"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "Aapne phone uthaya sirf do minute ke liye... par achanak raat ke teen baj gaye!",
                    "char_pose": "slouching",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "cozy_bedroom",
                    "shake": 2.0,
                    "props": [{"type": "phone_device", "scale": 1.2}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "psychology_dopamine",
                    "narration": "Har ek notification dimaag me dopamine trigger karta hai. Bilkul ek pocket casino jaisa!",
                    "char_pose": "thinking",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "living_room_couch",
                    "shake": 0.0,
                    "props": [{"type": "phone_device", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "reality_check",
                    "narration": "Ek aam insaan din me 2,617 baar screen chhoota hai. Poori zindagi ke 11 saal!",
                    "char_pose": "explaining",
                    "expression": "normal",
                    "shot_type": "standard",
                    "bg_style": "living_room_couch",
                    "shake": 0.0,
                    "props": [{"type": "clock", "scale": 1.1}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 4,
                    "beat": "what_if_disappears",
                    "narration": "Agar 7 din ke liye phone gayab ho jaye... Day 1 par phantom vibration syndrome satayega.",
                    "char_pose": "panicking",
                    "expression": "screaming",
                    "shot_type": "standard",
                    "bg_style": "city_street",
                    "shake": 4.0,
                    "props": [{"type": "phone_device", "scale": 1.0}],
                    "sfx": "shatter"
                },
                {
                    "scene_id": 5,
                    "beat": "the_breakthrough",
                    "narration": "Lekin Day 4 par deep focus laut aayega. Asli duniya achanak shaant aur khubsurat lagegi.",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "city_street",
                    "shake": 0.0,
                    "props": [{"type": "sun", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 6,
                    "beat": "call_to_action",
                    "narration": "Aaj aapka screen time kitne ghante tha? Abhi check karein aur niche comment karein!",
                    "char_pose": "pointing_up",
                    "expression": "smirk",
                    "shot_type": "standard",
                    "bg_style": "cozy_bedroom",
                    "shake": 0.0,
                    "props": [{"type": "phone_device", "scale": 1.1}],
                    "sfx": "title_boom"
                }
            ]
            viral_titles = [
                "Kya Hoga Agar 7 Din Ke Liye Phone Chhin Jaye? 📱",
                "Smartphone: Aapke Dimaag Ka Pocket Casino",
                "How 2,617 Daily Screen Taps Stole 11 Years of Your Life"
            ]
            thumb_hook = "7 DIN NO PHONE?!"
            thumb_prop = "phone_device"
        else:
            title = "The Smartphone Trap: How Screens Stole Our Life"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "You unlocked your phone for just two minutes... suddenly it's 3:00 AM. Pure digital hypnosis.",
                    "char_pose": "slouching",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "cozy_bedroom",
                    "shake": 2.0,
                    "props": [{"type": "phone_device", "scale": 1.2}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "psychology_dopamine",
                    "narration": "Every notification triggers a sharp dopamine spike. Your smartphone is literally a pocket casino.",
                    "char_pose": "thinking",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "living_room_couch",
                    "shake": 0.0,
                    "props": [{"type": "phone_device", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "reality_check",
                    "narration": "The average human taps their screen 2,617 times every single day. That's 11 whole years.",
                    "char_pose": "explaining",
                    "expression": "normal",
                    "shot_type": "standard",
                    "bg_style": "living_room_couch",
                    "shake": 0.0,
                    "props": [{"type": "clock", "scale": 1.1}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 4,
                    "beat": "what_if_disappears",
                    "narration": "What if your phone disappeared for 7 days? On Day 1, phantom vibrations drive you crazy.",
                    "char_pose": "panicking",
                    "expression": "screaming",
                    "shot_type": "standard",
                    "bg_style": "city_street",
                    "shake": 4.0,
                    "props": [{"type": "phone_device", "scale": 1.0}],
                    "sfx": "shatter"
                },
                {
                    "scene_id": 5,
                    "beat": "the_breakthrough",
                    "narration": "By Day 4, deep focus awakens. The real world stops feeling unbearable and boring.",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "city_street",
                    "shake": 0.0,
                    "props": [{"type": "sun", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 6,
                    "beat": "call_to_action",
                    "narration": "What was your screen time today? Check your phone right now and comment below!",
                    "char_pose": "pointing_up",
                    "expression": "smirk",
                    "shot_type": "standard",
                    "bg_style": "cozy_bedroom",
                    "shake": 0.0,
                    "props": [{"type": "phone_device", "scale": 1.1}],
                    "sfx": "title_boom"
                }
            ]
            viral_titles = [
                "What If Your Phone Disappeared for 7 Days? 📱",
                "The Smartphone Trap: How Screens Stole Our Life",
                "Why 2,617 Daily Screen Taps Stole 11 Years of Your Brain"
            ]
            thumb_hook = "7 DAYS NO PHONE?!"
            thumb_prop = "phone_device"

        return {
            "title": title,
            "topic": topic,
            "language": lang,
            "is_5min": is_5min,
            "aspect_ratio": aspect_ratio,
            "bg_style": "cozy_bedroom",
            "youtube_kit": {
                "viral_titles": viral_titles,
                "seo_description": f"Exploring the psychology and reality of {topic}! How screen time and notifications rewire our focus.\n\n#Smartphone #Dopamine #Shorts #Animation",
                "tags": [f"what if {topic}", "smartphone addiction", "screen time", "dopamine detox", "viral shorts", "stick figure animation"],
                "hashtags": ["#Shorts", "#Smartphone", "#Dopamine", "#ViralStory"],
                "pinned_comment": "Aaj aapka screen time kitne ghante tha? Check karke batayein! 👇" if lang == "hi" else "What was your screen time today? Check your settings and comment below! 👇",
                "thumbnail_hook": thumb_hook,
                "thumbnail_prop": thumb_prop
            },
            "scenes": scenes
        }

    # --- ARCHETYPE: RESTART HUMANITY (Awaken style: 5.3M views) ---
    def _build_restart_humanity(self, topic: str, lang: str, is_5min: bool, aspect_ratio: str) -> Dict[str, Any]:
        if lang == "hi":
            title = "Can 2 People Really Restart Humanity?"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "Aath arab log... raat-o-raat gayab ho gaye. Sirf aap bache hain... aur ek stranger.",
                    "char_pose": "panicking",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "ruins_wasteland",
                    "characters": ["HERO", "SECONDARY"],
                    "badge": "POPULATION: 2",
                    "shake": 2.0,
                    "props": [{"type": "earth", "scale": 1.2}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "the_core_question",
                    "narration": "Kya sirf 2 log poori manav jaati ko wapas zinda kar sakte hain? Biology kehti hai...",
                    "char_pose": "thinking",
                    "expression": "thinking",
                    "shot_type": "macro_prop",
                    "bg_style": "ruins_wasteland",
                    "characters": ["HERO"],
                    "badge": "GEN 1: SURVIVAL",
                    "props": [{"type": "dna_strand", "scale": 1.5}],
                    "shake": 0.0,
                    "sfx": "ding"
                },
                {
                    "scene_id": 3,
                    "beat": "generation_one",
                    "narration": "Pehli generation me sab theek rehta hai. Par generation two me... sab bhai-behan hain.",
                    "char_pose": "explaining",
                    "expression": "deadpan",
                    "shot_type": "standard",
                    "bg_style": "ruins_wasteland",
                    "characters": ["HERO", "SECONDARY"],
                    "badge": "GEN 2: MUTATION",
                    "shake": 0.0,
                    "props": [{"type": "dna_strand", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 4,
                    "beat": "genetic_bottleneck",
                    "narration": "Genetic bottleneck. Recessive bimariyaan 80 guna tezi se badh jaati hain... sab tabah.",
                    "char_pose": "hands_on_head",
                    "expression": "shocked",
                    "shot_type": "science_blueprint",
                    "bg_style": "lab",
                    "characters": ["DOC"],
                    "badge": "50/500 RULE",
                    "shake": 3.0,
                    "props": [],
                    "sfx": "shatter"
                },
                {
                    "scene_id": 5,
                    "beat": "minimum_population_rule",
                    "narration": "Scientists ka 50/500 rule: Humanity ko bachane ke liye kam se kam 500 log chahiye.",
                    "char_pose": "pointing_up",
                    "expression": "normal",
                    "shot_type": "standard",
                    "bg_style": "ruins_wasteland",
                    "characters": ["HERO", "SECONDARY"],
                    "badge": "GENETIC BOTTLENECK",
                    "shake": 0.0,
                    "props": [{"type": "dna_strand", "scale": 1.1}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 6,
                    "beat": "climax_question",
                    "narration": "Toh agar aakhri 2 log bache... kya aap koshish karenge? Niche comment karein!",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "ruins_wasteland",
                    "characters": ["HERO", "SECONDARY"],
                    "badge": "WHAT WOULD YOU DO?",
                    "shake": 0.0,
                    "props": [],
                    "sfx": "title_boom"
                }
            ]
            viral_titles = [
                "Can 2 People Really Restart Humanity? 🧬",
                "What If Only 2 People Survived on Earth?",
                "The Genetic Bottleneck: Why 2 People Cannot Save Us"
            ]
            thumb_hook = "ONLY 2 HUMANS?!"
            thumb_prop = "dna_strand"
        else:
            title = "Can 2 People Really Restart Humanity?"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "Eight billion people... gone overnight. Exactly two humans remain on Earth. You... and one stranger.",
                    "char_pose": "panicking",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "ruins_wasteland",
                    "characters": ["HERO", "SECONDARY"],
                    "badge": "POPULATION: 2",
                    "shake": 2.0,
                    "props": [{"type": "earth", "scale": 1.2}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "the_core_question",
                    "narration": "Can two people truly repopulate an entire planet? Biology has a brutal answer.",
                    "char_pose": "thinking",
                    "expression": "thinking",
                    "shot_type": "macro_prop",
                    "bg_style": "ruins_wasteland",
                    "characters": ["HERO"],
                    "badge": "GEN 1: SURVIVAL",
                    "shake": 0.0,
                    "props": [{"type": "dna_strand", "scale": 1.5}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 3,
                    "beat": "generation_one",
                    "narration": "Generation one thrives. But by generation two... every child is brother and sister.",
                    "char_pose": "explaining",
                    "expression": "deadpan",
                    "shot_type": "standard",
                    "bg_style": "ruins_wasteland",
                    "characters": ["HERO", "SECONDARY"],
                    "badge": "GEN 2: MUTATION",
                    "shake": 0.0,
                    "props": [{"type": "dna_strand", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 4,
                    "beat": "genetic_bottleneck",
                    "narration": "The genetic bottleneck. Deadly recessive mutations multiply by eighty percent within three generations.",
                    "char_pose": "hands_on_head",
                    "expression": "shocked",
                    "shot_type": "science_blueprint",
                    "bg_style": "lab",
                    "characters": ["DOC"],
                    "badge": "50/500 RULE",
                    "shake": 3.0,
                    "props": [],
                    "sfx": "shatter"
                },
                {
                    "scene_id": 5,
                    "beat": "minimum_population_rule",
                    "narration": "The famous 50/500 rule: You need at least five hundred humans to restart civilization.",
                    "char_pose": "pointing_up",
                    "expression": "normal",
                    "shot_type": "standard",
                    "bg_style": "ruins_wasteland",
                    "characters": ["HERO", "SECONDARY"],
                    "badge": "GENETIC BOTTLENECK",
                    "shake": 0.0,
                    "props": [{"type": "dna_strand", "scale": 1.1}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 6,
                    "beat": "climax_question",
                    "narration": "Would you try anyway? Tell us what you would do in the comments!",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "ruins_wasteland",
                    "characters": ["HERO", "SECONDARY"],
                    "badge": "WHAT WOULD YOU DO?",
                    "shake": 0.0,
                    "props": [],
                    "sfx": "title_boom"
                }
            ]
            viral_titles = [
                "Can 2 People Really Restart Humanity? 🧬",
                "What If Only 2 Humans Were Left on Earth?",
                "The Genetic Mystery of Repopulating Earth"
            ]
            thumb_hook = "ONLY 2 HUMANS?!"
            thumb_prop = "dna_strand"

        return {
            "title": title,
            "topic": topic,
            "language": lang,
            "is_5min": is_5min,
            "aspect_ratio": aspect_ratio,
            "bg_style": "ruins_wasteland",
            "primary_prop": "dna_strand",
            "science_metric": {
                "title": "GENETIC DIVERSITY THRESHOLD",
                "subtitle": "INBREEDING DEPRESSION RISK",
                "from": 2.0,
                "to": 99.4,
                "unit": "%",
                "label_start": "Gen 1 (2%)",
                "label_mid": "Gen 2 (48%)",
                "label_end": "Gen 4 (99.4%)"
            },
            "comparison_bars": [
                {"label": "MINIMUM (50/500)", "v": 0.88, "color": "#7ee787"},
                {"label": "SURVIVORS (2)", "v": 0.04, "color": "#ff5555"}
            ],
            "crisis_alert": {
                "label": "GENETIC BOTTLENECK",
                "value": "INBREEDING COLLAPSE"
            },
            "youtube_kit": {
                "viral_titles": viral_titles,
                "seo_description": "Can 2 people repopulate the entire Earth after a global apocalypse? We break down the real genetic bottleneck math and minimum viable population rules.\\n\\n#WhatIf #Science #Animation #Apocalypse #Shorts",
                "tags": ["can 2 people restart humanity", "minimum viable population", "genetic bottleneck", "stick figure animation", "what if animation", "viral shorts"],
                "hashtags": ["#Shorts", "#WhatIf", "#Science", "#Animation"],
                "pinned_comment": "Agar dharti par sirf 2 log bachein, toh kya aap repopulate karne ki koshish karenge? Honest answer batao! 👇",
                "thumbnail_hook": thumb_hook,
                "thumbnail_prop": thumb_prop
            },
            "scenes": scenes
        }

    # --- ARCHETYPE: ONLY MAN LEFT ON EARTH (IMAGINE style: 1.1M views) ---
    def _build_only_man_earth(self, topic: str, lang: str, is_5min: bool, aspect_ratio: str) -> Dict[str, Any]:
        if lang == "hi":
            title = "What If You Were the Only Man Left on Earth?"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "Subah aapki aankh khulti hai. Bahar ajeeb sannaata hai... 8 arab log gayab ho chuke hain.",
                    "char_pose": "panicking",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "cozy_bedroom",
                    "shake": 2.0,
                    "props": [{"type": "alarm_clock", "scale": 1.1}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "honeymoon_phase",
                    "narration": "Pehle kuch din sapne jaise lagte hain. Supermarkets free, supercars free, sab aapka hai.",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "city_street",
                    "shake": 0.0,
                    "props": [{"type": "money_bag", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "day_seven_blackout",
                    "narration": "Day 7: Power grid achanak collapse kar jata hai. Poora shehar ghup andhere me doob jata hai.",
                    "char_pose": "panicking",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "city_street",
                    "shake": 3.0,
                    "props": [],
                    "sfx": "power_down"
                },
                {
                    "scene_id": 4,
                    "beat": "nuclear_threat",
                    "narration": "Day 30: Duniya ke 440 nuclear plants bina cooling ke melt hona shuru hote hain.",
                    "char_pose": "hands_on_head",
                    "expression": "screaming",
                    "shot_type": "standard",
                    "bg_style": "ruins_wasteland",
                    "shake": 4.0,
                    "props": [{"type": "volcano", "scale": 1.1}],
                    "sfx": "shatter"
                },
                {
                    "scene_id": 5,
                    "beat": "solitude_toll",
                    "narration": "Mahine 6: Sannaata dimaag ko cheerne lagta hai. Insaan ko insaan ki zaroorat hoti hai.",
                    "char_pose": "slouching",
                    "expression": "sleepy",
                    "shot_type": "standard",
                    "bg_style": "ruins_wasteland",
                    "shake": 0.0,
                    "props": [],
                    "sfx": "ding"
                },
                {
                    "scene_id": 6,
                    "beat": "the_twist_cta",
                    "narration": "Aur fir... radio par achanak static me ek aawaaz aati hai: 'Hello?' Aap kya karenge?",
                    "char_pose": "pointing",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "cozy_bedroom",
                    "shake": 2.0,
                    "props": [{"type": "phone_device", "scale": 1.2}],
                    "sfx": "title_boom"
                }
            ]
            viral_titles = [
                "What If You Were the Only Person Left on Earth? 🌍",
                "The Only Man on Earth: Timeline of Solitude",
                "Could You Survive 30 Days Completely Alone?"
            ]
            thumb_hook = "ONLY MAN LEFT?!"
            thumb_prop = "earth"
        else:
            title = "What If You Were the Only Person Left on Earth?"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "You wake up to absolute silence. Every street, every phone... eight billion people just vanished.",
                    "char_pose": "panicking",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "cozy_bedroom",
                    "shake": 2.0,
                    "props": [{"type": "alarm_clock", "scale": 1.1}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "honeymoon_phase",
                    "narration": "Week one feels like paradise. Empty malls, free supercars, absolute freedom.",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "city_street",
                    "shake": 0.0,
                    "props": [{"type": "money_bag", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "day_seven_blackout",
                    "narration": "Day seven: The electrical grid fails. The entire world goes dead and silent.",
                    "char_pose": "panicking",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "city_street",
                    "shake": 3.0,
                    "props": [],
                    "sfx": "power_down"
                },
                {
                    "scene_id": 4,
                    "beat": "nuclear_threat",
                    "narration": "Day thirty: Over four hundred nuclear plants lose cooling water and start to fail.",
                    "char_pose": "hands_on_head",
                    "expression": "screaming",
                    "shot_type": "standard",
                    "bg_style": "ruins_wasteland",
                    "shake": 4.0,
                    "props": [{"type": "volcano", "scale": 1.1}],
                    "sfx": "shatter"
                },
                {
                    "scene_id": 5,
                    "beat": "solitude_toll",
                    "narration": "Month six: Silence becomes deafening. Isolation starts playing tricks on your mind.",
                    "char_pose": "slouching",
                    "expression": "sleepy",
                    "shot_type": "standard",
                    "bg_style": "ruins_wasteland",
                    "shake": 0.0,
                    "props": [],
                    "sfx": "ding"
                },
                {
                    "scene_id": 6,
                    "beat": "the_twist_cta",
                    "narration": "Then suddenly... your walkie-talkie clicks with static: 'Is anybody out there?' What now?",
                    "char_pose": "pointing",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "cozy_bedroom",
                    "shake": 2.0,
                    "props": [{"type": "phone_device", "scale": 1.2}],
                    "sfx": "title_boom"
                }
            ]
            viral_titles = [
                "What If You Were the Only Person Left on Earth? 🌍",
                "The Only Human on Earth: A Survival Timeline",
                "The Terrifying Reality of Absolute Solitude"
            ]
            thumb_hook = "ONLY MAN LEFT?!"
            thumb_prop = "earth"

        return {
            "title": title,
            "topic": topic,
            "language": lang,
            "is_5min": is_5min,
            "aspect_ratio": aspect_ratio,
            "bg_style": "city_street",
            "youtube_kit": {
                "viral_titles": viral_titles,
                "seo_description": "What if you woke up tomorrow and you were the only human left on planet Earth? We break down the exact timeline of survival, infrastructure collapse, and isolation.\n\n#WhatIf #Solitude #Animation #Survival #Shorts",
                "tags": ["only man left on earth", "alone on earth timeline", "what if animation", "stick figure animation", "survival timeline", "apocalypse animation"],
                "hashtags": ["#Shorts", "#WhatIf", "#Survival", "#Viral"],
                "pinned_comment": "Agar aap akele bachte, toh sabse pehle kahan jaate? Malls ya Supercars? Comment karo! 👇",
                "thumbnail_hook": thumb_hook,
                "thumbnail_prop": thumb_prop
            },
            "scenes": scenes
        }

    # --- ARCHETYPE 2: SURVIVAL TIMELINE (e.g. Locked in school with crush, Only man left) ---
    def _build_survival_scenario(self, topic: str, lang: str, is_5min: bool, aspect_ratio: str) -> Dict[str, Any]:
        if lang == "hi":
            title = "Locked Inside for 30 Days: The Survival Story"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "day_one_hook",
                    "narration": "Shaam 4:07 baje. School ke saare darwaze achanak lock ho jaate hain... Click.",
                    "char_pose": "panicking",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "school_classroom",
                    "shake": 4.0,
                    "props": [{"type": "vending_machine", "scale": 1.1}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "the_setup",
                    "narration": "Andar sirf 2 log bache hain. Ek aap... aur ek wo jisse aapne kabhi baat nahi ki.",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "shot_type": "standard",
                    "bg_style": "school_classroom",
                    "shake": 0.0,
                    "props": [],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "day_three_crisis",
                    "narration": "Day 3: Vending machine ke 84 snacks khatam ho chuke hain. Survival shuru hota hai.",
                    "char_pose": "shrugging",
                    "expression": "deadpan",
                    "shot_type": "standard",
                    "bg_style": "school_classroom",
                    "shake": 0.0,
                    "props": [{"type": "vending_machine", "scale": 1.0}],
                    "sfx": "shatter"
                },
                {
                    "scene_id": 4,
                    "beat": "day_ten_scale",
                    "narration": "Day 10: Khidki ke bahar 20 lakh log live dekh rahe hain. Par andar sannaata hai.",
                    "char_pose": "hands_on_head",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "school_classroom",
                    "shake": 3.0,
                    "props": [],
                    "sfx": "ding"
                },
                {
                    "scene_id": 5,
                    "beat": "day_twenty_breaking_point",
                    "narration": "Day 21: Bahar minus 15 degree thand hai... aur heating system band ho jata hai.",
                    "char_pose": "panicking",
                    "expression": "screaming",
                    "shot_type": "standard",
                    "bg_style": "frozen_ice",
                    "shake": 5.0,
                    "props": [{"type": "thermometer", "scale": 1.1}],
                    "sfx": "power_down"
                },
                {
                    "scene_id": 6,
                    "beat": "climax_choice",
                    "narration": "Ab yeh game nahi raha. Agar aap fass gaye, toh aap pehla kadam kya uthayenge?",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "school_classroom",
                    "shake": 0.0,
                    "props": [],
                    "sfx": "title_boom"
                }
            ]
            viral_titles = [
                "Locked in School for 30 Days: Could You Survive? 😱",
                "What If You Were Sealed Inside for 30 Days?!",
                "The 30-Day Survival Experiment Explained"
            ]
            thumb_hook = "LOCKED 30 DAYS?!"
            thumb_prop = "vending_machine"
        else:
            title = "What If You Were Locked Inside for 30 Days?"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "day_one_hook",
                    "narration": "Friday, 4:07 p.m. Every single door seals shut at the same time... Click.",
                    "char_pose": "panicking",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "school_classroom",
                    "shake": 4.0,
                    "props": [{"type": "vending_machine", "scale": 1.1}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "the_setup",
                    "narration": "Exactly two people are left inside. You... and someone who has never spoken to you.",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "shot_type": "standard",
                    "bg_style": "school_classroom",
                    "shake": 0.0,
                    "props": [],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "day_three_crisis",
                    "narration": "By day three, the vending machine is empty. Eighty-four snacks... completely gone.",
                    "char_pose": "shrugging",
                    "expression": "deadpan",
                    "shot_type": "standard",
                    "bg_style": "school_classroom",
                    "shake": 0.0,
                    "props": [{"type": "vending_machine", "scale": 1.0}],
                    "sfx": "shatter"
                },
                {
                    "scene_id": 4,
                    "beat": "day_ten_scale",
                    "narration": "By day ten, two million people are watching outside the window. Tension peaks.",
                    "char_pose": "hands_on_head",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "school_classroom",
                    "shake": 3.0,
                    "props": [],
                    "sfx": "ding"
                },
                {
                    "scene_id": 5,
                    "beat": "day_twenty_breaking_point",
                    "narration": "Day twenty-one: It is minus fifteen outside... and the heating system dies.",
                    "char_pose": "panicking",
                    "expression": "screaming",
                    "shot_type": "standard",
                    "bg_style": "frozen_ice",
                    "shake": 5.0,
                    "props": [{"type": "thermometer", "scale": 1.1}],
                    "sfx": "power_down"
                },
                {
                    "scene_id": 6,
                    "beat": "climax_choice",
                    "narration": "This is no longer a game. What is the first thing YOU would do? Tell us below!",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "school_classroom",
                    "shake": 0.0,
                    "props": [],
                    "sfx": "title_boom"
                }
            ]
            viral_titles = [
                "What If You Were Locked in School for 30 Days?! 👀",
                "30 Days Sealed Inside: The Survival Timeline",
                "Could You Survive Locked Inside for a Month?"
            ]
            thumb_hook = "30 DAYS SEALED?!"
            thumb_prop = "vending_machine"

        return {
            "title": title,
            "topic": topic,
            "language": lang,
            "is_5min": is_5min,
            "aspect_ratio": aspect_ratio,
            "bg_style": "school_classroom",
            "youtube_kit": {
                "viral_titles": viral_titles,
                "seo_description": "What happens when two people are sealed inside a building for 30 days? We break down the psychological timeline, resource math, and survival reality!\n\n#Survival #Story #WhatIf #Animation #ViralShorts",
                "tags": ["locked inside for 30 days", "survival timeline", "suddenly you style", "hypothetical scenario", "stick figure animation", "viral shorts"],
                "hashtags": ["#Shorts", "#Survival", "#WhatIf", "#Viral"],
                "pinned_comment": "Aap aise scenario me akele rehna pasand karenge ya crush ke saath? Comment karo! 👇",
                "thumbnail_hook": thumb_hook,
                "thumbnail_prop": thumb_prop
            },
            "scenes": scenes
        }

    # --- ARCHETYPE 3: DINOSAURS ---
    def _build_dinosaurs(self, topic: str, lang: str, is_5min: bool, aspect_ratio: str) -> Dict[str, Any]:
        if lang == "hi":
            title = "Kya Hoga Agar Dinosaurs Kabhi Khatam Hi Na Hote?"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "Agar 6.6 crore saal pehle wo asteroid na takrata... toh aaj aap T-Rex se bhaag rahe hote!",
                    "char_pose": "panicking",
                    "expression": "screaming",
                    "shot_type": "standard",
                    "bg_style": "jungle_forest",
                    "shake": 6.0,
                    "props": [{"type": "dinosaur", "scale": 1.2}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "human_evolution",
                    "narration": "Giant predators zinda rehte, toh insano ka evolution open plains par kabhi nahi ho pata.",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "shot_type": "standard",
                    "bg_style": "jungle_forest",
                    "shake": 0.0,
                    "props": [{"type": "dna_strand", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "troodon_intelligence",
                    "narration": "Troodon jaise chote dinosaurs ka dimaag tezz tha. Wo aaj insano se zyada smart ho sakte the!",
                    "char_pose": "thinking",
                    "expression": "thinking",
                    "shot_type": "standard",
                    "bg_style": "webcomic_light",
                    "shake": 0.0,
                    "props": [{"type": "question_mark", "scale": 1.1}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 4,
                    "beat": "modern_world",
                    "narration": "Hamare shehar concrete ke nahi, balki unchi metal fencing aur bunkers ke bane hote.",
                    "char_pose": "shrugging",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "neon_city",
                    "shake": 4.0,
                    "props": [{"type": "dinosaur", "scale": 1.1}],
                    "sfx": "shatter"
                },
                {
                    "scene_id": 5,
                    "beat": "modern_birds",
                    "narration": "Shocking fact: Dinosaurs aaj bhi zinda hain! Saare pakshi unhi ke direct descendants hain.",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "shot_type": "standard",
                    "bg_style": "webcomic_light",
                    "shake": 0.0,
                    "props": [{"type": "clock", "scale": 1.0}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 6,
                    "beat": "climax_cta",
                    "narration": "Toh shukr manaiye us asteroid ka! Subscribe karein aise hi mind-blowing What-Ifs ke liye.",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "jungle_forest",
                    "shake": 0.0,
                    "props": [],
                    "sfx": "title_boom"
                }
            ]
            viral_titles = [
                "Kya Hoga Agar Dinosaurs Zinda Hote? 😱",
                "Agar Asteroid Na Takrata Toh Kya Hota?!",
                "The Day Dinosaurs Ruled Modern Earth!"
            ]
            thumb_hook = "DINOSAURS ZINDA?!"
            thumb_prop = "dinosaur"
        else:
            title = "What If Dinosaurs Never Went Extinct?"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "If a six-mile asteroid hadn't hit Earth... you would be sprinting from T-Rexes today!",
                    "char_pose": "panicking",
                    "expression": "screaming",
                    "shot_type": "standard",
                    "bg_style": "jungle_forest",
                    "shake": 6.0,
                    "props": [{"type": "dinosaur", "scale": 1.2}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "human_evolution",
                    "narration": "If apex dinosaurs survived... mammals would never leave burrows. Humans might never evolve.",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "shot_type": "standard",
                    "bg_style": "jungle_forest",
                    "shake": 0.0,
                    "props": [{"type": "dna_strand", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "troodon_intelligence",
                    "narration": "Smart pack hunters like Troodon already had large brains. They might have built civilizations!",
                    "char_pose": "thinking",
                    "expression": "thinking",
                    "shot_type": "standard",
                    "bg_style": "webcomic_light",
                    "shake": 0.0,
                    "props": [{"type": "question_mark", "scale": 1.1}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 4,
                    "beat": "modern_world",
                    "narration": "Cities would require giant electric domes and armored bunkers to survive 70-ton herbivores.",
                    "char_pose": "shrugging",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "neon_city",
                    "shake": 4.0,
                    "props": [{"type": "dinosaur", "scale": 1.1}],
                    "sfx": "shatter"
                },
                {
                    "scene_id": 5,
                    "beat": "modern_birds",
                    "narration": "The craziest part? Dinosaurs never vanished. Every bird outside is a living theropod dinosaur!",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "shot_type": "standard",
                    "bg_style": "webcomic_light",
                    "shake": 0.0,
                    "props": [{"type": "clock", "scale": 1.0}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 6,
                    "beat": "climax_cta",
                    "narration": "So be grateful for that asteroid! Hit like, and subscribe for more deep dives.",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "jungle_forest",
                    "shake": 0.0,
                    "props": [],
                    "sfx": "title_boom"
                }
            ]
            viral_titles = [
                "What If Dinosaurs Never Went Extinct? 🦖",
                "If The Asteroid Missed: Humans vs Dinosaurs",
                "Could Modern Humans Survive With Dinosaurs?!"
            ]
            thumb_hook = "DINOSAURS ALIVE?!"
            thumb_prop = "dinosaur"

        return {
            "title": title,
            "topic": topic,
            "language": lang,
            "is_5min": is_5min,
            "aspect_ratio": aspect_ratio,
            "bg_style": "jungle_forest",
            "youtube_kit": {
                "viral_titles": viral_titles,
                "seo_description": "What if the Cretaceous asteroid missed Earth 66 million years ago? Would humans have ever evolved, or would intelligent dinosaurs build modern cities?\n\n#Dinosaurs #WhatIf #Evolution #ScienceFacts #Animation",
                "tags": ["what if dinosaurs never went extinct", "dinosaurs alive today", "prehistoric timeline", "stick figure animation", "jurassic park science", "viral animation"],
                "hashtags": ["#Shorts", "#Dinosaurs", "#WhatIf", "#Science"],
                "pinned_comment": "Agar aaj T-Rex zinda hota toh aapka pet hota ya aap uska lunch? Comment below! 👇",
                "thumbnail_hook": thumb_hook,
                "thumbnail_prop": thumb_prop
            },
            "scenes": scenes
        }

    # --- ARCHETYPE 4: TECH & AI ---
    def _build_tech_ai(self, topic: str, lang: str, is_5min: bool, aspect_ratio: str) -> Dict[str, Any]:
        if lang == "hi":
            title = "Kya Hoga Agar AI Ne Saari Jobs Le Li?"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "Kal subah aap office pahunche... aur pata chala har employee ko AI ne replace kar diya!",
                    "char_pose": "panicking",
                    "expression": "screaming",
                    "shot_type": "standard",
                    "bg_style": "neon_city",
                    "shake": 5.0,
                    "props": [{"type": "robot_ai", "scale": 1.2}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "immediate_shock",
                    "narration": "Pehle 30 din me coding, finance aur teaching jaise jobs 100 percent automate ho jaate hain.",
                    "char_pose": "pointing",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "neon_city",
                    "shake": 0.0,
                    "props": [{"type": "phone_device", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "economic_crash",
                    "narration": "Agar kisi ke paas salary nahi hogi... toh koi samaan kaise khareedega? Economy freeze!",
                    "char_pose": "thinking",
                    "expression": "thinking",
                    "shot_type": "standard",
                    "bg_style": "webcomic_light",
                    "shake": 3.0,
                    "props": [{"type": "money_bag", "scale": 1.1}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 4,
                    "beat": "the_solution",
                    "narration": "Governments ko Universal Basic Income shuru karna padega. Sabko free me paise milenge!",
                    "char_pose": "shrugging",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "webcomic_light",
                    "shake": 0.0,
                    "props": [{"type": "money_bag", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 5,
                    "beat": "human_purpose",
                    "narration": "Insan kaam se aazad ho jayenge. Art, science aur exploration hamara naya routine banega.",
                    "char_pose": "pointing_up",
                    "expression": "normal",
                    "shot_type": "standard",
                    "bg_style": "neon_city",
                    "shake": 0.0,
                    "props": [{"type": "sun", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 6,
                    "beat": "climax_cta",
                    "narration": "Kya aap aisi duniya me rehna chahenge? Apni rai comment karein aur subscribe karein!",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "neon_city",
                    "shake": 0.0,
                    "props": [],
                    "sfx": "title_boom"
                }
            ]
            viral_titles = [
                "Kya Hoga Agar AI Ne Saari Jobs Le Li? 🤖",
                "The Day AI Replaced Every Human Worker!",
                "Will AI Make Money Useless in 10 Years?!"
            ]
            thumb_hook = "ALL JOBS GONE?!"
            thumb_prop = "robot_ai"
        else:
            title = "What If AI Took Over All Human Jobs?"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "Tomorrow morning, you log into work... and realize an AI has taken your exact job.",
                    "char_pose": "panicking",
                    "expression": "screaming",
                    "shot_type": "standard",
                    "bg_style": "neon_city",
                    "shake": 5.0,
                    "props": [{"type": "robot_ai", "scale": 1.2}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "immediate_shock",
                    "narration": "Within 30 days, finance, legal, and software engineering are completely automated by silicon.",
                    "char_pose": "pointing",
                    "expression": "shocked",
                    "shot_type": "standard",
                    "bg_style": "neon_city",
                    "shake": 0.0,
                    "props": [{"type": "phone_device", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "economic_crash",
                    "narration": "The paradox? If nobody has a paycheck... who buys what the robots produce?",
                    "char_pose": "thinking",
                    "expression": "thinking",
                    "shot_type": "standard",
                    "bg_style": "webcomic_light",
                    "shake": 3.0,
                    "props": [{"type": "money_bag", "scale": 1.1}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 4,
                    "beat": "the_solution",
                    "narration": "Nations are forced to implement Universal Basic Income. Money is wired directly to citizens.",
                    "char_pose": "shrugging",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "webcomic_light",
                    "shake": 0.0,
                    "props": [{"type": "money_bag", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 5,
                    "beat": "human_purpose",
                    "narration": "Humanity enters post-scarcity: art, space exploration, and passion projects replace the 9-to-5 grind.",
                    "char_pose": "pointing_up",
                    "expression": "normal",
                    "shot_type": "standard",
                    "bg_style": "neon_city",
                    "shake": 0.0,
                    "props": [{"type": "sun", "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 6,
                    "beat": "climax_cta",
                    "narration": "Is an AI utopia heaven... or a trap? Comment your thoughts and subscribe for more!",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "shot_type": "standard",
                    "bg_style": "neon_city",
                    "shake": 0.0,
                    "props": [],
                    "sfx": "title_boom"
                }
            ]
            viral_titles = [
                "What If AI Replaced Every Human Job? 🤖",
                "The 10-Year Timeline: Life Without 9-to-5 Work",
                "Could Humanity Survive When Robots Do Everything?!"
            ]
            thumb_hook = "AI TAKES ALL?!"
            thumb_prop = "robot_ai"

        return {
            "title": title,
            "topic": topic,
            "language": lang,
            "is_5min": is_5min,
            "aspect_ratio": aspect_ratio,
            "bg_style": "neon_city",
            "youtube_kit": {
                "viral_titles": viral_titles,
                "seo_description": "What happens when artificial intelligence automates 100% of human labor? We examine economics, universal basic income, and the post-work future!\n\n#AI #FutureTech #Economy #WhatIf #Animation",
                "tags": ["what if ai took over all jobs", "future of work automation", "universal basic income", "artificial intelligence explainer", "viral animation"],
                "hashtags": ["#Shorts", "#AI", "#Future", "#Viral"],
                "pinned_comment": "Agar AI aapka kaam kare, toh aap free time me kya karenge? Tell us below! 👇",
                "thumbnail_hook": thumb_hook,
                "thumbnail_prop": thumb_prop
            },
            "scenes": scenes
        }

    # --- ARCHETYPE 5: UNIVERSAL DYNAMIC WHAT-IF (Autonomous multi-domain semantic engine) ---
    def _build_universal_what_if(self, topic: str, lang: str, is_5min: bool, aspect_ratio: str) -> Dict[str, Any]:
        clean_subj = re.sub(r'^(what\s+if|kya\s+hoga\s+agar|the\s+truth\s+about|how\s+to)\s+', '', topic, flags=re.IGNORECASE).rstrip("? ")
        if not clean_subj:
            clean_subj = "this hidden truth"

        t_low = topic.lower()

        # Semantic environment and prop selection based on domain
        if any(w in t_low for w in ["money", "cash", "crypto", "rich", "paisa", "invest", "wealth", "business", "market", "economy"]):
            bg_1, bg_2, bg_3 = "bank_vault", "city_street", "office_workspace"
            p_1, p_2, p_3 = "money_bag", "phone_device", "target_bullseye"
        elif any(w in t_low for w in ["ai", "tech", "robot", "code", "cyber", "software", "computer", "future"]):
            bg_1, bg_2, bg_3 = "tech_server_room", "neon_city", "office_workspace"
            p_1, p_2, p_3 = "laptop", "brain_glow", "lightbulb_idea"
        elif any(w in t_low for w in ["sport", "run", "fit", "gym", "body", "muscle", "health", "exercise", "athlet"]):
            bg_1, bg_2, bg_3 = "running_track", "gym_fitness", "sports_stadium"
            p_1, p_2, p_3 = "running_shoes", "dumbbell", "trophy_cup"
        elif any(w in t_low for w in ["space", "sun", "moon", "earth", "planet", "cosm", "alien", "star"]):
            bg_1, bg_2, bg_3 = "dusk_space", "mountain_peak", "dusk_space"
            p_1, p_2, p_3 = "earth", "sun", "question_mark"
        elif any(w in t_low for w in ["learn", "study", "exam", "book", "focus", "read", "memory", "mind"]):
            bg_1, bg_2, bg_3 = "library_books", "school_classroom", "office_workspace"
            p_1, p_2, p_3 = "book", "brain_glow", "lightbulb_idea"
        else:
            bg_1, bg_2, bg_3 = "office_workspace", "outdoor_park", "city_street"
            p_1, p_2, p_3 = "target_bullseye", "lightbulb_idea", "trophy_cup"

        if lang == "hi":
            title = f"{clean_subj.title()} Ka Shocking Sach!"
            if is_5min:
                scenes = [
                    {
                        "scene_id": 1,
                        "beat": "cold_hook",
                        "narration": f"Agar aap {clean_subj} ko ignore kar rahe hain... toh sabse badi galti kar rahe hain.",
                        "char_pose": "pointing",
                        "expression": "shocked",
                        "shot_type": "standard",
                        "bg_style": bg_1,
                        "props": [{"type": p_1, "scale": 1.2}],
                        "sfx": "drone_hit"
                    },
                    {
                        "scene_id": 2,
                        "beat": "the_paradox",
                        "narration": "Duniya sochti hai ki yeh aasan hai... lekin statistics kuch aur hi kadwa sach batate hain.",
                        "char_pose": "thinking",
                        "expression": "thinking",
                        "shot_type": "standard",
                        "bg_style": bg_2,
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 3,
                        "beat": "studio_analytics",
                        "narration": "Data dekhiye: 94% log shuru karte hain, lekin sirf 6% log actual breakthrough tak pahunchte hain.",
                        "char_pose": "pointing",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "sfx": "ding",
                        "bar_chart": {
                            "title": "GLOBAL RETENTION METRIC",
                            "bars": [
                                {"label": "Day 1 Starters", "value": 94, "color": "#06b6d4"},
                                {"label": "Week 2 Drop", "value": 38, "color": "#f59e0b"},
                                {"label": "Top Masters", "value": 6, "color": "#10b981"}
                            ]
                        },
                        "stage_badge": {"num": 1, "title": "THE BIG PARADOX"}
                    },
                    {
                        "scene_id": 4,
                        "beat": "the_first_action",
                        "narration": "Shuru me sab theek lagta hai. Dopamine high hota hai aur motivation aag jaisa chamakta hai.",
                        "char_pose": "running",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": bg_2,
                        "sfx": "whoosh"
                    },
                    {
                        "scene_id": 5,
                        "beat": "studio_disruption",
                        "narration": "Yahin sabse bada trap hai: Log temporary motivation ko permanent system samajh lete hain.",
                        "char_pose": "explaining",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "sfx": "shatter",
                        "comparison_split": {
                            "left": {"title": "99% AMATEUR TRAP", "points": ["Wait for inspiration", "Emotional inconsistency", "Quit at first resistance"]},
                            "right": {"title": "1% MASTER PROTOCOL", "points": ["Non-negotiable daily habits", "Systems over feelings", "Compounding focus"]}
                        },
                        "stage_badge": {"num": 2, "title": "DISRUPTING ASSUMPTIONS"}
                    },
                    {
                        "scene_id": 6,
                        "beat": "the_friction_wall",
                        "narration": "Jaise hi excitement khatam hoti hai... dimaag par thakan aur laziness ka pahaad toot padta hai.",
                        "char_pose": "slouching",
                        "expression": "exhausted",
                        "shot_type": "standard",
                        "bg_style": bg_2,
                        "dark_bags": True,
                        "props": [{"type": p_2, "scale": 1.1}],
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 7,
                        "beat": "the_breaking_point",
                        "narration": "Yeh wahi critical checkpoint hai... jahan aakar 90 percent log chup-chaap haar maan lete hain.",
                        "char_pose": "exhausted",
                        "expression": "shocked",
                        "shot_type": "standard",
                        "bg_style": "hospital_lab",
                        "sfx": "shatter"
                    },
                    {
                        "scene_id": 8,
                        "beat": "studio_resistance_gauge",
                        "narration": "Science isse 'The Dip' kehti hai—jahan aapka dimag purani aaraam-parast aadat me lautne ki zidd karta hai.",
                        "char_pose": "thinking",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_dark",
                        "sfx": "ding",
                        "circular_gauge": {"value": 91, "label": "RESISTANCE PEAK", "unit": "%"},
                        "stage_badge": {"num": 3, "title": "UNVEILING THE MECHANISM"}
                    },
                    {
                        "scene_id": 9,
                        "beat": "the_turning_point",
                        "narration": "Lekin jo log rukte nahi... unka dimaag naye neural pathways construct karna shuru karta hai.",
                        "char_pose": "standing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": bg_1,
                        "sfx": "ding"
                    },
                    {
                        "scene_id": 10,
                        "beat": "the_deep_focus",
                        "narration": "Achanak, jo cheez kal tak pahaad lag rahi thi... wo aapki second nature ban jaati hai.",
                        "char_pose": "typing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "office_workspace",
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 11,
                        "beat": "studio_truth_revelation",
                        "narration": "Kamyabi koi lottery nahi hai—yeh sirf unshakeable execution aur compounding ka mathematics hai.",
                        "char_pose": "pointing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "sfx": "ding",
                        "glass_card": {
                            "title": "THE MATHEMATICAL TRUTH",
                            "subtitle": "Small daily disciplines repeated consistently create massive exponential advantage."
                        },
                        "stage_badge": {"num": 4, "title": "ULTIMATE TRUTH REVELATION"}
                    },
                    {
                        "scene_id": 12,
                        "beat": "the_compounding_surge",
                        "narration": "Ek baar jab momentum lock ho gaya... toh results 10 guna tezi se multiply hote hain.",
                        "char_pose": "lifting",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": bg_3,
                        "props": [{"type": p_3, "scale": 1.2}],
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 13,
                        "beat": "the_breakthrough_moment",
                        "narration": "Jo kal tak impossible lag raha tha... aaj aapka normal standard ban chuka hai.",
                        "char_pose": "celebrating",
                        "expression": "happy",
                        "shot_type": "standard",
                        "bg_style": bg_3,
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 14,
                        "beat": "the_mastery_level",
                        "narration": "Aap aam bheed se nikal kar... top 1 percent tier ke andar establish ho chuke hain.",
                        "char_pose": "standing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "aura": 0.5
                    },
                    {
                        "scene_id": 15,
                        "beat": "the_core_philosophy",
                        "narration": f"Mastery ka ek hi rule hai: Kabhi mood ka intezaar mat karo. Action pehle lo, mood khud follow karega.",
                        "char_pose": "cheer",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "sfx": "ding"
                    },
                    {
                        "scene_id": 16,
                        "beat": "the_challenge_cta",
                        "narration": f"Aapka {clean_subj} par kya nazariya hai? Niche comment me zaroor batayein!",
                        "char_pose": "pointing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_dark",
                        "sfx": "title_boom",
                        "stage_badge": {"num": 5, "title": "COMMUNITY DEBATE"}
                    }
                ]
            else:
                scenes = [
                    {
                        "scene_id": 1,
                        "beat": "cold_hook",
                        "narration": f"Agar aap {clean_subj} ko ignore kar rahe hain... toh sabse badi galti kar rahe hain.",
                        "char_pose": "pointing",
                        "expression": "shocked",
                        "shot_type": "standard",
                        "bg_style": bg_1,
                        "shake": 0.0,
                        "props": [{"type": p_1, "scale": 1.2}],
                        "sfx": "drone_hit"
                    },
                    {
                        "scene_id": 2,
                        "beat": "the_first_action",
                        "narration": f"Jaise hi aap {clean_subj} ko deeply samajhte hain... dimaag turant alert ho jaata hai.",
                        "char_pose": "thinking",
                        "expression": "thinking",
                        "shot_type": "standard",
                        "bg_style": bg_2,
                        "shake": 0.0,
                        "props": [{"type": "clock", "scale": 1.1}],
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 3,
                        "beat": "the_hidden_science",
                        "narration": "Iske peeche ek scientific reality hai... jo 99 percent log bilkul nahi jaante.",
                        "char_pose": "pointing_up",
                        "expression": "happy",
                        "shot_type": "standard",
                        "bg_style": "hospital_lab",
                        "shake": 0.0,
                        "props": [{"type": "brain_glow", "scale": 1.2}],
                        "sfx": "ding"
                    },
                    {
                        "scene_id": 4,
                        "beat": "the_friction_wall",
                        "narration": "Yeh aasan nahi hai. Most people yahin par aakar haar maan lete hain.",
                        "char_pose": "exhausted",
                        "expression": "shocked",
                        "shot_type": "standard",
                        "bg_style": bg_2,
                        "shake": 1.5,
                        "props": [{"type": p_2, "scale": 1.1}],
                        "sfx": "shatter"
                    },
                    {
                        "scene_id": 5,
                        "beat": "the_breakthrough",
                        "narration": "Lekin jo log consistent rehte hain... unka result seedha 10 guna multiply hota hai.",
                        "char_pose": "celebrating",
                        "expression": "happy",
                        "shot_type": "standard",
                        "bg_style": bg_3,
                        "shake": 0.0,
                        "props": [{"type": p_3, "scale": 1.2}],
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 6,
                        "beat": "the_challenge_cta",
                        "narration": f"Aapka {clean_subj} par kya nazariya hai? Niche comment karein aur batayein!",
                        "char_pose": "hands_on_hips",
                        "expression": "happy",
                        "shot_type": "standard",
                        "bg_style": bg_3,
                        "shake": 0.0,
                        "props": [{"type": "gold_medal", "scale": 1.1}],
                        "sfx": "title_boom"
                    }
                ]
            viral_titles = [
                f"{clean_subj.title()} Ka Shocking Sach! 😱",
                f"Why 99% of People Get {clean_subj.title()} Completely Wrong",
                f"The 10x Secret of {clean_subj.title()} Explained"
            ]
            thumb_hook = "KISI KO NAHI PATA?!"
            thumb_prop = p_1
        else:
            title = f"The Shocking Truth About {clean_subj.title()}"
            if is_5min:
                scenes = [
                    {
                        "scene_id": 1,
                        "beat": "cold_hook",
                        "narration": f"If you overlook {clean_subj}... you are leaving massive potential completely on the table.",
                        "char_pose": "pointing",
                        "expression": "shocked",
                        "shot_type": "standard",
                        "bg_style": bg_1,
                        "props": [{"type": p_1, "scale": 1.2}],
                        "sfx": "drone_hit"
                    },
                    {
                        "scene_id": 2,
                        "beat": "the_paradox",
                        "narration": "Everyone assumes it comes down to raw luck... but the underlying data proves otherwise.",
                        "char_pose": "thinking",
                        "expression": "thinking",
                        "shot_type": "standard",
                        "bg_style": bg_2,
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 3,
                        "beat": "studio_analytics",
                        "narration": "Notice the metrics: 94% of people initiate with high hopes, but only 6% break through.",
                        "char_pose": "pointing",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "sfx": "ding",
                        "bar_chart": {
                            "title": "GLOBAL BREAKTHROUGH METRICS",
                            "bars": [
                                {"label": "Day 1 Starters", "value": 94, "color": "#06b6d4"},
                                {"label": "Week 2 Dropoff", "value": 38, "color": "#f59e0b"},
                                {"label": "Top 1% Masters", "value": 6, "color": "#10b981"}
                            ]
                        },
                        "stage_badge": {"num": 1, "title": "THE STATISTICAL GAP"}
                    },
                    {
                        "scene_id": 4,
                        "beat": "the_first_action",
                        "narration": "In the beginning, novelty feels intoxicating. Dopamine carries you effortlessly forward.",
                        "char_pose": "running",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": bg_2,
                        "sfx": "whoosh"
                    },
                    {
                        "scene_id": 5,
                        "beat": "studio_disruption",
                        "narration": "This is the fatal trap: Mistaking the emotional high of starting with actual mastery.",
                        "char_pose": "explaining",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "sfx": "shatter",
                        "comparison_split": {
                            "left": {"title": "99% AMATEUR TRAP", "points": ["Wait for inspiration", "Feelings dictate actions", "Surrender at friction"]},
                            "right": {"title": "1% MASTER PROTOCOL", "points": ["Scheduled execution", "Actions dictate feelings", "Unrelenting daily system"]}
                        },
                        "stage_badge": {"num": 2, "title": "SHATTERING ILLUSIONS"}
                    },
                    {
                        "scene_id": 6,
                        "beat": "the_friction_wall",
                        "narration": "The moment excitement fades... internal resistance surges like a brick wall in your mind.",
                        "char_pose": "slouching",
                        "expression": "exhausted",
                        "shot_type": "standard",
                        "bg_style": bg_2,
                        "dark_bags": True,
                        "props": [{"type": p_2, "scale": 1.1}],
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 7,
                        "beat": "the_breaking_point",
                        "narration": "This exact friction is where the majority quietly surrender and return to comfort.",
                        "char_pose": "exhausted",
                        "expression": "shocked",
                        "shot_type": "standard",
                        "bg_style": "hospital_lab",
                        "sfx": "shatter"
                    },
                    {
                        "scene_id": 8,
                        "beat": "studio_resistance_gauge",
                        "narration": "Cognitive science labels this Resistance—the homeostatic pull back into familiar mediocrity.",
                        "char_pose": "thinking",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_dark",
                        "sfx": "ding",
                        "circular_gauge": {"value": 91, "label": "RESISTANCE PEAK", "unit": "%"},
                        "stage_badge": {"num": 3, "title": "UNVEILING THE FRICTION"}
                    },
                    {
                        "scene_id": 9,
                        "beat": "the_turning_point",
                        "narration": "Refuse to surrender, and your brain begins laying down permanent neural myelin pathways.",
                        "char_pose": "standing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": bg_1,
                        "sfx": "ding"
                    },
                    {
                        "scene_id": 10,
                        "beat": "the_deep_focus",
                        "narration": "Suddenly, what once felt grueling becomes an automatic, effortless baseline rhythm.",
                        "char_pose": "typing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "office_workspace",
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 11,
                        "beat": "studio_truth_revelation",
                        "narration": "Success isn't accidental luck. It is pure mechanical compounding of structured daily habits.",
                        "char_pose": "pointing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "sfx": "ding",
                        "glass_card": {
                            "title": "THE MATHEMATICAL TRUTH",
                            "subtitle": "Small daily disciplines repeated consistently create massive exponential advantage."
                        },
                        "stage_badge": {"num": 4, "title": "THE ULTIMATE TRUTH"}
                    },
                    {
                        "scene_id": 12,
                        "beat": "the_compounding_surge",
                        "narration": "Once compounding takes over... your returns multiply at a staggering ten-times pace.",
                        "char_pose": "lifting",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": bg_3,
                        "props": [{"type": p_3, "scale": 1.2}],
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 13,
                        "beat": "the_breakthrough_moment",
                        "narration": "What once seemed impossible has now become your non-negotiable daily standard.",
                        "char_pose": "celebrating",
                        "expression": "happy",
                        "shot_type": "standard",
                        "bg_style": bg_3,
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 14,
                        "beat": "the_mastery_level",
                        "narration": "You have crossed the threshold from ordinary spectator into the top one percent.",
                        "char_pose": "standing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "aura": 0.5
                    },
                    {
                        "scene_id": 15,
                        "beat": "the_core_philosophy",
                        "narration": f"The golden rule of mastery: Never negotiate with feelings. Action comes first; feelings follow.",
                        "char_pose": "cheer",
                        "expression": "motivated",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_light",
                        "sfx": "ding"
                    },
                    {
                        "scene_id": 16,
                        "beat": "the_challenge_cta",
                        "narration": f"Will you apply this protocol today... or let another year slip by? Drop your thoughts below!",
                        "char_pose": "pointing",
                        "expression": "disciplined",
                        "shot_type": "standard",
                        "bg_style": "studio_tech_dark",
                        "sfx": "title_boom",
                        "stage_badge": {"num": 5, "title": "COMMUNITY DEBATE"}
                    }
                ]
            else:
                scenes = [
                    {
                        "scene_id": 1,
                        "beat": "cold_hook",
                        "narration": f"If you overlook {clean_subj}... you are leaving massive potential completely on the table.",
                        "char_pose": "pointing",
                        "expression": "shocked",
                        "shot_type": "standard",
                        "bg_style": bg_1,
                        "shake": 0.0,
                        "props": [{"type": p_1, "scale": 1.2}],
                        "sfx": "drone_hit"
                    },
                    {
                        "scene_id": 2,
                        "beat": "the_first_action",
                        "narration": f"The moment you confront {clean_subj}... everything you thought you knew changes instantly.",
                        "char_pose": "thinking",
                        "expression": "thinking",
                        "shot_type": "standard",
                        "bg_style": bg_2,
                        "shake": 0.0,
                        "props": [{"type": "clock", "scale": 1.1}],
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 3,
                        "beat": "the_hidden_science",
                        "narration": "There is a deep psychological principle here... that 99 percent of people miss.",
                        "char_pose": "pointing_up",
                        "expression": "happy",
                        "shot_type": "standard",
                        "bg_style": "hospital_lab",
                        "shake": 0.0,
                        "props": [{"type": "brain_glow", "scale": 1.2}],
                        "sfx": "ding"
                    },
                    {
                        "scene_id": 4,
                        "beat": "the_friction_wall",
                        "narration": "It isn't effortless. This exact obstacle is where ordinary people quit.",
                        "char_pose": "exhausted",
                        "expression": "shocked",
                        "shot_type": "standard",
                        "bg_style": bg_2,
                        "shake": 1.5,
                        "props": [{"type": p_2, "scale": 1.1}],
                        "sfx": "shatter"
                    },
                    {
                        "scene_id": 5,
                        "beat": "the_breakthrough",
                        "narration": "Push through that barrier, and your compounding advantage explodes ten times over.",
                        "char_pose": "celebrating",
                        "expression": "happy",
                        "shot_type": "standard",
                        "bg_style": bg_3,
                        "shake": 0.0,
                        "props": [{"type": p_3, "scale": 1.2}],
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 6,
                        "beat": "the_challenge_cta",
                        "narration": f"Will you master {clean_subj} today... or stay behind? Drop your thoughts below!",
                        "char_pose": "hands_on_hips",
                        "expression": "happy",
                        "shot_type": "standard",
                        "bg_style": bg_3,
                        "shake": 0.0,
                        "props": [{"type": "gold_medal", "scale": 1.1}],
                        "sfx": "title_boom"
                    }
                ]
            viral_titles = [
                f"The Shocking Truth About {clean_subj.title()}! 😱",
                f"Why 99% of People Fail at {clean_subj.title()}",
                f"The 10x Advantage: How {clean_subj.title()} Changes Everything"
            ]
            thumb_hook = "SHOCKING TRUTH?!"
            thumb_prop = p_1

        pinned = (
            f"What is your biggest takeaway about {clean_subj}? Let us know in the comments below! 👇"
            if lang == "en"
            else f"Aapke mutabiq {clean_subj} par aapki kya raye hai? Comment karein! 👇"
        )
        return {
            "title": title,
            "topic": topic,
            "language": lang,
            "is_5min": is_5min,
            "aspect_ratio": aspect_ratio,
            "bg_style": "dusk_space",
            "youtube_kit": {
                "viral_titles": viral_titles,
                "seo_description": f"Exploring the fascinating reality of {clean_subj}! What happens to human psychology, everyday life, and society?\n\n#Animation #ViralShorts #Story #Education",
                "tags": [f"{clean_subj}", f"truth about {clean_subj}", "stick figure animation", "viral shorts", "educational animation"],
                "hashtags": ["#Shorts", "#Viral", "#Story", "#Animation"],
                "pinned_comment": pinned,
                "thumbnail_hook": thumb_hook,
                "thumbnail_prop": thumb_prop
            },
            "scenes": scenes
        }
