import screen_brightness_control as sbc
import re
import re
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from core.registry import register_command
from voice.tts import speak



@register_command(r"control brightness", needs_input=True)
def brightness_control(command: str):
    try:
        # Percentage extract karo
        percent = int(re.search(r'(\d+)%', command).group(1))

        if "increase" in command.lower():
            current = sbc.get_brightness(display=0)[0]
            new_brightness = min(100, current + percent)
            sbc.set_brightness(new_brightness, display=0)
            speak(f"🔆 Brightness increased to {new_brightness}%")

        elif "decrease" in command.lower():
            current = sbc.get_brightness(display=0)[0]
            new_brightness = max(0, current - percent)
            sbc.set_brightness(new_brightness, display=0)
            speak(f"🌑 Brightness decreased to {new_brightness}%")

        elif "set" in command.lower() or "to" in command.lower():
            sbc.set_brightness(percent, display=0)
            speak(f"📶 Brightness set to {percent}%")

        else:
            print("⚠️ Command not recognized. Use 'increase', 'decrease', or 'set to'.")

    except Exception as e:
        print("❌ Error:", e)


@register_command(r"control volume", needs_input=True)
def volume_control(command: str):
    try:
        # Extract percentage from the command
        percent = int(re.search(r'(\d+)%', command).group(1))

        # Setup volume interface
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        # Get current volume level
        current_volume = volume.GetMasterVolumeLevelScalar() * 100

        if "increase" in command.lower():
            new_volume = min(100, current_volume + percent)
            volume.SetMasterVolumeLevelScalar(new_volume / 100.0, None)
            speak(f"🔊 Volume increased to {int(new_volume)}%")

        elif "decrease" in command.lower():
            new_volume = max(0, current_volume - percent)
            volume.SetMasterVolumeLevelScalar(new_volume / 100.0, None)
            speak(f"🔉 Volume decreased to {int(new_volume)}%")

        elif "set" in command.lower() or "to" in command.lower():
            volume.SetMasterVolumeLevelScalar(percent / 100.0, None)
            speak(f"📢 Volume set to {percent}%")

        else:
            print("⚠️ Command not recognized. Use 'increase', 'decrease', or 'set to'.")

    except Exception as e:
        print("❌ Error:", e)
