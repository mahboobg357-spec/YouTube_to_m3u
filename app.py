import os
import subprocess
from flask import Flask, Response

app = Flask(__name__)

# یہاں اپنی پلے لسٹ کا اصل لنک ڈالیں
PLAYLIST_URL = "https://www.youtube.com/watch?v=bQLHMy0SAWc&list=PLinVjP-aRmltrRFT9zRn1hmsu0TM8HDDx&pp=0gcJCf4COCosWNin"

@app.route("/")
def index():
    return "<h1>Live 24/7 TV Stream Server is Running!</h1><p>Stream Link: /live.m3u8</p>"

@app.route("/live.m3u8")
def live_stream():
    cmd = [
        "yt-dlp",
        "-f", "best[ext=mp4]/best",
        "-g",
        "--flat-playlist",
        PLAYLIST_URL
    ]
    
    def generate():
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
        for url in process.stdout:
            url = url.strip()
            if url:
                stream_proc = subprocess.Popen(
                    ["ffmpeg", "-re", "-i", url, "-c", "copy", "-f", "mpegts", "pipe:1"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL
                )
                while True:
                    data = stream_proc.stdout.read(1024 * 64)
                    if not data:
                        break
                    yield data

    return Response(generate(), mimetype="video/mp2t")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
