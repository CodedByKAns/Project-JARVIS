import pyautogui
import os
import ctypes
import subprocess
import requests
import winshell
from core.registry import register_command
from voice.tts import speak

@register_command(r"minimize all open windows", needs_input=False)
def minimize_all_windows():
    speak("Minimizing all open windows.")
    pyautogui.hotkey('win', 'd')

@register_command(r"maximize active window", needs_input=False)
def maximize_active_window():
    speak("Maximizing the active window.")
    pyautogui.hotkey('win', 'up')

@register_command(r"minimize active window", needs_input=False)
def minimize_active_window():
    speak("Minimizing the active window.")
    pyautogui.hotkey('win', 'down')

@register_command(r"close activate window", needs_input=False)
def close_active_window():
    speak("Closing the active window.")
    pyautogui.hotkey('alt', 'f4')

@register_command(r"switch window", needs_input=False)
def switch_window():
    speak("Switching to the next window.")
    pyautogui.hotkey('alt', 'tab')

@register_command(r"shutdown pc", needs_input=False)
def shutdown_system():
    speak("Shutting down the system.")
    os.system("shutdown /s /t 1")

@register_command(r"restart pc", needs_input=False)
def restart_system():
    speak("Restarting the system.")
    os.system("shutdown /r /t 1")

@register_command(r"lock pc", needs_input=False)
def lock_system():
    speak("Locking the system.")
    ctypes.windll.user32.LockWorkStation()

@register_command(r"log off", needs_input=False)
def log_off():
    speak("Logging off the current user.")
    os.system("shutdown /l")

@register_command(r"clear temproary files", needs_input=False)
def clean_temp_files():
    speak("Cleaning temporary files.")
    os.system("del /q/f/s %TEMP%\\*")

@register_command(r"enable dark mode", needs_input=False)
def enable_dark_mode():
    speak("Enabling dark mode.")
    subprocess.run(['reg', 'add', r'HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize', '/v', 'AppsUseLightTheme', '/t', 'REG_DWORD', '/d', '0', '/f'])

@register_command(r"disable dark mode", needs_input=False)
def disable_dark_mode():
    speak("Disabling dark mode.")
    subprocess.run(['reg', 'add', r'HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize', '/v', 'AppsUseLightTheme', '/t', 'REG_DWORD', '/d', '1', '/f'])

@register_command(r"empty recyle bin", needs_input=False)
def empty_recycle_bin():
    speak("Emptying the recycle bin.")
    winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)

@register_command(r"ip address", needs_input=False)
def get_public_ip():
    speak("Fetching your public IP address.")
    ip = requests.get("https://api.ipify.org").text
    print(f"Your public IP address is: {ip}")
    speak(f"Your public IP address is: {ip}")
    return ip

