"""
Prompt Templates & 7-Beat Viral Formula Rules
Enforces viral storytelling structure and strict style locks.
"""

VIRAL_7_BEAT_SCHEMA = {
    "type": "object",
    "properties": {
        "topic": {"type": "string"},
        "title": {"type": "string"},
        "language": {"type": "string", "enum": ["hi", "en"]},
        "scenes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "scene_id": {"type": "integer"},
                    "beat": {
                        "type": "string",
                        "enum": [
                            "cold_hook",        # Beat 1: 0-4s high stakes shock
                            "premise_card",     # Beat 2: 4-8s question & title card
                            "first_consequence",# Beat 3: 8-16s funny / fast breakdown
                            "scientific_pivot", # Beat 4: 16-28s real evidence / myth-break
                            "escalation_domino",# Beat 5: 28-40s extreme domino effect
                            "climax_gag",       # Beat 6: 40-50s peak realization
                            "circular_payoff"   # Beat 7: 50-60s callback loop to Beat 1
                        ]
                    },
                    "narration": {"type": "string"},
                    "char_pose": {
                        "type": "string",
                        "enum": ["idle", "pointing", "thinking", "shrugging", "panicking", "hands_on_hips"]
                    },
                    "expression": {
                        "type": "string",
                        "enum": ["normal", "shocked", "thinking", "screaming", "deadpan"]
                    },
                    "bg_style": {"type": "string", "enum": ["dusk_space", "webcomic_light"]},
                    "shake": {"type": "number"},
                    "props": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string"},
                                "scale": {"type": "number"}
                            }
                        }
                    },
                    "sfx": {"type": "string", "enum": ["whoosh", "pop", "ding", "none"]}
                },
                "required": ["scene_id", "beat", "narration", "char_pose", "expression"]
            }
        }
    }
}

STYLE_LOCK_PROMPT = """
You are CARTOON-JARVIS, an elite YouTube Explainer & 'What If' Animation Director.
Your task is to take a core question or topic and write a high-retention 7-Beat narrative script.

CRITICAL RETENTION RULES:
1. BEAT 1 (Cold Hook): Start in the middle of chaos. No greeting ("Hello friends"). Instant shock.
2. BEAT 2 (Premise): State the core question with intense curiosity.
3. BEAT 3 (First Consequence): The immediate common assumption, and why it's hilariously or horribly wrong.
4. BEAT 4 (Scientific Fact): Introduce a verified surprising scientific principle.
5. BEAT 5 (Escalation Domino): Describe what happens to humans or everyday life in 24 hours.
6. BEAT 6 (Climax): The ultimate weird conclusion.
7. BEAT 7 (Circular Loop): Connect the final sentence right back into the first sentence for infinite loop retention!

LANGUAGE GUIDELINES:
- If Hindi: Use punchy modern conversational Hinglish (clear, engaging, viral style).
- If English: Fast-paced, witty, Kurzgesagt/Casually Explained style.
"""
