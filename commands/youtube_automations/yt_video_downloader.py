import yt_dlp
import os
import time
import pyautogui
import pyperclip
from core.registry import register_command
from voice.tts import speak

def get_youtube_url():
    """📋 Gets the current YouTube URL from the browser's address bar."""
    pyautogui.hotkey('ctrl', 'l')  # Focus address bar
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'c')  # Copy URL
    time.sleep(0.3)
    return pyperclip.paste().strip()

def download_video(video_url, output_path='downloads/'):
    """📥 Downloads YouTube video in 1080p MP4 format."""
    options = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'ffmpeg_location': r'C:\ffmpeg\bin\ffmpeg.exe',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }

    os.makedirs(output_path, exist_ok=True)

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([video_url])
        speak("✅ Video downloaded successfully.")
    except Exception as e:
        speak("❌ Failed to download the video.")
        print(f"⚠️ Error during download:\n{e}")

@register_command(r"download youtube video", needs_input=False)
def yt_video_downloader():
    """🎬 Copies YouTube URL and downloads the video."""
    speak("Getting the YouTube link from your browser...")
    print("📋 Copying URL from browser...")
    
    url = get_youtube_url()
    print(f"🔗 URL found: {url}")

    if url.startswith("http"):
        speak("Starting the download now.")
        download_video(url)
    else:
        speak("❌ Couldn't get a valid YouTube link.")
        print("❌ Invalid or empty URL.")
