import yt_dlp
import os
from utils.convert import convert_to_mp3

def download(url):
    output_path = "/tmp/youtube_audio.%(ext)s"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    mp3_path = output_path.replace(".%(ext)s", ".mp3")
    return mp3_path, os.path.basename(mp3_path)

def download_video(url):
    output_path = "/tmp/youtube_video.%(ext)s"
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Encontrar el archivo descargado
    ext_list = ['.mp4', '.mkv', '.webm']
    for ext in ext_list:
        possible_path = output_path.replace(".%(ext)s", ext)
        if os.path.exists(possible_path):
            return possible_path, os.path.basename(possible_path)

    raise Exception("No se pudo encontrar el archivo descargado")
