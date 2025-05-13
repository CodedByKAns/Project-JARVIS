import sys
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal
from core.runner import run_jarvis
from core.key_commander import CommandOverlay
import keyboard

class HotkeyThread(QThread):
    show_overlay = pyqtSignal()

    def run(self):
        keyboard.add_hotkey('ctrl+shift+j', self.show_overlay.emit)
        keyboard.wait()

class JarvisThread(QThread):
    def run(self):
        run_jarvis()

def main():
    # Initialize QApplication in the main thread
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Create the CommandOverlay (GUI)
    overlay = CommandOverlay()
    overlay.hide()

    # Set up the hotkey thread to listen for Ctrl+Shift+J
    hotkey_thread = HotkeyThread()
    hotkey_thread.show_overlay.connect(overlay.show)
    hotkey_thread.start()

    # Run run_jarvis in a separate thread
    jarvis_thread = JarvisThread()
    jarvis_thread.start()

    print("✅ Ready! Press Ctrl + Shift + J to show the JARVIS GUI.")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()