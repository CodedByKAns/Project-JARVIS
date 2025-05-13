# tts.py
import os
import sys
import asyncio
import time
import pygame
import edge_tts
import re
import hashlib

from PyQt5.QtWidgets import QApplication
from core.popup import TypingPopup

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

# Ensure single QApplication
app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

VOICE = "hi-IN-MadhurNeural"

async def generate_tts(text, filename):
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate='+25%'
    )
    await communicate.save(filename)

def split_text(text, max_length=250):
    sentences = re.split(r'(?<=[।.!?]) +', text)
    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) < max_length:
            current += sentence + " "
        else:
            chunks.append(current.strip())
            current = sentence + " "
    if current:
        chunks.append(current.strip())
    return chunks

def speak(text):
    chunks = split_text(text)
    popup = TypingPopup(text)
    popup.show()

    # Initialize pygame once
    pygame.mixer.init()

    for i, chunk in enumerate(chunks):
        # Unique filename based on content
        hashname = hashlib.md5(chunk.encode()).hexdigest()
        filename = os.path.join(TEMP_DIR, f"{hashname}.mp3")

        # Remove existing file (precaution)
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                time.sleep(0.1)
                os.remove(filename)

        # Generate and save TTS
        asyncio.run(generate_tts(chunk, filename))

        # Play the audio
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            app.processEvents()
            time.sleep(0.05)

        # Delete after playing
        try:
            os.remove(filename)
        except:
            pass

    pygame.mixer.quit()

