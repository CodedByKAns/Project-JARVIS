# commands/youtube.py

import re
import webbrowser
import pywhatkit
from core.registry import register_command
from voice.tts import speak

@register_command(r"play on youtube", needs_input=True)
def search_youtube(command: str):
    """🔍 Searches or plays something on YouTube using voice command."""
    topic = re.sub(r"play on youtube", "", command, flags=re.IGNORECASE).strip()

    if topic:
        speak(f"Searching YouTube for {topic}")
        try:
            pywhatkit.playonyt(topic)
        except Exception as e:
            speak("Sorry, something went wrong while searching on YouTube.")
            print(f"❌ Error in pywhatkit.playonyt: {e}")
    else:
        speak("What should I search for on YouTube?")
