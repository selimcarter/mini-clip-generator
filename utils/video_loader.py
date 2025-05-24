import yt_dlp
import uuid

def download_video(url):
    output_path = f"video_{uuid.uuid4().hex}.mp4"
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': output_path,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path