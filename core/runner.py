# core/runner.py
import os
import importlib.util
from voice.tts import speak
from voice.stt import listen
from core.registry import match_command
from core.conversation import chat_with_jarvis

def auto_import_commands(commands_dir="commands"):
    for root, dirs, files in os.walk(commands_dir):
        # Skip __pycache__ folders
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                relative_path = os.path.join(root, file).replace("/", ".").replace("\\", ".")
                module_name = relative_path[:-3]  # remove .py
                spec = importlib.util.find_spec(module_name)
                if spec:
                    importlib.import_module(module_name)

# 🚀 Auto-load all command modules
auto_import_commands()

# 🧠 Main Loop
def run_jarvis():
    while True:
        command = listen()
        if not command:
            continue

        func, needs_input = match_command(command.lower())
        if func:
            try:
                result = func(command) if needs_input else func()
                if result == "exit":
                    break
            except TypeError as e:
                print(f"❌ Function argument error: {e}")
                speak("There was an error running that command.")
        else:
            response = chat_with_jarvis(command)
            speak(response)



