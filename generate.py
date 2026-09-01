import subprocess
import json

# Replace with your playlist URL
PLAYLIST_URL = "https://www.youtube.com/watch?v=bQLHMy0SAWc&list=PLinVjP-aRmltrRFT9zRn1hmsu0TM8HDDx&pp=0gcJCf4COCosWNin"

print("Fetching links...")

cmd = [
    "yt-dlp",
    "--flat-playlist",
    "-J",
    PLAYLIST_URL
]

result = subprocess.check_output(cmd).decode("utf-8")
data = json.loads(result)

m3u_lines = ["#EXTM3U\n"]

for index, entry in enumerate(data.get("entries", []), start=1):
    video_id = entry.get("id")
    title = entry.get("title", f"Video {index}")
    
    try:
        stream_cmd = ["yt-dlp", "-g", "-f", "best", f"https://www.youtube.com/watch?v={video_id}"]
        direct_url = subprocess.check_output(stream_cmd).decode("utf-8").strip()
        
        m3u_lines.append(f'#EXTINF:-1 group-title="YouTube Playlist",{index}. {title}\n')
        m3u_lines.append(f"{direct_url}\n")
    except Exception as e:
        continue

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.writelines(m3u_lines)

print("Playlist ready!")
