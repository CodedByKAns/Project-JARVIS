import speech_recognition as sr
from .tts import speak

# 🎤 Listen until user says "jarvis"
def listen(prompt=None):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        if prompt:
            speak(prompt)

        r.adjust_for_ambient_noise(source, duration=1)

        print("🎧 Continuous listening started... Say 'Jarvis' to activate.")

        while True:
            try:
                print("🎤 Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=8)
                command = r.recognize_google(audio, language='en-IN').lower()
                print(f"🗣️ You said: {command}")

                if "jarvis" in command:
                    parts = command.split("jarvis", 1)
                    after_jarvis = parts[1].strip()

                    if after_jarvis:
                        return after_jarvis  # 🔁 Return what was said *after* "jarvis"
                    else:
                        return ""  # Only "jarvis" was said

                else:
                    print("❌ Wake word not found. Waiting...")
                    # Optional: no speak() to keep it quiet while waiting

            except sr.WaitTimeoutError:
                print("⌛ Timeout. Still listening...")
            except sr.UnknownValueError:
                print("😕 Could not understand. Listening again...")
            except sr.RequestError:
                speak("There was a problem with the speech service.")
                return None
