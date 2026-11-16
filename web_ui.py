"""
CARTOON-JARVIS: Automated $0 Zero-Budget YouTube Video Factory
Interactive Streamlit Web UI: Text Prompt -> Viral Video + Thumbnail + YouTube Kit
"""

import os
import sys
import time
import json
import re
import streamlit as st

# Ensure workspace root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from studio.brain.ai_director import AIDirector
from studio.audio.sfx_generator import SFXGenerator
from studio.visual.thumbnail_generator import ThumbnailGenerator
from studio.renderer.chunk_renderer import ChunkRenderer
from studio.renderer.video_compiler import VideoCompiler
from studio.renderer.aitrends_bridge import generate_viral_video_aitrends
from studio.storage.storage_manager import StorageManager


# Streamlit Page Config
st.set_page_config(
    page_title="Cartoon-Jarvis • YouTube AI Animation Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark Studio Theme + Neon Accents)
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FFD93D, #6BCB77, #4D96FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-header {
        color: #A0A0B0;
        font-size: 1.05rem;
        margin-bottom: 25px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8E53 100%);
        color: white;
        font-weight: 700;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.6);
    }
    .yt-badge {
        background: #1E1E2E;
        padding: 14px 18px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
        margin-bottom: 12px;
    }
    .scene-card {
        background: #181926;
        padding: 14px;
        border-radius: 8px;
        border-left: 4px solid #FFD93D;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "_", text)[:40]


def get_available_videos():
    out_dir = "output_videos"
    if not os.path.exists(out_dir):
        return []
    files = [f for f in os.listdir(out_dir) if f.endswith(".mp4")]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(out_dir, x)), reverse=True)
    return files


# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/clapperboard.png", width=85)
    st.title("Studio Settings")

    st.markdown("### 📐 Video Format & Platform")
    aspect_choice = st.radio(
        "Aspect Ratio",
        [
            "⚡ YouTube Shorts (9:16 Vertical) — Viral Reach",
            "📺 YouTube Standard (16:9 Landscape) — Deep Dive"
        ],
        index=0
    )
    is_shorts = "Shorts" in aspect_choice
    aspect_ratio = "9:16" if is_shorts else "16:9"
    width = 1080 if is_shorts else 1920
    height = 1920 if is_shorts else 1080

    st.markdown("---")
    st.markdown("### 🌐 Language & Voice")
    lang_choice = st.selectbox(
        "Narration Language",
        ["Hindi (hi) - Madhur Neural", "English (en) - Christopher Neural"],
        index=0
    )
    lang = "hi" if "Hindi" in lang_choice else "en"
    voice_desc = "hi-IN-MadhurNeural (Energetic Male)" if lang == "hi" else "en-US-ChristopherNeural (Deep Narrative)"
    st.caption(f"🎙️ **Active Voice:** `{voice_desc}`")

    st.markdown("---")
    st.markdown("### ⏱️ Video Length")
    duration_mode = st.radio(
        "Duration Target",
        [
            "⚡ 1-Minute Short (~60s, 6-8 scenes)",
            "🎓 5-Minute Deep-Dive (~300s, 16 scenes)",
            "🔥 10-Minute Epic (~600s, 30 scenes)"
        ],
        index=0
    )
    is_5min = ("5-Minute" in duration_mode or "10-Minute" in duration_mode)
    duration_str = "10min" if "10-Minute" in duration_mode else ("5min" if "5-Minute" in duration_mode else "1min")

    st.markdown("---")
    st.markdown("### 🎨 Animation Engine")
    engine_choice = st.selectbox(
        "Rendering Engine",
        [
            "🎬 AITrends 2D Studio (Cinematic Canvas + 3D + Dusk + -14 LUFS) [Recommended]",
            "🌟 Native Cartoon Studio (Kinetic Subtitles + Full 1080p + Rim-Lit Character)"
        ],
        index=0
    )
    use_aitrends = "AITrends" in engine_choice

    style_choice = st.selectbox(
        "Cinematic Visual Style",
        ["style2a", "dayone", "hybrid", "dusk", "midnight", "golden", "neon", "storybook"],
        format_func=lambda s: {
            "style2a": "Style 2A: Modern Studio Tech (Cyan HUD + Floor Grid)",
            "dayone": "Style 2B: Day One Films (Discipline & Mindset Noir)",
            "hybrid": "Hybrid Engine: Studio Tech HUDs + Day One Story Sets",
            "dusk": "Cinematic Dusk (Warm Amber & Mauve)",
            "midnight": "Midnight Blue (Cold Navy & Rain)",
            "golden": "Golden Hour (Vibrant Orange & Teal)",
            "neon": "Neon Noir (Magenta & Cyan Bloom)",
            "storybook": "Soft Storybook (Gentle Pastel Tone)"
        }.get(s, s),
        index=0
    )

    st.markdown("---")
    st.markdown("### 🔑 AI Scripting Engine")
    api_key_input = st.text_input(
        "Gemini API Key (Optional)",
        type="password",
        placeholder="Paste free Gemini key for infinite AI topics",
        help="Leave blank to use the built-in $0 offline smart topic director!"
    )

    st.markdown("---")
    st.markdown("### 💾 Storage & Disk Usage")
    storage_mgr = StorageManager()
    summary = storage_mgr.get_storage_summary()
    st.markdown(f"**Studio Usage:** `{summary['total_system_mb']} MB` ({summary['video_count']} videos)")
    st.markdown(f"**Temp Cache:** `{summary['temp_size_mb']} MB` | **Free Disk:** `{summary['disk_free_gb']} GB`")
    if st.button("🧹 Clean Scratch Cache", use_container_width=True):
        count, freed, _ = storage_mgr.purge_temp_cache()
        st.success(f"Freed {freed} MB ({count} scratch files)")
        time.sleep(1)
        st.rerun()

    st.markdown("---")
    st.caption("💡 **100% Free & Self-Hosted** — Zero API costs or cloud subscriptions.")


# --- MAIN HEADER ---
st.markdown('<p class="main-header">🚀 YOUTUBE AI VIDEO FACTORY</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Prompt-to-Video Engine • Kinetic Subtitles • High-CTR Thumbnail • Full YouTube SEO Kit • $0 Cost</p>', unsafe_allow_html=True)

tab_create, tab_creator_kit, tab_gallery = st.tabs(["✨ Create New Video", "🔥 YouTube Creator Kit", "📁 Video Archive"])


# ==========================================
# TAB 1: CREATE NEW VIDEO
# ==========================================
with tab_create:
    col_input, col_preset = st.columns([2.5, 1.3])

    with col_input:
        topic_input = st.text_input(
            "Enter ANY Prompt, Question, or Topic:",
            placeholder="e.g. What if dinosaurs never went extinct?",
            value=""
        )

    with col_preset:
        st.write("🔥 **Reference Viral Masterpieces:**")
        p1 = st.button("🧬 Can 2 People Restart Humanity? (Awaken)")
        p2 = st.button("🌍 Only Man Left on Earth (IMAGINE)")
        p3 = st.button("🏫 Locked in School 30 Days (Suddenly You)")
        p4 = st.button("🛋️ Story of a Lazy Man (Viral Fable)")
        p5 = st.button("⚡ Reaction Time 10x Faster")
        p6 = st.button("☀️ Sun Disappears 7 Days")

        if p1:
            st.session_state["topic"] = "Can 2 People Really Restart Humanity?"
        elif p2:
            st.session_state["topic"] = "What If You Were the Only Man Left on Earth"
        elif p3:
            st.session_state["topic"] = "What If You Were Locked in School for 30 Days With Your Crush?"
        elif p4:
            st.session_state["topic"] = "Story of a Lazy Man"
        elif p5:
            st.session_state["topic"] = "What If Your Reaction Time Was 10x Faster?"
        elif p6:
            st.session_state["topic"] = "What if the Sun disappeared for 7 days?"

    if "topic" in st.session_state and st.session_state["topic"]:
        topic_input = st.session_state["topic"]

    # Buttons
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        plan_script_btn = st.button("📝 Plan Script & SEO", use_container_width=True)
    with col_btn2:
        render_package_btn = st.button("🎬 Generate Full YouTube Package (Video + Thumbnail + SEO)", use_container_width=True)

    # 1. PLAN SCRIPT ONLY
    if plan_script_btn and topic_input:
        with st.spinner("AI Director writing retention script and YouTube SEO metadata..."):
            director = AIDirector(api_key=api_key_input)
            blueprint = director.generate_full_package(
                topic=topic_input,
                lang=lang,
                duration_mode=duration_str,
                aspect_ratio=aspect_ratio
            )
            st.session_state["current_blueprint"] = blueprint
            st.success(f"Blueprint ready: '{blueprint.get('title')}' ({len(blueprint.get('scenes', []))} scenes) via {blueprint.get('source')}")

    # Display Blueprint Preview
    if "current_blueprint" in st.session_state:
        bp = st.session_state["current_blueprint"]
        scenes = bp.get("scenes", [])
        yt_kit = bp.get("youtube_kit", {})

        st.markdown(f"### 📋 Video Blueprint: *{bp.get('title')}*")
        st.caption(f"Scenes: **{len(scenes)}** • Format: **{aspect_choice}** • Engine: **{bp.get('source')}**")

        # Viral Titles Preview
        if yt_kit.get("viral_titles"):
            st.markdown("🎯 **Suggested High-CTR Titles:**")
            for vt in yt_kit["viral_titles"]:
                st.code(vt, language="markdown")

        with st.expander("🔍 View Scene-by-Scene Script & Emotions", expanded=False):
            for s in scenes:
                st.markdown(f"""
                <div class="scene-card">
                    <b>Scene {s['scene_id']} [{s.get('beat', '').upper()}]</b> • Pose: <i>{s.get('char_pose')}</i> • Expression: <i>{s.get('expression')}</i> • SFX: <code>{s.get('sfx', 'none')}</code><br>
                    <p style="margin-top: 6px; font-size: 1.05rem;">"{s.get('narration')}"</p>
                </div>
                """, unsafe_allow_html=True)

        if st.button("🚀 Render This Blueprint Now", use_container_width=True):
            render_package_btn = True

    # 2. EXECUTE FULL RENDERING PIPELINE
    if render_package_btn:
        active_topic = topic_input or "What if dinosaurs never went extinct?"

        # 1. Ensure assets
        sfx_gen = SFXGenerator(sfx_dir="assets/sfx")
        sfx_gen.ensure_sfx()

        # 2. Get Blueprint
        if (
            "current_blueprint" in st.session_state
            and st.session_state["current_blueprint"].get("topic") == active_topic
            and st.session_state["current_blueprint"].get("language") == lang
        ):
            blueprint = st.session_state["current_blueprint"]
        else:
            director = AIDirector(api_key=api_key_input)
            blueprint = director.generate_full_package(
                topic=active_topic,
                lang=lang,
                duration_mode=duration_str,
                aspect_ratio=aspect_ratio
            )
            st.session_state["current_blueprint"] = blueprint

        scenes = blueprint.get("scenes", [])
        yt_kit = blueprint.get("youtube_kit", {})
        slug = slugify(active_topic)

        status_box = st.status(f"🎥 Producing Complete YouTube Package: '{active_topic}'...", expanded=True)
        progress_bar = st.progress(0.0)
        start_time = time.time()

        if use_aitrends:
            status_box.write("🌟 **[AITrends 2D Studio]** Scripting, synthesizing voice, vector canvas & -14 LUFS DSP mastering...")
            progress_bar.progress(0.2)
            res = generate_viral_video_aitrends(
                topic=active_topic,
                lang=lang,
                duration_mode=duration_str,
                aspect_ratio=aspect_ratio,
                style=style_choice,
                scale=1.0,
                gemini_api_key=api_key_input
            )
            final_video_path = res["video_path"]
            thumb_path = res["thumbnail_path"]
            thumb_filename = os.path.basename(thumb_path)
            final_filename = os.path.basename(final_video_path)
            yt_kit = res["blueprint"].get("youtube_kit", {})
            st.session_state["last_thumbnail"] = thumb_path
            st.session_state["last_video"] = final_video_path
            st.session_state["last_kit"] = yt_kit
            st.session_state["last_project_dir"] = res.get("project_dir")
            st.session_state["last_scene_images"] = res.get("scene_images", [])
        else:
            # Step A: Generate High-CTR Thumbnail
            status_box.write("🖼️ Generating High-CTR Viral Thumbnail (1280x720)...")
            thumb_gen = ThumbnailGenerator(width=1280, height=720)
            thumb_filename = f"{slug}_{lang}_thumbnail.jpg"
            thumb_path = os.path.join("output_videos", thumb_filename)
            thumb_gen.generate_thumbnail(
                hook_text=yt_kit.get("thumbnail_hook", "SACH DEKHO?!"),
                bg_style=scenes[0].get("bg_style", "dusk_space") if scenes else "dusk_space",
                prop_type=yt_kit.get("thumbnail_prop", "question_mark"),
                char_pose="panicking",
                char_expression="screaming",
                output_path=thumb_path
            )
            st.session_state["last_thumbnail"] = thumb_path

            # Step B: Render Scene Chunks
            renderer = ChunkRenderer(width=width, height=height, fps=24, temp_dir="temp")
            chunk_paths = []

            for idx, scene in enumerate(scenes, start=1):
                status_box.write(f"⚙️ **[Scene {idx}/{len(scenes)}]** Synthesizing voice, animated stick figure & subtitles...")
                chunk_file = renderer.render_scene_chunk(scene, scene_idx=idx, lang=lang)
                chunk_paths.append(chunk_file)
                progress_bar.progress(idx / (len(scenes) + 1))

            # Step C: Final Assembly
            status_box.write("🎞️ Lossless concatenation via FFmpeg demuxer...")
            compiler = VideoCompiler(output_dir="output_videos")
            final_filename = f"{slug}_{lang}.mp4"
            final_video_path = compiler.concatenate_chunks(chunk_paths, output_filename=final_filename)

            # Step D: Save YouTube Metadata Kit JSON
            kit_filename = f"{slug}_{lang}_youtube_kit.json"
            kit_path = os.path.join("output_videos", kit_filename)
            with open(kit_path, "w", encoding="utf-8") as f:
                json.dump({
                    "topic": active_topic,
                    "title": blueprint.get("title"),
                    "language": lang,
                    "aspect_ratio": aspect_ratio,
                    "youtube_kit": yt_kit,
                    "video_file": final_filename,
                    "thumbnail_file": thumb_filename
                }, f, indent=2, ensure_ascii=False)

            st.session_state["last_video"] = final_video_path
            st.session_state["last_kit"] = yt_kit

        elapsed = round(time.time() - start_time, 1)
        progress_bar.progress(1.0)
        status_box.update(label=f"🎉 Full YouTube Package Complete in {elapsed}s!", state="complete", expanded=False)

        st.balloons()
        proj_dir_msg = f" • Project Folder: `{st.session_state.get('last_project_dir')}`" if st.session_state.get('last_project_dir') else ""
        st.success(f"Video saved to `{final_video_path}` • Thumbnail saved to `{thumb_path}`{proj_dir_msg}")

        # Dedicated Project Folder Link & Scene Illustrations
        if st.session_state.get("last_project_dir"):
            st.info(f"📁 **Dedicated Project Folder:** `{st.session_state.get('last_project_dir')}`\n\nContains: `prompt.json`, `script.json`, `images/`, `audio/`, `final_video.mp4`, and `youtube_package.json`.")

        scene_imgs = st.session_state.get("last_scene_images") or []
        if scene_imgs:
            with st.expander("🎨 Generated Scene Illustrations (Pollinations AI)", expanded=True):
                img_cols = st.columns(min(len(scene_imgs), 6))
                for c_idx, (col, img_p) in enumerate(zip(img_cols, scene_imgs), start=1):
                    with col:
                        st.image(img_p, caption=f"Scene {c_idx}", use_container_width=True)

        # Post-Generation Preview
        col_res1, col_res2 = st.columns([2.5, 1.5])
        with col_res1:
            st.markdown("### 🎬 Rendered Video")
            st.video(final_video_path)
            with open(final_video_path, "rb") as f:
                st.download_button("⬇️ Download MP4 Video", data=f.read(), file_name=final_filename, mime="video/mp4", use_container_width=True)

        with col_res2:
            st.markdown("### 🖼️ Viral Thumbnail")
            st.image(thumb_path, use_container_width=True)
            with open(thumb_path, "rb") as f:
                st.download_button("⬇️ Download Thumbnail (.jpg)", data=f.read(), file_name=thumb_filename, mime="image/jpeg", use_container_width=True)


# ==========================================
# TAB 2: YOUTUBE CREATOR KIT (COPY-PASTE HUB)
# ==========================================
with tab_creator_kit:
    st.markdown("### 🚀 YouTube Upload Assistant (1-Click Copy)")
    st.write("Here is your ready-to-publish viral package optimized for YouTube algorithm & rapid monetization:")

    active_kit = st.session_state.get("last_kit") or (st.session_state.get("current_blueprint", {}).get("youtube_kit"))

    if not active_kit:
        st.info("No video generated yet. Generate a video in the 'Create New Video' tab to see your custom YouTube Kit!")
    else:
        # 1. TITLES
        st.markdown("#### 🎯 1. High-CTR Titles (Pick One)")
        titles = active_kit.get("viral_titles", [])
        for t in titles:
            st.code(t, language="markdown")

        # 2. DESCRIPTION
        st.markdown("#### 📝 2. SEO-Optimized Description")
        desc = active_kit.get("seo_description", "")
        hashtags = " ".join(active_kit.get("hashtags", []))
        full_desc = f"{desc}\n\n{hashtags}"
        st.text_area("YouTube Description:", value=full_desc, height=140)

        # 3. TAGS
        st.markdown("#### 🏷️ 3. Ranking Tags (Paste in YouTube Studio)")
        tags_list = active_kit.get("tags", [])
        tags_str = ", ".join(tags_list)
        st.code(tags_str, language="markdown")

        # 4. PINNED COMMENT
        st.markdown("#### 💬 4. Pinned Engagement Comment")
        default_pin = "What do you think about this? Let us know in the comments below! 👇" if lang == "en" else "Aapki is baare me kya raye hai? Comment karke batayein! 👇"
        pin_cmt = active_kit.get("pinned_comment") or default_pin
        st.code(pin_cmt, language="markdown")


# ==========================================
# TAB 3: VIDEO ARCHIVE & STORAGE MANAGER
# ==========================================
with tab_gallery:
    st.markdown("### 🗄️ Video Archive & Cascading Storage Manager")
    storage_mgr = StorageManager()
    videos = get_available_videos()

    if not videos:
        st.info("No videos in archive yet.")
    else:
        selected_vid = st.selectbox("Select Video to Inspect or Delete:", videos)
        if selected_vid:
            vpath = os.path.join("output_videos", selected_vid)
            breakdown = storage_mgr.get_video_storage_breakdown(selected_vid)

            col_g1, col_g2 = st.columns([2.3, 1.7])

            with col_g1:
                st.video(vpath)

            with col_g2:
                st.markdown(f"#### 📦 Storage Footprint: **`{breakdown['total_mb']} MB`**")

                # List all cascading assets
                st.markdown("**Associated Files & Project Cache:**")
                for item in breakdown["items"]:
                    icon = "🎬" if item["type"] == "video" else ("🖼️" if item["type"] == "thumbnail" else ("📋" if item["type"] == "youtube_kit" else "📁"))
                    st.markdown(f"- {icon} `{item['name']}` ({item['size_mb']} MB)")

                # Matching thumbnail preview
                thumb_match = next((item["path"] for item in breakdown["items"] if item["type"] == "thumbnail"), None)
                if thumb_match and os.path.exists(thumb_match):
                    st.image(str(thumb_match), caption="Matching Thumbnail", use_container_width=True)

                col_dl, col_del = st.columns([1, 1])
                with col_dl:
                    with open(vpath, "rb") as vf:
                        st.download_button(
                            label="⬇️ Download",
                            data=vf.read(),
                            file_name=selected_vid,
                            mime="video/mp4",
                            use_container_width=True
                        )

                with col_del:
                    delete_clicked = st.button("🗑️ Delete Video", use_container_width=True)

                if delete_clicked:
                    st.session_state[f"confirm_delete_{selected_vid}"] = True

                if st.session_state.get(f"confirm_delete_{selected_vid}", False):
                    st.error(f"⚠️ Confirm: Permanently delete **{selected_vid}** and ALL {len(breakdown['items'])} related assets ({breakdown['total_mb']} MB)?")
                    col_yes, col_no = st.columns([1, 1])
                    with col_yes:
                        if st.button("🔴 Confirm Delete", use_container_width=True):
                            success, freed_mb, logs = storage_mgr.delete_video_cascading(selected_vid)
                            if success:
                                st.success(f"✅ Deleted {selected_vid} and all related files! Freed {freed_mb} MB.")
                            else:
                                st.warning(f"Deletion notes: {', '.join(logs)}")
                            st.session_state.pop(f"confirm_delete_{selected_vid}", None)
                            time.sleep(1.2)
                            st.rerun()
                    with col_no:
                        if st.button("Cancel", use_container_width=True):
                            st.session_state.pop(f"confirm_delete_{selected_vid}", None)
                            st.rerun()

        st.markdown("---")
        st.markdown("#### 🧹 Global System Scratch Cache Cleanup")
        col_c1, col_c2 = st.columns([3, 1.2])
        with col_c1:
            st.caption("Cleans leftover scene chunks (`temp/chunks`), scratch debug frames, and loose temporary test audio without touching finished videos.")
        with col_c2:
            if st.button("🧹 Purge Scratch Cache", use_container_width=True):
                count, freed, _ = storage_mgr.purge_temp_cache()
                st.success(f"Freed {freed} MB of scratch cache!")
                time.sleep(1.2)
                st.rerun()

