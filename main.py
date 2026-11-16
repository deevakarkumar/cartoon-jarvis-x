"""
CARTOON-JARVIS: Automated $0 Zero-Budget YouTube Video Studio
End-to-End Pipeline Entry Point: Prompt -> Video + Thumbnail + YouTube Viral Kit
"""

import argparse
import json
import os
import re
import sys
import time

# Ensure workspace root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from studio.brain.ai_director import AIDirector
from studio.audio.sfx_generator import SFXGenerator
from studio.visual.thumbnail_generator import ThumbnailGenerator
from studio.renderer.chunk_renderer import ChunkRenderer
from studio.renderer.video_compiler import VideoCompiler
from studio.renderer.aitrends_bridge import generate_viral_video_aitrends


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "_", text)[:40]


def run_pipeline(
    topic: str,
    lang: str = "hi",
    duration_mode: str = "1min",
    aspect_ratio: str = "16:9",
    gemini_api_key: str = None,
    engine: str = "studio",
    style: str = "dusk"
):
    if engine.lower() in ["aitrends", "canvas"]:
        return generate_viral_video_aitrends(
            topic=topic,
            lang=lang,
            duration_mode=duration_mode,
            aspect_ratio=aspect_ratio,
            style=style,
            scale=0.5,
            gemini_api_key=gemini_api_key
        )

    is_shorts = (aspect_ratio == "9:16" or "short" in aspect_ratio.lower())
    width = 1080 if is_shorts else 1920
    height = 1920 if is_shorts else 1080

    print("\n" + "=" * 65, flush=True)
    print("🎬 CARTOON-JARVIS: $0 Automated YouTube Video & Shorts Factory", flush=True)
    print("=" * 65, flush=True)
    print(f"📌 Topic: {topic}", flush=True)
    print(f"🌐 Language: {'Hindi (hi)' if lang == 'hi' else 'English (en)'}", flush=True)
    print(f"📐 Format: {'⚡ YouTube Shorts (9:16 - 1080x1920)' if is_shorts else '📺 YouTube Standard (16:9 - 1920x1080)'}", flush=True)
    print(f"⏱️ Target Duration: {duration_mode}", flush=True)
    print("-" * 65, flush=True)

    start_time = time.time()

    # 1. Ensure SFX Assets Exist
    sfx_gen = SFXGenerator(sfx_dir="assets/sfx")
    sfx_gen.ensure_sfx()

    # 2. AI Director: Scriptwriting + YouTube Viral Kit Generation
    print("🧠 Step 1: AI Director crafting retention script & YouTube kit...", flush=True)
    director = AIDirector(api_key=gemini_api_key)
    blueprint = director.generate_full_package(
        topic=topic,
        lang=lang,
        duration_mode=duration_mode,
        aspect_ratio="9:16" if is_shorts else "16:9"
    )

    scenes = blueprint.get("scenes", [])
    youtube_kit = blueprint.get("youtube_kit", {})
    slug = slugify(topic)

    print(f"   [AI Director] Title: '{blueprint.get('title')}' ({len(scenes)} scenes)", flush=True)
    print(f"   [Source Engine]: {blueprint.get('source', 'smart_offline_engine')}", flush=True)

    # 3. Generate YouTube High-CTR Thumbnail
    print("\n🖼️ Step 2: Generating YouTube High-CTR Viral Thumbnail...", flush=True)
    thumb_gen = ThumbnailGenerator(width=1280, height=720)
    thumb_filename = f"{slug}_{lang}_thumbnail.jpg"
    thumb_path = os.path.join("output_videos", thumb_filename)
    
    thumb_gen.generate_thumbnail(
        hook_text=youtube_kit.get("thumbnail_hook", "SACH DEKHO?!"),
        bg_style=scenes[0].get("bg_style", "dusk_space") if scenes else "dusk_space",
        prop_type=youtube_kit.get("thumbnail_prop", "question_mark"),
        char_pose="panicking",
        char_expression="screaming",
        output_path=thumb_path
    )

    # 4. Save YouTube Viral Metadata Kit
    kit_filename = f"{slug}_{lang}_youtube_kit.json"
    kit_path = os.path.join("output_videos", kit_filename)
    with open(kit_path, "w", encoding="utf-8") as f:
        json.dump({
            "topic": topic,
            "title": blueprint.get("title"),
            "language": lang,
            "aspect_ratio": "9:16" if is_shorts else "16:9",
            "youtube_kit": youtube_kit,
            "video_file": f"{slug}_{lang}.mp4",
            "thumbnail_file": thumb_filename
        }, f, indent=2, ensure_ascii=False)
    print(f"  [YouTube Kit] Saved -> {kit_path}", flush=True)

    # 5. Scene-by-Scene Chunk Rendering (Anti-RAM-Crash)
    print(f"\n🎨 Step 3: Rendering Scene Chunks ({width}x{height} @ 24fps)...", flush=True)
    renderer = ChunkRenderer(width=width, height=height, fps=24, temp_dir="temp")
    chunk_paths = []

    for idx, scene in enumerate(scenes, start=1):
        print(f"\n--- [Scene {idx}/{len(scenes)}] ---", flush=True)
        chunk_file = renderer.render_scene_chunk(scene, scene_idx=idx, lang=lang)
        chunk_paths.append(chunk_file)

    # 6. Final Lossless Assembly
    print("\n🎞️ Step 4: Lossless Assembly via FFmpeg Demuxer...", flush=True)
    compiler = VideoCompiler(output_dir="output_videos")
    final_filename = f"{slug}_{lang}.mp4"
    final_video_path = compiler.concatenate_chunks(chunk_paths, output_filename=final_filename)

    elapsed = round(time.time() - start_time, 1)
    file_size_mb = round(os.path.getsize(final_video_path) / (1024 * 1024), 2)

    print("\n" + "=" * 65, flush=True)
    print(f"🎉 SUCCESS! Complete YouTube Package Generated in {elapsed}s", flush=True)
    print(f"🎬 Video File:     {os.path.abspath(final_video_path)} ({file_size_mb} MB)", flush=True)
    print(f"🖼️ Thumbnail:      {os.path.abspath(thumb_path)}", flush=True)
    print(f"📋 YouTube Kit:    {os.path.abspath(kit_path)}", flush=True)
    print(f"🔥 Viral Titles:")
    for vt in youtube_kit.get("viral_titles", []):
        print(f"   • {vt}", flush=True)
    print("=" * 65 + "\n", flush=True)

    return {
        "video_path": final_video_path,
        "thumbnail_path": thumb_path,
        "kit_path": kit_path,
        "blueprint": blueprint
    }


def main():
    parser = argparse.ArgumentParser(description="CARTOON-JARVIS: Automated $0 YouTube Studio")
    parser.add_argument("--topic", type=str, default=None, help="Core question or topic prompt")
    parser.add_argument("--lang", type=str, choices=["hi", "en"], default="hi", help="Language: 'hi' or 'en'")
    parser.add_argument("--duration", type=str, choices=["1min", "5min"], default="1min", help="Duration mode")
    parser.add_argument("--format", type=str, choices=["16:9", "9:16"], default="16:9", help="Aspect ratio: '16:9' or '9:16' (Shorts)")
    parser.add_argument("--engine", type=str, choices=["studio", "aitrends", "pil"], default="studio", help="Engine: 'studio' (Native 1080p + Kinetic Subtitles + Character Rig) or 'aitrends' (HTML Canvas)")
    parser.add_argument("--style", type=str, default="dusk", choices=["dusk", "midnight", "golden", "neon", "storybook"], help="Visual style for aitrends engine")
    parser.add_argument("--api_key", type=str, default=None, help="Optional Gemini API key for dynamic AI scripting")
    parser.add_argument("--delete", type=str, default=None, help="Permanently delete a video and ALL cascading assets (thumbnail, youtube kit, project cache)")
    parser.add_argument("--clean-temp", action="store_true", help="Purge loose temp chunks, orphan debug frames, and scratch files")
    parser.add_argument("--storage", action="store_true", help="Display full storage consumption metrics across the studio")

    args = parser.parse_args()

    # Handle Storage / Cleanup operations
    from studio.storage.storage_manager import StorageManager
    storage_mgr = StorageManager()

    if args.storage:
        summary = storage_mgr.get_storage_summary()
        print("\n" + "=" * 60)
        print("📊 CARTOON-JARVIS: STORAGE CONSUMPTION AUDIT")
        print("=" * 60)
        print(f"🎬 Output Videos:      {summary['output_size_mb']} MB ({summary['video_count']} videos)")
        print(f"📁 AITrends Projects:  {summary['projects_size_mb']} MB")
        print(f"🧹 Temp & Cache:       {summary['temp_size_mb']} MB")
        print(f"💾 Total Studio Usage: {summary['total_system_mb']} MB")
        print(f"💽 Host Disk Free:     {summary['disk_free_gb']} GB")
        print("=" * 60 + "\n")
        return

    if args.clean_temp:
        count, freed_mb, items = storage_mgr.purge_temp_cache(include_chunks=True)
        print(f"\n🧹 Temp Cache Cleaned: Freed {freed_mb} MB ({count} scratch files removed).")
        for item in items:
            print(f"   • {item}")
        print()
        return

    if args.delete:
        target = args.delete.strip()
        # Find exact or best matching video
        target_video = target if target.endswith(".mp4") else f"{target}.mp4"
        breakdown = storage_mgr.get_video_storage_breakdown(target_video)
        if not breakdown["exists"]:
            # Try fuzzy match
            all_vids = [f.name for f in storage_mgr.output_dir.glob("*.mp4")]
            matched = [v for v in all_vids if target.lower() in v.lower()]
            if matched:
                target_video = matched[0]
                breakdown = storage_mgr.get_video_storage_breakdown(target_video)

        if not breakdown["exists"]:
            print(f"\n❌ Error: No video matching '{target}' found in output_videos/.")
            return

        print(f"\n🗑️ Deleting video '{target_video}' and cascading assets...")
        for item in breakdown["items"]:
            print(f"   - {item['type'].upper()}: {item['name']} ({item['size_mb']} MB)")
        print(f"   Total to be freed: {breakdown['total_mb']} MB")

        success, freed_mb, logs = storage_mgr.delete_video_cascading(target_video)
        if success:
            print(f"\n✅ SUCCESS: Deleted '{target_video}'. Freed {freed_mb} MB across all related files!")
        else:
            print(f"\n⚠️ Completed with warnings:")
            for l in logs:
                print(f"   {l}")
        print()
        return

    topic = args.topic or "Can 2 People Really Restart Humanity?"
    run_pipeline(
        topic=topic,
        lang=args.lang,
        duration_mode=args.duration,
        aspect_ratio=args.format,
        gemini_api_key=args.api_key,
        engine=args.engine,
        style=args.style
    )


if __name__ == "__main__":
    main()
