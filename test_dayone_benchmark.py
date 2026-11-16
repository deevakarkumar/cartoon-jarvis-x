import os
import sys
import json
import time

# Ensure workspace root is in path
sys.path.insert(0, r"e:\agent x")

from studio.renderer.aitrends_bridge import generate_viral_video_aitrends

print("=== STARTING DAY ONE FILMS BENCHMARK TEST ===")
t0 = time.time()
res = generate_viral_video_aitrends(
    topic="Motivation Will Fail You: Discipline Is Everything",
    lang="hi",
    duration_mode="1min",
    aspect_ratio="16:9",
    style="dayone",
    scale=1.0
)

print("\n=== BENCHMARK TEST COMPLETED SUCCESSFULLY! ===")
print(f"Elapsed: {round(time.time() - t0, 1)}s")
print("Result:")
print(json.dumps({
    "final_video_path": res.get("final_video_path"),
    "project_dir": res.get("project_dir"),
    "total_duration": res.get("total_duration"),
    "num_shots": res.get("num_shots")
}, indent=2))
