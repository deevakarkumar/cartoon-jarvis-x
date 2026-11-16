"""
Storage & Asset Lifecycle Management for Cartoon-Jarvis
Executes clean, atomic cascading deletions of videos along with all associated:
- High-CTR thumbnails (*_thumbnail.jpg, *_thumb.png)
- YouTube SEO metadata kits (*_youtube_kit.json)
- Intermediate 3D/Canvas project folders (projects/<slug>/build/parts)
- Temporary render chunks, orphan voiceover audio, and scratch debug frames.
"""

import os
import shutil
import logging
import gc
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

logger = logging.getLogger(__name__)


def get_dir_size_mb(path: Path) -> float:
    """Calculate total size of all files in directory in megabytes."""
    if not path or not path.exists():
        return 0.0
    if path.is_file():
        return path.stat().st_size / (1024 * 1024)
    total_bytes = 0
    for root, _, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                total_bytes += os.path.getsize(fp)
            except (OSError, FileNotFoundError):
                pass
    return round(total_bytes / (1024 * 1024), 2)


def get_file_size_mb(path: Path) -> float:
    """Calculate file size in megabytes."""
    if not path or not path.exists() or not path.is_file():
        return 0.0
    try:
        return round(path.stat().st_size / (1024 * 1024), 2)
    except Exception:
        return 0.0


def safe_delete_file(path: Path) -> bool:
    """Safely delete file on Windows with GC and retries."""
    if not path or not path.exists():
        return True
    for attempt in range(3):
        try:
            path.unlink()
            return True
        except PermissionError:
            gc.collect()
            time.sleep(0.2)
        except Exception as e:
            logger.warning(f"Error unlinking {path}: {e}")
            break
    return False


def safe_delete_dir(path: Path) -> bool:
    """Safely delete directory tree on Windows with GC and retries."""
    if not path or not path.exists():
        return True
    for attempt in range(3):
        try:
            shutil.rmtree(path)
            return True
        except PermissionError:
            gc.collect()
            time.sleep(0.25)
        except Exception as e:
            logger.warning(f"Error removing tree {path}: {e}")
            break
    return False


class StorageManager:
    def __init__(self, workspace_root: Optional[str] = None):
        if workspace_root:
            self.root = Path(workspace_root)
        else:
            # e:\agent x
            self.root = Path(__file__).resolve().parent.parent.parent

        self.output_dir = self.root / "output_videos"
        self.temp_dir = self.root / "temp"
        self.projects_dir = self.root / "studio" / "renderer" / "aitrends_kit" / "projects"
        self.debug_frames_dir = self.output_dir / "debug_frames"

    def get_storage_summary(self) -> Dict[str, Any]:
        """Returns comprehensive storage metrics across the system."""
        output_mb = get_dir_size_mb(self.output_dir)
        temp_mb = get_dir_size_mb(self.temp_dir)
        projects_mb = get_dir_size_mb(self.projects_dir)
        total_mb = round(output_mb + temp_mb + projects_mb, 2)

        # Free space on host drive
        disk_free_gb = 0.0
        try:
            total, used, free = shutil.disk_usage(str(self.root))
            disk_free_gb = round(free / (1024 * 1024 * 1024), 1)
        except Exception:
            pass

        videos = list(self.output_dir.glob("*.mp4")) if self.output_dir.exists() else []

        return {
            "output_size_mb": output_mb,
            "temp_size_mb": temp_mb,
            "projects_size_mb": projects_mb,
            "total_system_mb": total_mb,
            "disk_free_gb": disk_free_gb,
            "video_count": len(videos)
        }

    def _get_candidate_stems(self, video_name: str) -> List[str]:
        """Derive possible matching stems for related assets."""
        stem = Path(video_name).stem
        stems = [stem]

        # e.g. can_2_people_really_restart_humanity_hi_aitrends -> can_2_people_really_restart_humanity_hi
        if stem.endswith("_aitrends"):
            stems.append(stem[:-9])

        # e.g. can_2_people_really_restart_humanity_hi -> can_2_people_really_restart_humanity
        for s in list(stems):
            for suffix in ["_hi", "_en"]:
                if s.endswith(suffix):
                    stems.append(s[:-len(suffix)])

        # Deduplicate preserving order
        seen = set()
        res = []
        for s in stems:
            if s and s not in seen:
                seen.add(s)
                res.append(s)
        return res

    def get_video_storage_breakdown(self, video_name: str) -> Dict[str, Any]:
        """
        Calculates exact cascading storage breakdown for a video:
        - The .mp4 file
        - Associated thumbnail (.jpg/.png)
        - Associated YouTube kit (.json)
        - Associated aitrends project build directory
        """
        video_path = self.output_dir / video_name if not Path(video_name).is_absolute() else Path(video_name)
        if not video_path.exists():
            return {
                "exists": False,
                "video_name": video_name,
                "total_mb": 0.0,
                "items": []
            }

        video_size = get_file_size_mb(video_path)
        candidate_stems = self._get_candidate_stems(video_path.name)

        # Other videos to avoid deleting shared assets
        other_videos = [v.name for v in self.output_dir.glob("*.mp4") if v.name != video_path.name]
        other_stems = set()
        for ov in other_videos:
            for s in self._get_candidate_stems(ov):
                other_stems.add(s)

        related_files = []
        total_mb = video_size

        related_files.append({
            "type": "video",
            "name": video_path.name,
            "path": video_path,
            "size_mb": video_size,
            "is_dir": False
        })

        # 1. Thumbnails in output_videos
        if self.output_dir.exists():
            for f in self.output_dir.iterdir():
                if f.is_file() and (f.suffix.lower() in [".jpg", ".jpeg", ".png"]):
                    fstem = f.stem.lower()
                    if "thumb" in fstem:
                        for c in candidate_stems:
                            if fstem.startswith(c.lower()):
                                # Check if uniquely belonging to this video
                                is_shared = False
                                for os_stem in other_stems:
                                    if fstem.startswith(os_stem.lower()) and c != candidate_stems[0]:
                                        is_shared = True
                                        break
                                if not is_shared:
                                    smb = get_file_size_mb(f)
                                    total_mb += smb
                                    related_files.append({
                                        "type": "thumbnail",
                                        "name": f.name,
                                        "path": f,
                                        "size_mb": smb,
                                        "is_dir": False
                                    })
                                break

        # 2. YouTube SEO Kits in output_videos
        if self.output_dir.exists():
            for f in self.output_dir.iterdir():
                if f.is_file() and f.suffix.lower() == ".json":
                    fstem = f.stem.lower()
                    if "kit" in fstem or "meta" in fstem or "youtube" in fstem:
                        for c in candidate_stems:
                            if fstem.startswith(c.lower()):
                                is_shared = False
                                for os_stem in other_stems:
                                    if fstem.startswith(os_stem.lower()) and c != candidate_stems[0]:
                                        is_shared = True
                                        break
                                if not is_shared:
                                    smb = get_file_size_mb(f)
                                    total_mb += smb
                                    related_files.append({
                                        "type": "youtube_kit",
                                        "name": f.name,
                                        "path": f,
                                        "size_mb": smb,
                                        "is_dir": False
                                    })
                                break

        # 3. Associated aitrends project build folders
        if self.projects_dir.exists():
            aitrends_videos = [v for v in other_videos if v.endswith("_aitrends.mp4")]
            for p in self.projects_dir.iterdir():
                if p.is_dir():
                    p_name = p.name.lower()
                    for c in candidate_stems:
                        c_clean = c.lower().replace("_aitrends", "")
                        # Project names might be truncated to 35 chars
                        if p_name in c_clean or c_clean.startswith(p_name[:25]):
                            # Check if another aitrends video still needs this project
                            is_shared = any(p_name in ov.lower() for ov in aitrends_videos)
                            if not is_shared or video_path.name.endswith("_aitrends.mp4"):
                                p_mb = get_dir_size_mb(p)
                                total_mb += p_mb
                                related_files.append({
                                    "type": "project_build",
                                    "name": p.name,
                                    "path": p,
                                    "size_mb": p_mb,
                                    "is_dir": True
                                })
                            break

        return {
            "exists": True,
            "video_name": video_path.name,
            "total_mb": round(total_mb, 2),
            "items": related_files
        }

    def delete_video_cascading(self, video_name: str) -> Tuple[bool, float, List[str]]:
        """
        Permanently deletes a video and all related assets (thumbnails, kits, project build cache).
        Returns: (success: bool, total_freed_mb: float, list_of_deleted_descriptions: list[str])
        """
        breakdown = self.get_video_storage_breakdown(video_name)
        if not breakdown["exists"]:
            return False, 0.0, [f"Video '{video_name}' does not exist."]

        freed_mb = breakdown["total_mb"]
        deleted_descriptions = []
        overall_success = True

        for item in breakdown["items"]:
            path = item["path"]
            item_type = item["type"]
            item_size = item["size_mb"]

            if item["is_dir"]:
                success = safe_delete_dir(path)
                if success:
                    deleted_descriptions.append(f"📁 Deleted {item_type}: {item['name']} ({item_size:.1f} MB)")
                else:
                    deleted_descriptions.append(f"⚠️ Could not delete directory: {item['name']}")
                    overall_success = False
            else:
                success = safe_delete_file(path)
                if success:
                    deleted_descriptions.append(f"📄 Deleted {item_type}: {item['name']} ({item_size:.1f} MB)")
                else:
                    deleted_descriptions.append(f"⚠️ Could not delete file: {item['name']}")
                    overall_success = False

        return overall_success, freed_mb, deleted_descriptions

    def purge_temp_cache(self, include_chunks: bool = True) -> Tuple[int, float, List[str]]:
        """
        Purges temporary scratch files:
        - debug_frames in output_videos
        - intermediate chunks in temp/chunks
        - loose test mp3/jpg in temp/
        Does NOT touch finalized videos or active assets.
        """
        deleted_items = []
        initial_summary = self.get_storage_summary()
        initial_temp = initial_summary["temp_size_mb"]

        purged_count = 0

        # 1. Clean debug frames
        if self.debug_frames_dir.exists():
            for f in self.debug_frames_dir.iterdir():
                if f.is_file():
                    if safe_delete_file(f):
                        purged_count += 1
            deleted_items.append("Cleaned output_videos/debug_frames/")

        # 2. Clean temp chunks
        chunks_dir = self.temp_dir / "chunks"
        if include_chunks and chunks_dir.exists():
            for f in chunks_dir.iterdir():
                if f.is_file():
                    if safe_delete_file(f):
                        purged_count += 1
            deleted_items.append("Cleaned temp/chunks/ intermediate scene clips")

        # 3. Clean loose test images / mp3 in temp
        if self.temp_dir.exists():
            for f in self.temp_dir.iterdir():
                if f.is_file() and f.suffix.lower() in [".jpg", ".png", ".mp3", ".wav", ".txt"]:
                    if safe_delete_file(f):
                        purged_count += 1

        final_summary = self.get_storage_summary()
        freed_mb = max(0.0, round(initial_temp - final_summary["temp_size_mb"], 2))
        return purged_count, freed_mb, deleted_items
