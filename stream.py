import json
import os
import subprocess
import time

# نیچے کوٹیشن مارکس کے اندر اپنی 30 سے 40 ویڈیوز والی پلے لسٹ کا لنک پیسٹ کریں
PLAYLIST_URL = "https://www.youtube.com/watch?v=dc5bEPnBZEk&list=PLinVjP-aRmlsfgXN264NXF2BaBslOO_B-"

print("Fetching playlist entries...")
cmd = ["yt-dlp", "--flat-playlist", "-J", PLAYLIST_URL]
res = subprocess.run(cmd, capture_output=True, text=True)

try:
    data = json.loads(res.stdout)
    entries = data.get("entries", [])
except Exception as e:
    print(f"Error parsing JSON: {e}")
    entries = []

m3u_lines = ["#EXTM3U\n"]
media_urls = []

for entry in entries:
    vid_id = entry.get("id")
    title = entry.get("title", "Live Video")
    if not vid_id:
        continue

    video_url = f"https://www.youtube.com/watch?v={vid_id}"
    get_stream = subprocess.run(
        ["yt-dlp", "-g", "-f", "best[ext=mp4]/best", video_url],
        capture_output=True,
        text=True,
    )
    stream_url = get_stream.stdout.strip()

    if stream_url and stream_url.startswith("http"):
        m3u_lines.append(f'#EXTINF:-1 tvg-name="{title}",{title}\n{stream_url}\n')
        media_urls.append(stream_url)

# پوری پلے لسٹ فائل محفوظ کرنا
with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.writelines(m3u_lines)

# سنگل فکسڈ لائیو چینل بنانا
if media_urls:
    total_tracks = len(media_urls)
    current_slot = int(time.time() // 240)
    current_index = current_slot % total_tracks
    active_stream = media_urls[current_index]

    live_hls = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:300
#EXT-X-MEDIA-SEQUENCE:{current_slot}
#EXTINF:240.0,Live Music Channel
{active_stream}
"""
    with open("live_channel.m3u8", "w", encoding="utf-8") as f:
        f.write(live_hls)

print("Files generated successfully!")
