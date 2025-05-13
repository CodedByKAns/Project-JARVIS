# commands/system/open_any.py

import os
import subprocess
import traceback
import difflib
import webbrowser
import getpass
import re

from core.registry import register_command
from voice.tts import speak

# ✅ Username for dynamic paths
USERNAME = getpass.getuser()

# ✅ App Paths
APP_PATHS = {
    # 🔧 Developer Tools
    "vscode": fr"C:\Users\{USERNAME}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "pycharm": r"C:\Program Files\JetBrains\PyCharm Community Edition 2023.2.1\bin\pycharm64.exe",
    "notepad++": r"C:\Program Files\Notepad++\notepad++.exe",
    "postman": fr"C:\Users\{USERNAME}\AppData\Local\Programs\Postman\Postman.exe",
    "git bash": r"C:\Program Files\Git\git-bash.exe",
    "cmd": "cmd",
    "powershell": "powershell",

    # 🌐 Browsers
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",

    # 🎵 Media Players
    "spotify": fr"C:\Users\{USERNAME}\AppData\Roaming\Spotify\Spotify.exe",
    "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    "photos": "start ms-photos:",
    "films and tv": "start ms-filmstv:",

    # 📞 Communication
    "whatsapp": fr"C:\Users\{USERNAME}\AppData\Local\WhatsApp\WhatsApp.exe",
    "discord": fr"C:\Users\{USERNAME}\AppData\Local\Discord\Update.exe --processStart Discord.exe",
    "telegram": fr"C:\Users\{USERNAME}\AppData\Roaming\Telegram Desktop\Telegram.exe",
    "skype": r"C:\Program Files (x86)\Microsoft\Skype for Desktop\Skype.exe",

    # 🎮 Gaming
    "steam": r"C:\Program Files (x86)\Steam\steam.exe",
    "epic games": r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe",
    "riot client": r"C:\Riot Games\Riot Client\RiotClientServices.exe",
    "battle.net": r"C:\Program Files (x86)\Battle.net\Battle.net Launcher.exe",

    # ⚙️ System Utilities
    "calculator": "calc",
    "notepad": "notepad",
    "task manager": "taskmgr",
    "settings": "start ms-settings:",
    "control panel": "control"
}

# ✅ Website Shortcuts
WEB_URLS = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "stackoverflow": "https://stackoverflow.com",
    "chatgpt": "https://chat.openai.com",
    "gmail": "https://mail.google.com",
    "linkedin": "https://www.linkedin.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://twitter.com",
    "medium": "https://medium.com/",
    "trello": "https://trello.com/",
    "canva": "https://www.canva.com/",
    "hackerrank": "https://www.hackerrank.com/",
    "khanacademy": "https://www.khanacademy.org/",
    "unsplash": "https://unsplash.com/",
    "cohere": "https://cohere.ai/",
    "zapier": "https://zapier.com/",
    "w3schools": "https://www.w3schools.com/",
    "mdn_web_docs": "https://developer.mozilla.org/",
    "freecodecamp": "https://www.freecodecamp.org/",
    "coursera": "https://www.coursera.org/",
    "edx": "https://www.edx.org/",
    "udemy": "https://www.udemy.com/",
    "googlescholar": "https://scholar.google.com/",
    "quora": "https://www.quora.com/",
    "notion": "https://www.notion.so/",
    "jotform": "https://www.jotform.com/",
    "dropbox": "https://www.dropbox.com/",
    "googledrive": "https://drive.google.com/",
    "onedrive": "https://onedrive.live.com/",
    "evernote": "https://www.evernote.com/",
    "claude": "https://claude.ai/",
    "duolingo": "https://www.duolingo.com/",
    "kaggle": "https://www.kaggle.com/",
    "grok": "https://grok.com/",
    "asana": "https://asana.com/",
    "slack": "https://slack.com/",
    "figma": "https://www.figma.com/",
    "vs_code": "https://code.visualstudio.com/",
    "sublime_text": "https://www.sublimetext.com/",
    "pypi": "https://pypi.org/",
    "npm": "https://www.npmjs.com/",
    "bootstrap": "https://getbootstrap.com/",
    "font_awesome": "https://fontawesome.com/",
    "gitlab": "https://about.gitlab.com/",
    "docker": "https://www.docker.com/",
    "jenkins": "https://www.jenkins.io/",
    "digitalocean": "https://www.digitalocean.com/",
    "linode": "https://www.linode.com/",
    "aws": "https://aws.amazon.com/",
    "heroku": "https://www.heroku.com/",
    "vercel": "https://vercel.com/",
    "netlify": "https://www.netlify.com/",
    "cloudflare": "https://www.cloudflare.com/",
    "twitch": "https://www.twitch.tv/",
    "pinterest": "https://www.pinterest.com/",
    "reddit": "https://www.reddit.com/",
    "hootsuite": "https://hootsuite.com/",
    "mailchimp": "https://mailchimp.com/",
    "flipkart": "https://flipkart.com/",
    "amazon": "https://amazon.com/",
    "sendgrid": "https://sendgrid.com/"
}



def suggest_closest_app(name):
    all_keys = list(APP_PATHS.keys()) + list(WEB_URLS.keys())
    matches = difflib.get_close_matches(name, all_keys, n=1, cutoff=0.6)
    return matches[0] if matches else None


@register_command(r"\b(open|start|launch|run)\s+(.+)", needs_input=True)
def open_any_app(command: str):
    raw = command.lower().split(maxsplit=1)[1].strip()

    if not raw:
        speak("Please tell me what you'd like me to open.")
        return

    # 🧹 Clean command and split apps
    raw = re.sub(r"\b(and|then|also|with|comma)\b", ",", raw)
    raw = raw.replace("  ", " ")
    parts = re.split(r",|\band\b|\s+", raw)
    parts = [p.strip() for p in parts if p.strip()]

    opened = []

    for name in parts:
        if name in APP_PATHS:
            try:
                subprocess.Popen(APP_PATHS[name], shell=True)
                opened.append(name)
            except Exception:
                speak(f"Error while opening {name}")
                print(f"❌ Error opening {name}:\n{traceback.format_exc()}")

        elif name in WEB_URLS:
            try:
                webbrowser.open(WEB_URLS[name])
                opened.append(name)
            except Exception:
                speak(f"Couldn't open website {name}")
                print(f"❌ Error opening website {name}")

        else:
            suggestion = suggest_closest_app(name)
            if suggestion:
                speak(f"{name} not found, did you mean {suggestion}? Opening it.")
                try:
                    if suggestion in APP_PATHS:
                        subprocess.Popen(APP_PATHS[suggestion], shell=True)
                    else:
                        webbrowser.open(WEB_URLS[suggestion])
                    opened.append(suggestion)
                except Exception:
                    speak(f"Couldn't open {suggestion} either.")
                    print(f"❌ Error opening suggestion {suggestion}:\n{traceback.format_exc()}")
            else:
                speak(f"Sorry, I couldn't recognize {name}. Skipping it.")

    if opened:
        speak("Opening " + ", ".join(opened))
    else:
        speak("Sorry, nothing could be opened.")


# command = "open chrome and youtube"
# open_any_app(command)