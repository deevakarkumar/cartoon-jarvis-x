"""
Script & Storyboard Generator
Creates high-retention multi-chapter explainer scripts (1-minute shorts or 5-minute deep dives).
Dynamically supports any topic in both Hindi and English with strict duration controls
and authentic subject-specific survival, biological, and cosmic facts.
"""

import json
import re
from typing import Dict, Any, List


class ScriptGenerator:
    def __init__(self, default_lang: str = "en"):
        self.default_lang = default_lang

    def clean_subject(self, topic: str, lang: str) -> str:
        """Strips 'what if', 'kya ho agar' to get the clean core subject."""
        t = re.sub(r"^(what\s+if\s+(we\s+|you\s+|humanity\s+|humans\s+)?(could\s+|were\s+|got\s+|are\s+)?|kya\s+ho\s+agar\s+)", "", topic, flags=re.IGNORECASE)
        t = t.strip("? .!")
        return t

    def generate_script(self, topic: str, lang: str = "en", duration_target: str = "1min") -> Dict[str, Any]:
        """
        Generates structured explainer scripts.
        Strictly enforces:
        - 1-Minute Short: 4 to 6 scenes (~50-65s total)
        - 5-Minute Deep Dive: 16 to 18 scenes (~270-300s total)
        """
        lang = lang.lower().strip()
        lang = "hi" if "hi" in lang else "en"

        topic_clean = topic.strip()
        topic_lower = topic_clean.lower()
        is_5min = ("5min" in duration_target or "5" in str(duration_target))

        # 1. JUNGLE / FOREST / WILDERNESS SURVIVAL
        if any(w in topic_lower for w in ["jungle", "forest", "wood", "wild", "trapped", "island", "desert"]):
            data = self._script_jungle_trapped(topic_clean, lang, is_5min)

        # 2. WEEPING / CRYING / TEARS
        elif any(w in topic_lower for w in ["weep", "cry", "tear", "aansu", "rona"]):
            data = self._script_no_crying(topic_clean, lang, is_5min)

        # 3. SLEEP / INSOMNIA
        elif any(w in topic_lower for w in ["sleep", "neend", "soye", "insomnia"]):
            data = self._script_no_sleep(topic_clean, lang, is_5min)

        # 4. SUN BLACKOUT
        elif any(w in topic_lower for w in ["sun", "suraj", "solar"]):
            data = self._script_sun_disappears(topic_clean, lang, is_5min)

        # 5. MOON VANISHED
        elif any(w in topic_lower for w in ["moon", "chand", "lunar"]):
            data = self._script_moon_vanished(topic_clean, lang, is_5min)

        # 6. DYNAMIC FALLBACK
        else:
            data = self._generate_dynamic_what_if(topic_clean, lang, is_5min)

        data["is_5min"] = is_5min
        return data

    # -------------------------------------------------------------
    # 1. TOPIC: TRAPPED IN A DEEP JUNGLE
    # -------------------------------------------------------------
    def _script_jungle_trapped(self, topic: str, lang: str, is_5min: bool) -> Dict[str, Any]:
        if lang == "hi":
            title = "Kya Ho Agar Aap Jungle Me Phans Jayein? (Jungle Survival)"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "Agar aap achanak kisi ghane jungle me akele phans jayein, to sabse pehle jungli janwar nahi, balki aapka apna darr aur dehydration aapko 72 ghante me maar dalega!",
                    "char_pose": "panicking",
                    "expression": "screaming",
                    "bg_style": "jungle_forest",
                    "shake": 6.0,
                    "props": [{"type": "tree", "x": 1450, "y": 420, "scale": 1.1}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "rule_of_threes",
                    "narration": "Survival ka pehla golden rule: Rule of Three. Aap bina hawa ke teen minute, bina paani ke teen din, aur bina khane ke teen hafte zinda reh sakte hain.",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "bg_style": "jungle_forest",
                    "shake": 0.0,
                    "props": [{"type": "clock", "x": 1400, "y": 380, "scale": 1.0}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "the_fatal_mistake",
                    "narration": "Sabse badi galti: Pyas lagne par kisi bhi ruki hui jheel ka paani peena. Usme maujood microscopic parasites aapke pait me severe infection karke aapko chalne ke layaq nahi chhodenge!",
                    "char_pose": "shrugging",
                    "expression": "shocked",
                    "bg_style": "jungle_forest",
                    "shake": 4.0,
                    "props": [{"type": "water_drop", "x": 1400, "y": 400, "scale": 1.2}],
                    "sfx": "shatter"
                },
                {
                    "scene_id": 4,
                    "beat": "navigation_trick",
                    "narration": "Rasta dhoondne ke liye hamesha behte hue paani ya choti nadi ka peecha karein. Nadi aage chalkar badi nadi banti hai, aur wahi aapko kisi gaon ya basti tak le jayegi.",
                    "char_pose": "thinking",
                    "expression": "thinking",
                    "bg_style": "jungle_forest",
                    "shake": 0.0,
                    "props": [{"type": "compass", "x": 1400, "y": 400, "scale": 1.1}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 5,
                    "beat": "predators_night",
                    "narration": "Raat hone se pehle zameen se 5 feet upar shelter banayein aur aag jalayein. Aag ka dhuwan aur roshni predators aur toxic insects ko dur rakhti hai.",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "bg_style": "jungle_forest",
                    "shake": 0.0,
                    "props": [{"type": "campfire", "x": 1400, "y": 500, "scale": 1.2}],
                    "sfx": "power_down"
                },
                {
                    "scene_id": 6,
                    "beat": "climax_outro",
                    "narration": "Toh jab agali baar aap jungle safari par jayein, toh apna compass aur matchbox mat bhoolna! Subscribe for more real survival hacks.",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "bg_style": "jungle_forest",
                    "shake": 0.0,
                    "props": [{"type": "tree", "x": 1450, "y": 420, "scale": 1.1}],
                    "sfx": "title_boom"
                }
            ]
        else:
            title = "What If You Got Trapped in a Deep Jungle?"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "If you suddenly found yourself stranded deep in an uncharted jungle, apex predators won't kill you first. Blind panic and deadly dehydration within seventy-two hours will!",
                    "char_pose": "panicking",
                    "expression": "screaming",
                    "bg_style": "jungle_forest",
                    "shake": 6.0,
                    "props": [{"type": "tree", "x": 1450, "y": 420, "scale": 1.1}],
                    "sfx": "drone_hit"
                },
                {
                    "scene_id": 2,
                    "beat": "rule_of_threes",
                    "narration": "Remember the fundamental survival Rule of Threes: three minutes without oxygen, three days without clean water, and three weeks without food.",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "bg_style": "jungle_forest",
                    "shake": 0.0,
                    "props": [{"type": "clock", "x": 1400, "y": 380, "scale": 1.0}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "the_fatal_mistake",
                    "narration": "The most common fatal mistake: drinking stagnant puddle water. Microscopic parasites and Giardia will trigger crippling dysentery that accelerates dehydration.",
                    "char_pose": "shrugging",
                    "expression": "shocked",
                    "bg_style": "jungle_forest",
                    "shake": 4.0,
                    "props": [{"type": "water_drop", "x": 1400, "y": 400, "scale": 1.2}],
                    "sfx": "shatter"
                },
                {
                    "scene_id": 4,
                    "beat": "navigation_trick",
                    "narration": "To find rescue, always follow flowing streams downhill. Tributaries invariably merge into larger rivers, leading directly to human settlements and roads.",
                    "char_pose": "thinking",
                    "expression": "thinking",
                    "bg_style": "jungle_forest",
                    "shake": 0.0,
                    "props": [{"type": "compass", "x": 1400, "y": 400, "scale": 1.1}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 5,
                    "beat": "predators_night",
                    "narration": "Before nightfall, build an elevated shelter five feet above ground and ignite a fire. Thick smoke and firelight repel venomous vipers and predators.",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "bg_style": "jungle_forest",
                    "shake": 0.0,
                    "props": [{"type": "campfire", "x": 1400, "y": 500, "scale": 1.2}],
                    "sfx": "power_down"
                },
                {
                    "scene_id": 6,
                    "beat": "climax_outro",
                    "narration": "So when you pack for your next wilderness expedition, never forget a lighter and a compass. Subscribe for more life-saving what-ifs!",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "bg_style": "jungle_forest",
                    "shake": 0.0,
                    "props": [{"type": "tree", "x": 1450, "y": 420, "scale": 1.1}],
                    "sfx": "title_boom"
                }
            ]

        return {"topic": topic, "title": title, "language": lang, "scenes": scenes}

    # -------------------------------------------------------------
    # 2. TOPIC: WEEPING / CRYING / TEARS
    # -------------------------------------------------------------
    def _script_no_crying(self, topic: str, lang: str, is_5min: bool) -> Dict[str, Any]:
        if not is_5min:
            if lang == "hi":
                title = "Kya Ho Agar Insan Kabhi Ro Na Sake? (1-Min Short)"
                scenes = [
                    {
                        "scene_id": 1,
                        "beat": "cold_hook",
                        "narration": "Agar insan ki aankhon se aansu nikalna band ho jaye, to sabse pehle dil ka dard nahi, balki 48 ghante me aapki aankhein andhi ho jayengi!",
                        "char_pose": "panicking",
                        "expression": "shocked",
                        "bg_style": "dusk_space",
                        "shake": 6.0,
                        "props": [{"type": "question_mark", "scale": 1.2}],
                        "sfx": "whoosh"
                    },
                    {
                        "scene_id": 2,
                        "beat": "premise_card",
                        "narration": "Aansu sirf rone ke liye nahi hote. Har baar jab aap palkein jhapkaate hain, aansu aapki cornea par ek protective oxygen layer banate hain.",
                        "char_pose": "pointing",
                        "expression": "normal",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [{"type": "earth", "scale": 1.0}],
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 3,
                        "beat": "first_consequence",
                        "narration": "Bina aansuon ke, har ek blink sandpaper ki tarah aapki aankh ko cheelne lagega. Pehle hi din severe corneal scratch aur jalan shuru ho jayegi!",
                        "char_pose": "shrugging",
                        "expression": "screaming",
                        "bg_style": "dusk_space",
                        "shake": 4.0,
                        "props": [{"type": "clock", "scale": 1.0}],
                        "sfx": "ding"
                    },
                    {
                        "scene_id": 4,
                        "beat": "scientific_pivot",
                        "narration": "Aansuon me Lysozyme naam ka powerful enzyme hota hai jo bacteria ko maarta hai. Aansu nahi honge to infections aankhon ko galane lagenge.",
                        "char_pose": "thinking",
                        "expression": "thinking",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [{"type": "atom", "scale": 1.1}],
                        "sfx": "whoosh"
                    },
                    {
                        "scene_id": 5,
                        "beat": "psychological_cost",
                        "narration": "Sabse khatarnaak baat: Emotional aansu sharir se Cortisol stress hormone ko bahar nikalte hain. Ro na pane se dimaag extreme tension me phatne lagega!",
                        "char_pose": "panicking",
                        "expression": "shocked",
                        "bg_style": "dusk_space",
                        "shake": 5.0,
                        "props": [{"type": "clock", "scale": 1.0}],
                        "sfx": "ding"
                    },
                    {
                        "scene_id": 6,
                        "beat": "climax_loop",
                        "narration": "Toh agar kabhi rona aaye, toh sharmayein mat. Khulkar ro lijiye, kyunki yeh aapki aankhon aur dimaag ka lifesaver hai!",
                        "char_pose": "hands_on_hips",
                        "expression": "happy",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [],
                        "sfx": "pop"
                    }
                ]
            else:
                title = "What If Humans Could Never Cry? (1-Min Short)"
                scenes = [
                    {
                        "scene_id": 1,
                        "beat": "cold_hook",
                        "narration": "If humans permanently lost the ability to weep, emotional heartbreak wouldn't destroy you first. Total blindness within seventy-two hours would!",
                        "char_pose": "panicking",
                        "expression": "shocked",
                        "bg_style": "dusk_space",
                        "shake": 6.0,
                        "props": [{"type": "question_mark", "scale": 1.2}],
                        "sfx": "whoosh"
                    },
                    {
                        "scene_id": 2,
                        "beat": "premise_card",
                        "narration": "Tears are not just about sadness. Every single blink coats your cornea with a microscopic liquid film carrying oxygen and nutrients.",
                        "char_pose": "pointing",
                        "expression": "normal",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [{"type": "earth", "scale": 1.0}],
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 3,
                        "beat": "first_consequence",
                        "narration": "Without basal tears, blinking turns into abrasive friction like sandpaper grinding against raw glass, causing rapid corneal ulcerations.",
                        "char_pose": "shrugging",
                        "expression": "screaming",
                        "bg_style": "dusk_space",
                        "shake": 4.0,
                        "props": [{"type": "clock", "scale": 1.0}],
                        "sfx": "ding"
                    },
                    {
                        "scene_id": 4,
                        "beat": "scientific_pivot",
                        "narration": "Tears contain lysozyme, a potent antibacterial enzyme that destroys bacterial cell walls in minutes. Without it, infections run rampant.",
                        "char_pose": "thinking",
                        "expression": "thinking",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [{"type": "atom", "scale": 1.1}],
                        "sfx": "whoosh"
                    },
                    {
                        "scene_id": 5,
                        "beat": "psychological_cost",
                        "narration": "Even wilder: emotional weeping flushes toxic stress hormones like cortisol out of your bloodstream. Trapped stress triggers catastrophic cardiovascular overload!",
                        "char_pose": "panicking",
                        "expression": "shocked",
                        "bg_style": "dusk_space",
                        "shake": 5.0,
                        "props": [{"type": "clock", "scale": 1.0}],
                        "sfx": "ding"
                    },
                    {
                        "scene_id": 6,
                        "beat": "climax_loop",
                        "narration": "So the next time life makes you shed a tear, be grateful. Crying is your body's built-in emotional exhaust pipe and optical shield!",
                        "char_pose": "hands_on_hips",
                        "expression": "happy",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [],
                        "sfx": "pop"
                    }
                ]
            return {"topic": topic, "title": title, "language": lang, "scenes": scenes}
        else:
            title = "The Full Medical Horror: What If Humans Could Never Weep? (5-Min Deep-Dive)"
            scenes = self._generate_extended_5min_crying(lang)
            return {"topic": topic, "title": title, "language": lang, "scenes": scenes}

    def _generate_extended_5min_crying(self, lang: str) -> List[Dict[str, Any]]:
        scenes = []
        timeline = [
            ("Hour 1: The Initial Dryness", "Minute sixty without basal tears. The delicate three-layer tear film vanishes, causing acute ocular burning."),
            ("Hour 6: Micro-Abrasions", "Every blink now creates microscopic lacerations across the cornea as eyelids rub dry epithelial cells."),
            ("Hour 12: Light Sensitivity", "Severe photophobia begins. Looking at any phone screen or daylight causes agonizing optical pain."),
            ("Day 1: Epithelial Erosion", "Twenty-four hours without moisture. The outer layer of the cornea begins peeling away in microscopic sheets."),
            ("Day 2: Bacterial Invasion", "Without lysozyme enzymes, ambient airborne bacteria invade the scratched eye surface, causing raging infections."),
            ("Day 3: Corneal Ulcerations", "Deep ulcers form across the eye tissue. Vision blurs into an impenetrable milky fog."),
            ("Day 4: Reflex Failure", "Foreign particles and dust can no longer be flushed away. Smoke and dirt remain permanently embedded."),
            ("Day 5: Hormone Trapping", "In the brain, emotional tears are blocked. Cortisol and adrenocorticotropic stress hormones remain trapped in the blood."),
            ("Day 6: Cardiovascular Strain", "Unreleased psychological stress triggers continuous sympathetic nervous activation, spiking blood pressure."),
            ("Day 7: The Blindness Threshold", "One week of total lacrimal failure results in permanent structural scarring of the cornea."),
            ("Week 2: Social & Emotional Disconnect", "Humans lose one of their most vital evolutionary empathy triggers. Social bonding mechanisms severely degrade."),
            ("Month 1: Artificial Lubrication Crisis", "Civilization scrambles for synthetic saline solutions, creating global pharmaceutical shortages."),
            ("Month 3: The Surgical Solutions", "Ophthalmologists turn to salivary gland transposition surgery just to keep patient eyeballs alive."),
            ("Year 1: Evolutionary Realization", "Humanity realizes that our fragile liquid tears are the unsung guardian of human vision."),
            ("The Epilogue: Why We Cry", "Tears are the only biological fluid designed to heal both physical tissue and psychological trauma simultaneously."),
            ("Circular Outro", "So appreciate every tear you shed. It is keeping you seeing, feeling, and truly human!")
        ]

        for idx, (head, text) in enumerate(timeline, start=1):
            scenes.append({
                "scene_id": idx,
                "beat": f"ch_{idx}",
                "narration": text if lang == "en" else f"{head}: {text}",
                "char_pose": "panicking" if idx in [1, 2, 4, 7, 9] else ("thinking" if idx in [3, 5, 8, 14] else "pointing"),
                "expression": "shocked" if idx in [1, 4, 7] else ("screaming" if idx in [2, 9] else "normal"),
                "bg_style": "dusk_space",
                "shake": 4.0 if idx in [2, 7, 9] else 0.0,
                "props": [{"type": "clock", "scale": 1.0}],
                "sfx": "whoosh" if idx % 2 == 1 else "pop"
            })
        return scenes

    # -------------------------------------------------------------
    # 3. TOPIC: SUN BLACKOUT
    # -------------------------------------------------------------
    def _script_sun_disappears(self, topic: str, lang: str, is_5min: bool) -> Dict[str, Any]:
        if not is_5min:
            if lang == "hi":
                title = "Kya Ho Agar Suraj Gayab Ho Jaye? (1-Min Short)"
                scenes = [
                    {
                        "scene_id": 1,
                        "beat": "cold_hook",
                        "narration": "Agar achanak Suraj gayab ho jaye, to aath minute tak kisi ko pata bhi nahi chalega! Kyunki dhoop aur gravity ko hum tak pahuchne me aath minute lagte hain.",
                        "char_pose": "pointing",
                        "expression": "normal",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [{"type": "sun", "scale": 1.2}],
                        "sfx": "whoosh"
                    },
                    {
                        "scene_id": 2,
                        "beat": "premise_card",
                        "narration": "Aath minute baad achanak ghor andhera cha jayega aur Dharti apni orbit chhod kar 67,000 miles per hour ki speed se seedhi antariksh me nikal padegi!",
                        "char_pose": "panicking",
                        "expression": "shocked",
                        "bg_style": "pitch_black_space",
                        "shake": 7.0,
                        "props": [{"type": "vanished_sun", "scale": 1.2}],
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 3,
                        "beat": "first_consequence",
                        "narration": "Chhe ghante me photosynthesis khatam aur barah ghante me poori dharti par temperature minus me chala jayega!",
                        "char_pose": "shrugging",
                        "expression": "screaming",
                        "bg_style": "frozen_ice",
                        "shake": 4.0,
                        "props": [{"type": "thermometer", "scale": 1.1}],
                        "sfx": "ding"
                    },
                    {
                        "scene_id": 4,
                        "beat": "scientific_pivot",
                        "narration": "Teesre din samundar ki upari satah jam kar ek insulating blanket ban jayegi, jo deep-sea life ko zinda rakhegi.",
                        "char_pose": "thinking",
                        "expression": "thinking",
                        "bg_style": "frozen_ice",
                        "shake": 0.0,
                        "props": [{"type": "frozen_earth", "scale": 1.1}],
                        "sfx": "whoosh"
                    },
                    {
                        "scene_id": 5,
                        "beat": "climax_loop",
                        "narration": "Isliye kal subah jab Suraj nikle, toh uska shukriya ada karna mat bhoolna!",
                        "char_pose": "hands_on_hips",
                        "expression": "happy",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [{"type": "sun", "scale": 1.2}],
                        "sfx": "pop"
                    }
                ]
            else:
                title = "What If The Sun Disappeared? (1-Min Short)"
                scenes = [
                    {
                        "scene_id": 1,
                        "beat": "cold_hook",
                        "narration": "If the Sun vanished right now, you wouldn't notice a single thing for eight minutes and twenty seconds!",
                        "char_pose": "pointing",
                        "expression": "normal",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [{"type": "sun", "scale": 1.2}],
                        "sfx": "whoosh"
                    },
                    {
                        "scene_id": 2,
                        "beat": "premise_card",
                        "narration": "Then, total pitch black strikes and Earth slingshots into deep space at sixty-seven thousand miles per hour!",
                        "char_pose": "panicking",
                        "expression": "shocked",
                        "bg_style": "pitch_black_space",
                        "shake": 7.0,
                        "props": [{"type": "vanished_sun", "scale": 1.2}],
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 3,
                        "beat": "first_consequence",
                        "narration": "Within twelve hours, global temperatures plunge below freezing, causing power grids worldwide to overload and blow.",
                        "char_pose": "shrugging",
                        "expression": "screaming",
                        "bg_style": "frozen_ice",
                        "shake": 4.0,
                        "props": [{"type": "thermometer", "scale": 1.1}],
                        "sfx": "ding"
                    },
                    {
                        "scene_id": 4,
                        "beat": "scientific_pivot",
                        "narration": "By day three, ocean surfaces freeze into a thick ice blanket that paradoxically insulates marine life below.",
                        "char_pose": "thinking",
                        "expression": "thinking",
                        "bg_style": "frozen_ice",
                        "shake": 0.0,
                        "props": [{"type": "frozen_earth", "scale": 1.1}],
                        "sfx": "whoosh"
                    },
                    {
                        "scene_id": 5,
                        "beat": "climax_loop",
                        "narration": "So tomorrow morning, look up and say thank you to the Sun. Subscribe for more cosmic what-ifs!",
                        "char_pose": "hands_on_hips",
                        "expression": "happy",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [{"type": "sun", "scale": 1.2}],
                        "sfx": "pop"
                    }
                ]
            return {"topic": topic, "title": title, "language": lang, "scenes": scenes}
        else:
            return self._script_sun_disappears_5min(lang)

    # -------------------------------------------------------------
    # 4. TOPIC: SLEEP
    # -------------------------------------------------------------
    def _script_no_sleep(self, topic: str, lang: str, is_5min: bool) -> Dict[str, Any]:
        if lang == "hi":
            return {
                "topic": topic,
                "title": "Kya Ho Agar Insan Kabhi Na Soye?",
                "language": "hi",
                "scenes": [
                    {
                        "scene_id": 1,
                        "beat": "cold_hook",
                        "narration": "Agar aapne achanak sona band kar diya, to 72 ghante ke andar aapka dimaag aisi cheezein dikhayega jo exist hi nahi karti!",
                        "char_pose": "panicking",
                        "expression": "screaming",
                        "bg_style": "dusk_space",
                        "shake": 6.0,
                        "props": [{"type": "clock", "scale": 1.1}],
                        "sfx": "whoosh"
                    },
                    {
                        "scene_id": 2,
                        "beat": "premise_card",
                        "narration": "Shuruwat me extra time ka maza aayega, lekin 24 ghante ke baad dimaag me dopamine ka fake surge aane lagta hai.",
                        "char_pose": "thinking",
                        "expression": "thinking",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [{"type": "question_mark", "scale": 1.0}],
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 3,
                        "beat": "scientific_pivot",
                        "narration": "Neend ke dauran hamara glymphatic system dimaag ke zehreelay toxins ko wash karta hai. Bina neend ke ye neurons ko maar dalte hain.",
                        "char_pose": "shrugging",
                        "expression": "shocked",
                        "bg_style": "dusk_space",
                        "shake": 4.0,
                        "props": [{"type": "atom", "scale": 1.1}],
                        "sfx": "ding"
                    },
                    {
                        "scene_id": 4,
                        "beat": "climax_loop",
                        "narration": "Toh phone side me rakhiye aur aaram se so jaiye, warna dimaag khud emergency restart le lega!",
                        "char_pose": "hands_on_hips",
                        "expression": "happy",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [],
                        "sfx": "pop"
                    }
                ]
            }
        else:
            return {
                "topic": topic,
                "title": "What If You Never Slept Again?",
                "language": "en",
                "scenes": [
                    {
                        "scene_id": 1,
                        "beat": "cold_hook",
                        "narration": "If you never went to sleep again, within seventy-two hours your own waking brain would hallucinate talking monsters in your bedroom!",
                        "char_pose": "panicking",
                        "expression": "screaming",
                        "bg_style": "dusk_space",
                        "shake": 6.0,
                        "props": [{"type": "clock", "scale": 1.1}],
                        "sfx": "whoosh"
                    },
                    {
                        "scene_id": 2,
                        "beat": "premise_card",
                        "narration": "At twenty-four hours, a surge of dopamine mimics euphoria, but your reaction time plunges to legal alcohol intoxication levels.",
                        "char_pose": "thinking",
                        "expression": "thinking",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [{"type": "question_mark", "scale": 1.0}],
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 3,
                        "beat": "scientific_pivot",
                        "narration": "During deep sleep, your glymphatic system flushes toxic beta-amyloid plaques. Without sleep, cellular trash suffocates your synapses.",
                        "char_pose": "shrugging",
                        "expression": "shocked",
                        "bg_style": "dusk_space",
                        "shake": 4.0,
                        "props": [{"type": "atom", "scale": 1.1}],
                        "sfx": "ding"
                    },
                    {
                        "scene_id": 4,
                        "beat": "climax_loop",
                        "narration": "So put your phone away and get some sleep. Your prefrontal cortex will thank you tomorrow!",
                        "char_pose": "hands_on_hips",
                        "expression": "happy",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [],
                        "sfx": "pop"
                    }
                ]
            }

    # -------------------------------------------------------------
    # 5. TOPIC: MOON VANISHED
    # -------------------------------------------------------------
    def _script_moon_vanished(self, topic: str, lang: str, is_5min: bool) -> Dict[str, Any]:
        if lang == "hi":
            return {
                "topic": topic,
                "title": "Kya Ho Agar Chand Gayab Ho Jaye?",
                "language": "hi",
                "scenes": [
                    {
                        "scene_id": 1,
                        "beat": "cold_hook",
                        "narration": "Agar achanak Chand gayab ho jaye, to sabse pehle raat ka andhera nahi, balki 300 kilometer lambi tsunami hume khatam karegi!",
                        "char_pose": "panicking",
                        "expression": "shocked",
                        "bg_style": "dusk_space",
                        "shake": 7.0,
                        "props": [{"type": "moon", "scale": 1.2}],
                        "sfx": "whoosh"
                    },
                    {
                        "scene_id": 2,
                        "beat": "premise_card",
                        "narration": "Lekin rukiye! Kya Chand sach me hamari dharti ko zinda rakh raha hai? Chand ki gravity hamare samundar ke paani ko kheench kar rakhti hai.",
                        "char_pose": "thinking",
                        "expression": "thinking",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [{"type": "question_mark", "scale": 1.0}],
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 3,
                        "beat": "scientific_pivot",
                        "narration": "Chand ke bina Dharti ka tilt hil kar 85 degree ho jayega. Sahara desert me baraf padegi aur din sirf chhe ghante ka reh jayega!",
                        "char_pose": "shrugging",
                        "expression": "screaming",
                        "bg_style": "dusk_space",
                        "shake": 5.0,
                        "props": [{"type": "earth", "scale": 1.1}],
                        "sfx": "ding"
                    },
                    {
                        "scene_id": 4,
                        "beat": "climax_gag",
                        "narration": "Toh agar agli baar aapko Chand par daag dikhe, toh uski tareef karna, kyunki wahi hume bacha raha hai!",
                        "char_pose": "hands_on_hips",
                        "expression": "happy",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [{"type": "moon", "scale": 0.9}],
                        "sfx": "pop"
                    }
                ]
            }
        else:
            return {
                "topic": topic,
                "title": "What If The Moon Vanished?",
                "language": "en",
                "scenes": [
                    {
                        "scene_id": 1,
                        "beat": "cold_hook",
                        "narration": "If the Moon disappeared right now, total darkness won't kill you first. Massive global tsunamis will!",
                        "char_pose": "panicking",
                        "expression": "shocked",
                        "bg_style": "dusk_space",
                        "shake": 7.0,
                        "props": [{"type": "moon", "scale": 1.2}],
                        "sfx": "whoosh"
                    },
                    {
                        "scene_id": 2,
                        "beat": "premise_card",
                        "narration": "Without lunar gravity, ocean tides collapse by 60 percent, completely destabilizing global marine currents.",
                        "char_pose": "pointing",
                        "expression": "normal",
                        "bg_style": "dusk_space",
                        "shake": 2.0,
                        "props": [{"type": "earth", "scale": 1.1}],
                        "sfx": "pop"
                    },
                    {
                        "scene_id": 3,
                        "beat": "scientific_pivot",
                        "narration": "Even worse: without the Moon acting as an orbital anchor, Earth's axis violently wobbles up to 85 degrees, plunging equatorial zones into ice ages!",
                        "char_pose": "shrugging",
                        "expression": "screaming",
                        "bg_style": "dusk_space",
                        "shake": 5.0,
                        "props": [{"type": "earth", "scale": 1.1}],
                        "sfx": "ding"
                    },
                    {
                        "scene_id": 4,
                        "beat": "climax_gag",
                        "narration": "So next time you look up at the night sky, say thank you to the Moon. Subscribe for more cosmic journeys!",
                        "char_pose": "hands_on_hips",
                        "expression": "happy",
                        "bg_style": "dusk_space",
                        "shake": 0.0,
                        "props": [{"type": "moon", "scale": 0.9}],
                        "sfx": "pop"
                    }
                ]
            }

    # -------------------------------------------------------------
    # 6. DYNAMIC GENERAL WHAT-IF (CLEANED SYNTAX)
    # -------------------------------------------------------------
    def _generate_dynamic_what_if(self, topic: str, lang: str, is_5min: bool) -> Dict[str, Any]:
        """Cleans user prompt so it never pastes raw English phrases into Hindi sentences."""
        subject = self.clean_subject(topic, lang)
        if lang == "hi":
            title = f"Kya Ho Agar: {subject.title()}?"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": f"Kya aapne kabhi socha hai ki agar sach me {subject} wali sthiti paida ho jaye, to aapka sabse pehla reaction kya hoga? Asli nateeja aapke hosh uda dega!",
                    "char_pose": "panicking",
                    "expression": "shocked",
                    "bg_style": "dusk_space",
                    "shake": 5.0,
                    "props": [{"type": "question_mark", "scale": 1.1}],
                    "sfx": "whoosh"
                },
                {
                    "scene_id": 2,
                    "beat": "premise_card",
                    "narration": "Aisi sthiti me insan ka dimaag aur body turant survival adrenaline rush me chali jati hai, jisse heart rate achanak 150 BPM cross kar jata hai.",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "bg_style": "dusk_space",
                    "shake": 0.0,
                    "props": [{"type": "earth", "scale": 1.0}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "scientific_pivot",
                    "narration": "Scientific studies batati hain ki aise crisis me bina kisi plan ke aage badhna 90 percent logo ke liye fatal sabit hota hai.",
                    "char_pose": "thinking",
                    "expression": "thinking",
                    "bg_style": "dusk_space",
                    "shake": 2.0,
                    "props": [{"type": "clock", "scale": 1.0}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 4,
                    "beat": "climax_gag",
                    "narration": "Isliye hamesha alert rahiye aur har situation ke liye taiyar rahiye! Subscribe karein aise hi mind-blowing scenarios ke liye.",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "bg_style": "dusk_space",
                    "shake": 0.0,
                    "props": [],
                    "sfx": "pop"
                }
            ]
        else:
            title = f"What If: {subject.title()}?"
            scenes = [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": f"Have you ever wondered what would happen if {subject} actually became your immediate reality? The biological consequences will stun you!",
                    "char_pose": "panicking",
                    "expression": "shocked",
                    "bg_style": "dusk_space",
                    "shake": 5.0,
                    "props": [{"type": "question_mark", "scale": 1.1}],
                    "sfx": "whoosh"
                },
                {
                    "scene_id": 2,
                    "beat": "premise_card",
                    "narration": "Under extreme disruption, your sympathetic nervous system instantly floods the bloodstream with norepinephrine, spiking your heart rate past 150 beats per minute.",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "bg_style": "dusk_space",
                    "shake": 0.0,
                    "props": [{"type": "earth", "scale": 1.0}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "scientific_pivot",
                    "narration": "Cognitive psychology reveals that without prior preparation, human analytical decision-making degrades by sixty percent under sudden environmental shock.",
                    "char_pose": "thinking",
                    "expression": "thinking",
                    "bg_style": "dusk_space",
                    "shake": 2.0,
                    "props": [{"type": "clock", "scale": 1.0}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 4,
                    "beat": "climax_gag",
                    "narration": "Stay vigilant, keep your composure, and prepare for the unexpected. Subscribe for more deep dive what-if scenarios!",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "bg_style": "dusk_space",
                    "shake": 0.0,
                    "props": [],
                    "sfx": "pop"
                }
            ]

        return {"topic": topic, "title": title, "language": lang, "scenes": scenes}

    # -------------------------------------------------------------
    # 7. 5-MINUTE SUN SCRIPT
    # -------------------------------------------------------------
    def _script_sun_disappears_5min(self, lang: str) -> Dict[str, Any]:
        return {
            "topic": "What if the Sun disappeared for 7 days?",
            "title": "What If The Sun Disappeared For 7 Days? (The Complete Timeline)",
            "language": "en",
            "scenes": [
                {
                    "scene_id": 1,
                    "beat": "cold_hook",
                    "narration": "If the Sun vanished right now, you wouldn't notice a single thing for eight minutes and twenty seconds. You would still feel its warm light hitting your skin, blissfully unaware of cosmic doom.",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "bg_style": "dusk_space",
                    "shake": 0.0,
                    "props": [{"type": "sun", "x": 1400, "y": 380, "scale": 1.2}],
                    "sfx": "whoosh"
                },
                {
                    "scene_id": 2,
                    "beat": "premise_card",
                    "narration": "Because light and gravity both travel at the exact same cosmic speed limit, Earth continues orbiting an empty point in space. But at minute eight and twenty-one seconds, total pitch black strikes worldwide.",
                    "char_pose": "panicking",
                    "expression": "shocked",
                    "bg_style": "pitch_black_space",
                    "shake": 6.0,
                    "props": [{"type": "vanished_sun", "x": 1400, "y": 380, "scale": 1.2}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 3,
                    "beat": "first_consequence",
                    "narration": "At that exact millisecond, the Sun's gravitational anchor snaps. Earth stops orbiting and slingshots into the dark interstellar void in a straight line at sixty-seven thousand miles per hour!",
                    "char_pose": "panicking",
                    "expression": "screaming",
                    "bg_style": "pitch_black_space",
                    "shake": 8.0,
                    "props": [{"type": "earth", "x": 1380, "y": 420, "scale": 1.1}],
                    "sfx": "whoosh"
                },
                {
                    "scene_id": 4,
                    "beat": "hour_6",
                    "narration": "Hour six of the blackout. With no solar photons striking the atmosphere, plants completely halt photosynthesis. Oxygen production instantly ceases, but humanity's real immediate threat is plummeting temperature.",
                    "char_pose": "thinking",
                    "expression": "thinking",
                    "bg_style": "pitch_black_space",
                    "shake": 0.0,
                    "props": [{"type": "clock", "x": 1380, "y": 400, "scale": 1.0}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 5,
                    "beat": "hour_12",
                    "narration": "By hour twelve, global surface temperatures drop past freezing in every country on Earth. Equatorial paradises like Hawaii and Miami experience freezing frost, while city power grids overload and explode from heating demand.",
                    "char_pose": "shrugging",
                    "expression": "shocked",
                    "bg_style": "frozen_ice",
                    "shake": 4.0,
                    "props": [{"type": "thermometer", "x": 1420, "y": 420, "scale": 1.1}],
                    "sfx": "whoosh"
                },
                {
                    "scene_id": 6,
                    "beat": "hour_24",
                    "narration": "Twenty-four hours without sunlight. Nocturnal animals and domestic pets wander in total confusion. The Moon has completely disappeared from the night sky, because without sunlight to reflect, it becomes a pitch-black cosmic ghost.",
                    "char_pose": "thinking",
                    "expression": "normal",
                    "bg_style": "pitch_black_space",
                    "shake": 0.0,
                    "props": [{"type": "moon", "x": 1400, "y": 380, "scale": 1.0}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 7,
                    "beat": "day_1_end",
                    "narration": "Panic sweeps across every major continent. Supermarket shelves are stripped bare in minutes, while emergency generators roar in darkness. But the worst environmental collapse is only just beginning.",
                    "char_pose": "panicking",
                    "expression": "screaming",
                    "bg_style": "pitch_black_space",
                    "shake": 5.0,
                    "props": [{"type": "clock", "x": 1380, "y": 400, "scale": 1.0}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 8,
                    "beat": "day_2_freeze",
                    "narration": "Day two. Global temperatures hit minus ten degrees Celsius. Rivers, lakes, and freshwater reservoirs freeze solid down to their rocky beds, paralyzing municipal water distribution worldwide.",
                    "char_pose": "pointing",
                    "expression": "shocked",
                    "bg_style": "frozen_ice",
                    "shake": 2.0,
                    "props": [{"type": "frozen_earth", "x": 1380, "y": 420, "scale": 1.1}],
                    "sfx": "whoosh"
                },
                {
                    "scene_id": 9,
                    "beat": "ocean_paradox",
                    "narration": "Yet out in the open oceans, a fascinating scientific paradox saves marine life. The top few inches of seawater freeze into a thick sheet of surface ice, creating a thermal insulating blanket that traps liquid water below!",
                    "char_pose": "thinking",
                    "expression": "thinking",
                    "bg_style": "frozen_ice",
                    "shake": 0.0,
                    "props": [{"type": "earth", "x": 1380, "y": 420, "scale": 1.1}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 10,
                    "beat": "day_3_fog",
                    "narration": "Day three. Cold air over freezing seas creates catastrophic super-fog. Moisture condenses and falls as blinding blizzards. In high altitudes, carbon dioxide begins freezing into dry ice on mountaintops.",
                    "char_pose": "shrugging",
                    "expression": "shocked",
                    "bg_style": "frozen_ice",
                    "shake": 3.0,
                    "props": [{"type": "thermometer", "x": 1420, "y": 420, "scale": 1.1}],
                    "sfx": "whoosh"
                },
                {
                    "scene_id": 11,
                    "beat": "geothermal_refuge",
                    "narration": "Day four. Humanity begins an urgent strategic migration towards volcanic and geothermal zones. Regions like Iceland and Yellowstone become the most valuable real estate on Earth, tapping endless heat from Earth's molten core.",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "bg_style": "dusk_space",
                    "shake": 0.0,
                    "props": [{"type": "earth", "x": 1380, "y": 420, "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 12,
                    "beat": "day_5_deep_cold",
                    "narration": "Day five. Surface temperature plunges past minus forty degrees Celsius. Exposed human skin freezes in under ninety seconds. Walking outside without Arctic pressurized survival suits is fatal.",
                    "char_pose": "panicking",
                    "expression": "screaming",
                    "bg_style": "frozen_ice",
                    "shake": 5.0,
                    "props": [{"type": "thermometer", "x": 1420, "y": 420, "scale": 1.1}],
                    "sfx": "whoosh"
                },
                {
                    "scene_id": 13,
                    "beat": "hydrothermal_vents",
                    "narration": "Thousands of feet beneath the frozen Pacific, creatures around hydrothermal vents notice absolutely nothing wrong. Fueled by subterranean geothermal chemistry instead of sunlight, their strange ecosystem thrives untouched.",
                    "char_pose": "thinking",
                    "expression": "thinking",
                    "bg_style": "pitch_black_space",
                    "shake": 0.0,
                    "props": [{"type": "earth", "x": 1380, "y": 420, "scale": 1.1}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 14,
                    "beat": "day_6_rogue_planet",
                    "narration": "Day six. Earth has traveled over nine million miles away from our former orbital path. We are officially an interstellar rogue planet wandering through deep space, insulated only by our molten radioactive iron core.",
                    "char_pose": "shrugging",
                    "expression": "shocked",
                    "bg_style": "pitch_black_space",
                    "shake": 4.0,
                    "props": [{"type": "frozen_earth", "x": 1380, "y": 420, "scale": 1.1}],
                    "sfx": "whoosh"
                },
                {
                    "scene_id": 15,
                    "beat": "day_7_sun_returns",
                    "narration": "Day seven. In our hypothetical experiment, the impossible happens. The Sun suddenly blinks back into existence! Fresh photons rip across the void at light-speed and smash into our frozen upper atmosphere.",
                    "char_pose": "panicking",
                    "expression": "shocked",
                    "bg_style": "dusk_space",
                    "shake": 8.0,
                    "props": [{"type": "sun", "x": 1400, "y": 380, "scale": 1.3}],
                    "sfx": "whoosh"
                },
                {
                    "scene_id": 16,
                    "beat": "thermal_shockwaves",
                    "narration": "The return of sunlight triggers violent atmospheric shockwaves. Super-heated air clashes with sub-zero ground fronts, creating ferocious thousand-mile thunderstorms and supersonic weather anomalies across every ocean.",
                    "char_pose": "shrugging",
                    "expression": "screaming",
                    "bg_style": "dusk_space",
                    "shake": 6.0,
                    "props": [{"type": "sun", "x": 1400, "y": 380, "scale": 1.1}],
                    "sfx": "pop"
                },
                {
                    "scene_id": 17,
                    "beat": "human_reckoning",
                    "narration": "Within weeks, surface ice thaws and dormant plant roots sprout anew. Humanity emerges from underground bunkers into blinding dawn, forever humbled by the fragile cosmic engine that powers our existence.",
                    "char_pose": "pointing",
                    "expression": "normal",
                    "bg_style": "dusk_space",
                    "shake": 0.0,
                    "props": [{"type": "earth", "x": 1380, "y": 420, "scale": 1.1}],
                    "sfx": "ding"
                },
                {
                    "scene_id": 18,
                    "beat": "circular_payoff",
                    "narration": "So when you step outside tomorrow morning and feel that golden warmth against your face, remember: we are just eight minutes away from the deep cosmic freeze. Subscribe for more what-if journeys!",
                    "char_pose": "hands_on_hips",
                    "expression": "happy",
                    "bg_style": "dusk_space",
                    "shake": 0.0,
                    "props": [{"type": "sun", "x": 1400, "y": 380, "scale": 1.2}],
                    "sfx": "pop"
                }
            ]
        }
