# commands/system/close_any.py

import os
import difflib
import traceback
import subprocess
import getpass
import re

from core.registry import register_command
from voice.tts import speak

USERNAME = getpass.getuser()

# Same app names as open_any.py for consistency
APP_PROCESS_NAMES = {
    "vscode": "Code.exe",
    "pycharm": "pycharm64.exe",
    "notepad++": "notepad++.exe",
    "postman": "Postman.exe",
    "git bash": "git-bash.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
    "chrome": "chrome.exe",
    "firefox": "firefox.exe",
    "edge": "msedge.exe",
    "brave": "brave.exe",
    "spotify": "Spotify.exe",
    "vlc": "vlc.exe",
    "photos": "Microsoft.Photos.exe",
    "films and tv": "Video.UI.exe",
    "whatsapp": "WhatsApp.exe",
    "discord": "Discord.exe",
    "telegram": "Telegram.exe",
    "skype": "Skype.exe",
    "steam": "steam.exe",
    "epic games": "EpicGamesLauncher.exe",
    "riot client": "RiotClientServices.exe",
    "battle.net": "Battle.net Launcher.exe",
    "calculator": "Calculator.exe",
    "notepad": "notepad.exe",
    "task manager": "Taskmgr.exe",
    "settings": "SystemSettings.exe",
    "control panel": "control.exe"
}


def suggest_closest_process(name):
    matches = difflib.get_close_matches(name, APP_PROCESS_NAMES.keys(), n=1, cutoff=0.6)
    return matches[0] if matches else None


@register_command(r"\b(close|terminate|exit|kill|shutdown)\s+(.+)", needs_input=True)
def close_any_app(command: str):
    raw = command.lower().split(maxsplit=1)[1].strip()

    if not raw:
        speak("Please tell me what you'd like me to close.")
        return

    raw = re.sub(r"\b(and|then|also|with|comma)\b", ",", raw)
    raw = raw.replace("  ", " ")
    parts = re.split(r",|\band\b|\s+", raw)
    parts = [p.strip() for p in parts if p.strip()]

    closed = []

    for name in parts:
        if name in APP_PROCESS_NAMES:
            process_name = APP_PROCESS_NAMES[name]
        else:
            suggestion = suggest_closest_process(name)
            if suggestion:
                speak(f"{name} not found, did you mean {suggestion}? Closing it.")
                process_name = APP_PROCESS_NAMES[suggestion]
                name = suggestion
            else:
                speak(f"Sorry, I couldn't recognize {name}. Skipping it.")
                continue

        try:
            subprocess.run(f"taskkill /f /im \"{process_name}\"", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            closed.append(name)
        except Exception:
            speak(f"Error while closing {name}")
            print(f"❌ Error closing {name}:\n{traceback.format_exc()}")

    if closed:
        speak("Closed " + ", ".join(closed))
    else:
        speak("Sorry, nothing could be closed.")
