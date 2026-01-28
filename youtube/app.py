from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form["url"]
    format_choice = request.form["format"]

    filename = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_DIR, f"{filename}.%(ext)s")

    if format_choice == "mp3":
        # 🎵 MP3（一定有聲音）
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "noplaylist": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
        final_file = os.path.join(DOWNLOAD_DIR, f"{filename}.mp3")

    else:
        # 🎬 MP4（強制 AAC 音訊）
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": output_template,
            "noplaylist": True,
            "merge_output_format": "mp4",
            "postprocessor_args": [
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
            ],
        }
        final_file = os.path.join(DOWNLOAD_DIR, f"{filename}.mp4")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download=True)

    return send_file(final_file, as_attachment=True)

if __name__ == "__main__":
    app.run()
