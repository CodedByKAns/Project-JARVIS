import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal
from core.key_commander import CommandOverlay
import keyboard

class HotkeyThread(QThread):
    show_overlay = pyqtSignal()

    def run(self):
        keyboard.add_hotkey('ctrl+shift+j', self.show_overlay.emit)
        keyboard.wait()

def ahk_thread():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    overlay = CommandOverlay()
    overlay.hide()

    hotkey_thread = HotkeyThread()
    hotkey_thread.show_overlay.connect(overlay.show)
    hotkey_thread.start()

    print("✅ Ready! Press Ctrl + Shift + J to show the JARVIS GUI.")
    sys.exit(app.exec_())