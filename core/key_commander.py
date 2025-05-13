import sys
import os
import importlib.util
import math
from PyQt5.QtWidgets import (QApplication, QLineEdit, QWidget, QVBoxLayout, QPushButton, 
                            QLabel, QHBoxLayout, QProgressBar, QFileDialog, QCompleter)
from PyQt5.QtCore import Qt, QRectF, QPropertyAnimation, pyqtProperty, QEasingCurve, QTimer, QStringListModel
from PyQt5.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QLinearGradient, QFontDatabase

from core.registry import match_command
from core.conversation import chat_with_jarvis
from commands.tools.jarvis_vision import analyze_uploaded_image
from commands.ai.code_helper import coding_assistant

def auto_import_commands(commands_dir="commands"):
    for root, dirs, files in os.walk(commands_dir):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                relative_path = os.path.join(root, file).replace("/", ".").replace("\\", ".")
                module_name = relative_path[:-3]
                spec = importlib.util.find_spec(module_name)
                if spec:
                    importlib.import_module(module_name)

auto_import_commands()

class CommandInput(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.overlay = parent

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            if self.overlay.command_history:
                self.overlay.history_index = max(0, self.overlay.history_index - 1)
                self.setText(self.overlay.command_history[self.overlay.history_index])
        elif event.key() == Qt.Key_Down:
            if self.overlay.command_history and self.overlay.history_index < len(self.overlay.command_history) - 1:
                self.overlay.history_index += 1
                self.setText(self.overlay.command_history[self.overlay.history_index])
            else:
                self.setText("")
        else:
            super().keyPressEvent(event)

class CommandOverlay(QWidget):
    def __init__(self):
        super().__init__(None)
        self._opacity = 0.0
        self._pulse_value = 0
        self.processing = False
        self.uploaded_file = None
        self.file_type = None
        self.code_language = None
        self.is_dragging_over = False
        self.is_dark_theme = True
        self.command_history = []
        self.history_index = 0
        
        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont(":/fonts/Inter-Regular.ttf")
        font_families = font_db.applicationFontFamilies(font_id)
        self.main_font = font_families[0] if font_families else "Arial"

        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_InputMethodEnabled)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)

        screen = QApplication.primaryScreen().geometry()
        w, h = 720, 160
        x = (screen.width() - w) // 2
        y = screen.height() - h - 100
        self.setGeometry(x, y, w, h)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)
        
        top_bar = QHBoxLayout()
        
        self.title_label = QLabel("J.A.R.V.I.S")
        title_font = QFont(self.main_font, 12, QFont.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #FFFFFF;")
        
        self.theme_button = QPushButton("🌙")
        self.theme_button.setFixedSize(28, 28)
        self.theme_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgba(255, 255, 255, 0.7);
                border: none;
                font-size: 16px;
                border-radius: 14px;
            }
            QPushButton:hover {
                background-color: rgba(50, 50, 50, 0.1);
                color: #FFFFFF;
            }
        """)
        self.theme_button.setToolTip("Toggle theme")
        self.theme_button.clicked.connect(self.toggle_theme)
        
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(28, 28)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgba(255, 255, 255, 0.7);
                border: none;
                font-size: 16px;
                font-weight: 600;
                border-radius: 14px;
            }
            QPushButton:hover {
                background-color: rgba(50, 50, 50, 0.1);
                color: #FFFFFF;
            }
        """)
        self.close_button.setToolTip("Close")
        self.close_button.clicked.connect(self.fade_out_and_hide)
        
        top_bar.addWidget(self.title_label)
        top_bar.addStretch()
        top_bar.addWidget(self.theme_button)
        top_bar.addWidget(self.close_button)
        
        main_layout.addLayout(top_bar)
        
        input_layout = QHBoxLayout()
        
        self.upload_button = QPushButton("📁")
        self.upload_button.setFixedSize(28, 28)
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgba(255, 255, 255, 0.7);
                border: none;
                font-size: 16px;
                border-radius: 14px;
            }
            QPushButton:hover {
                background-color: rgba(50, 50, 50, 0.1);
                color: #FFFFFF;
            }
        """)
        self.upload_button.setToolTip("Upload file")
        self.upload_button.clicked.connect(self.select_file)
        
        self.command_icon = QLabel("⌘")
        icon_font = QFont(self.main_font, 16, QFont.Bold)
        self.command_icon.setFont(icon_font)
        self.command_icon.setStyleSheet("color: #CCCCCC; padding-right: 10px;")
        
        self.input = CommandInput(self)
        input_font = QFont(self.main_font, 12)
        self.input.setFont(input_font)
        self.input.setStyleSheet("""
            QLineEdit {
                color: white;
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 14px;
                selection-background-color: rgba(200, 200, 200, 0.3);
            }
            QLineEdit:focus {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid #CCCCCC;
            }
        """)
        self.input.setPlaceholderText("Type a command...")
        self.input.returnPressed.connect(self.handle_command)
        self.input.setFocusPolicy(Qt.StrongFocus)
        
        self.history_model = QStringListModel(self.command_history, self)
        self.completer = QCompleter(self.history_model, self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.input.setCompleter(self.completer)
        
        self.clear_button = QPushButton("🗑️")
        self.clear_button.setFixedSize(28, 28)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgba(255, 255, 255, 0.7);
                border: none;
                font-size: 16px;
                border-radius: 14px;
            }
            QPushButton:hover {
                background-color: rgba(50, 50, 50, 0.1);
                color: #FFFFFF;
            }
        """)
        self.clear_button.setToolTip("Clear input")
        self.clear_button.clicked.connect(self.input.clear)
        
        input_layout.addWidget(self.upload_button)
        input_layout.addWidget(self.command_icon)
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.clear_button)
        
        main_layout.addLayout(input_layout)
        
        status_layout = QHBoxLayout()
        
        self.status_icon = QLabel("•")
        status_icon_font = QFont(self.main_font, 14)
        self.status_icon.setFont(status_icon_font)
        self.status_icon.setStyleSheet("color: #FFFFFF;")
        
        self.status_text = QLabel("Ready")
        status_font = QFont(self.main_font, 10)
        self.status_text.setFont(status_font)
        self.status_text.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #CCCCCC;
                border-radius: 2px;
            }
        """)
        self.progress_bar.hide()
        
        status_layout.addWidget(self.status_icon)
        status_layout.addWidget(self.status_text)
        status_layout.addStretch()
        
        main_layout.addLayout(status_layout)
        main_layout.addWidget(self.progress_bar)

        self.pulse_animation = QPropertyAnimation(self, b"pulse_value")
        self.pulse_animation.setDuration(1200)
        self.pulse_animation.setStartValue(0)
        self.pulse_animation.setEndValue(2 * math.pi)
        self.pulse_animation.setLoopCount(-1)
        
        self.setWindowOpacity(0.0)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        if self.is_dark_theme:
            self.theme_button.setText("🌙")
            self.set_dark_theme()
        else:
            self.theme_button.setText("☀️")
            self.set_light_theme()
        self.update()

    def set_dark_theme(self):
        self.title_label.setStyleSheet("color: #FFFFFF;")
        self.command_icon.setStyleSheet("color: #CCCCCC; padding-right: 10px;")
        self.input.setStyleSheet("""
            QLineEdit {
                color: white;
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 14px;
                selection-background-color: rgba(200, 200, 200, 0.3);
            }
            QLineEdit:focus {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid #CCCCCC;
            }
        """)
        self.status_text.setStyleSheet("color: rgba(255, 255, 255, 0.7);")

    def set_light_theme(self):
        self.title_label.setStyleSheet("color: #000000;")
        self.command_icon.setStyleSheet("color: #666666; padding-right: 10px;")
        self.input.setStyleSheet("""
            QLineEdit {
                color: black;
                background-color: rgba(0, 0, 0, 0.05);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                padding: 14px;
                selection-background-color: rgba(100, 100, 100, 0.3);
            }
            QLineEdit:focus {
                background-color: rgba(0, 0, 0, 0.08);
                border: 1px solid #666666;
            }
        """)
        self.status_text.setStyleSheet("color: rgba(0, 0, 0, 0.7);")

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        self.process_file(file_path)
    
    def process_file(self, file_path):
        if file_path:
            self.uploaded_file = file_path
            file_name = os.path.basename(file_path)
            extension = os.path.splitext(file_path)[1].lower()
            if extension in ['.png', '.jpg', '.jpeg', '.bmp']:
                self.file_type = 'image'
                self.command_icon.setText("🖼️")
                self.code_language = None
                self.set_status(f"Image: {file_name}", "#FFFFFF")
            elif extension in ['.py', '.html', '.js', '.css', '.java', '.cpp', '.c', '.rb', '.php', '.swift', '.kt', '.go', '.rs']:
                self.file_type = 'code'
                self.command_icon.setText("💻")
                language_map = {
                    '.py': 'Python',
                    '.html': 'HTML',
                    '.js': 'JavaScript',
                    '.css': 'CSS',
                    '.java': 'Java',
                    '.cpp': 'C++',
                    '.c': 'C',
                    '.rb': 'Ruby',
                    '.php': 'PHP',
                    '.swift': 'Swift',
                    '.kt': 'Kotlin',
                    '.go': 'Go',
                    '.rs': 'Rust'
                }
                self.code_language = language_map.get(extension, 'Unknown')
                self.set_status(f"{self.code_language} Code: {file_name}", "#FFFFFF")
            elif extension in ['.txt', '.md', '.log', '.csv', '.json']:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.input.setText(content)
                    self.file_type = None
                    self.command_icon.setText("📄")
                    self.code_language = None
                    self.set_status(f"Text: {file_name}", "#FFFFFF")
                except Exception as e:
                    print(f"Error reading text file: {e}")
                    self.uploaded_file = None
                    self.file_type = None
                    self.command_icon.setText("⌘")
                    self.code_language = None
                    self.set_status("Error loading text file", "#666666", timeout=2000)
            else:
                self.uploaded_file = None
                self.file_type = None
                self.command_icon.setText("⌘")
                self.code_language = None
                self.set_status("Unsupported file type", "#666666", timeout=2000)
        else:
            self.uploaded_file = None
            self.file_type = None
            self.command_icon.setText("⌘")
            self.code_language = None
            self.set_status("Ready", "#FFFFFF")
        self.force_focus()

    def dragEnterEvent(self, event):
        if self.processing:
            event.ignore()
        elif event.mimeData().hasUrls():
            self.is_dragging_over = True
            self.update()
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.is_dragging_over = False
        self.update()

    def dropEvent(self, event):
        if self.processing:
            return
        self.is_dragging_over = False
        self.update()
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.process_file(file_path)

    def force_focus(self):
        self.activateWindow()
        self.input.setFocus(Qt.OtherFocusReason)
        
    def fade_in(self):
        anim = QPropertyAnimation(self, b"opacity")
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.setDuration(300)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.finished.connect(self.force_focus)
        anim.start()
        self._fade_anim = anim

    def fade_out_and_hide(self):
        anim = QPropertyAnimation(self, b"opacity")
        anim.setEasingCurve(QEasingCurve.InCubic)
        anim.setDuration(250)
        anim.setStartValue(self._opacity)
        anim.setEndValue(0.0)
        anim.finished.connect(self.hide)
        anim.start()
        self._fade_out_anim = anim

    def get_opacity(self):
        return self._opacity

    def set_opacity(self, value):
        self._opacity = value
        self.setWindowOpacity(value)

    opacity = pyqtProperty(float, get_opacity, set_opacity)
    
    def set_status(self, status, color="#FFFFFF", timeout=None):
        self.status_text.setText(status)
        self.status_icon.setStyleSheet(f"color: {color};")
        if timeout:
            QTimer.singleShot(timeout, lambda: self.set_status("Ready", "#FFFFFF"))
    
    def start_processing(self):
        self.processing = True
        self.set_status("Processing...", "#AAAAAA")
        self.progress_bar.show()
        self.pulse_animation.start()
        self.input.setEnabled(False)
        self.upload_button.setEnabled(False)
        self.clear_button.setEnabled(False)
    
    def stop_processing(self):
        self.processing = False
        self.pulse_animation.stop()
        if self.uploaded_file:
            file_name = os.path.basename(self.uploaded_file)
            if self.file_type == 'image':
                self.set_status(f"Image: {file_name}", "#FFFFFF")
            elif self.file_type == 'code':
                self.set_status(f"{self.code_language} Code: {file_name}", "#FFFFFF")
            else:
                self.set_status("Ready", "#FFFFFF")
        else:
            self.set_status("Ready", "#FFFFFF")
        self.progress_bar.hide()
        self.status_icon.setStyleSheet("color: #FFFFFF;")
        self.input.setEnabled(True)
        self.upload_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        self.force_focus()

    def get_pulse_value(self):
        return self._pulse_value

    def set_pulse_value(self, value):
        self._pulse_value = value
        alpha = 150 + 50 * math.sin(value)
        self.status_icon.setStyleSheet(f"color: rgba(170, 170, 170, {int(alpha)});")

    pulse_value = pyqtProperty(float, get_pulse_value, set_pulse_value)

    def handle_command(self):
        command = self.input.text().strip()
        self.input.clear()
        self.command_history.append(command)
        self.history_model.setStringList(self.command_history)
        self.history_index = len(self.command_history)
        if not command:
            return
        self.start_processing()
        if self.file_type == 'image':
            QTimer.singleShot(50, lambda: self.process_uploaded_image(command))
        elif self.file_type == 'code':
            QTimer.singleShot(50, lambda: self.process_code_file(command))
        else:
            QTimer.singleShot(50, lambda: self.process_command(command))
        
    def process_uploaded_image(self, command):
        try:
            analyze_uploaded_image(self.uploaded_file, command)
            self.set_status("Image analysis complete", "#FFFFFF")
            QTimer.singleShot(1000, self.stop_processing)
        except Exception as e:
            self.set_status(f"Error: {str(e)[:50]}", "#666666")
            print(f"❌ Error analyzing image: {e}")
            QTimer.singleShot(1500, self.stop_processing)
        finally:
            self.uploaded_file = None
            self.file_type = None
            self.code_language = None
            self.command_icon.setText("⌘")

    def process_code_file(self, command):
        try:
            with open(self.uploaded_file, 'r', encoding='utf-8') as f:
                code_content = f.read()
            if self.code_language != 'Unknown':
                combined_input = (
                    f"You are an AI coding assistant. The user has provided the following prompt: '{command}'. "
                    f"Below is the code in {self.code_language} that needs to be analyzed or modified based on this prompt:\n\n"
                    f"{code_content}\n\nPlease provide your response accordingly."
                )
            else:
                combined_input = (
                    f"You are an AI coding assistant. The user has provided the following prompt: '{command}'. "
                    f"Below is the code that needs to be analyzed or modified based on this prompt:\n\n"
                    f"{code_content}\n\nPlease provide your response accordingly."
                )
            coding_assistant(combined_input)
            self.set_status("Code assistance complete", "#FFFFFF")
            QTimer.singleShot(1000, self.stop_processing)
        except Exception as e:
            self.set_status(f"Error: {str(e)[:50]}", "#666666")
            print(f"❌ Error processing code file: {e}")
            QTimer.singleShot(1500, self.stop_processing)
        finally:
            self.uploaded_file = None
            self.file_type = None
            self.code_language = None
            self.command_icon.setText("⌘")

    def process_command(self, command):
        try:
            func, needs_input = match_command(command.lower())
            if func:
                try:
                    result = func(command) if needs_input else func()
                    if result == "exit":
                        self.fade_out_and_hide()
                        return
                    self.set_status("Success", "#FFFFFF")
                    QTimer.singleShot(1000, self.stop_processing)
                except TypeError as e:
                    self.set_status(f"Error: {str(e)[:50]}", "#666666")
                    print(f"❌ Function argument error: {e}")
                    QTimer.singleShot(1500, self.stop_processing)
            else:
                self.set_status("Processing with AI...", "#AAAAAA")
                response = chat_with_jarvis(command)
                print(response)
                self.set_status("AI response complete", "#FFFFFF")
                QTimer.singleShot(1000, self.stop_processing)
        except Exception as e:
            self.set_status(f"Error: {type(e).__name__}", "#666666")
            print(f"❌ Error: {e}")
            QTimer.singleShot(1500, self.stop_processing)

    def showEvent(self, event):
        super().showEvent(event)
        self.fade_in()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.fade_out_and_hide()
        else:
            super().keyPressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        path = QPainterPath()
        rect = QRectF(0, 0, self.width(), self.height())
        path.addRoundedRect(rect, 20, 20)
        
        gradient = QLinearGradient(0, 0, 0, self.height())
        if self.is_dark_theme:
            gradient.setColorAt(0, QColor(10, 10, 10, 220))
            gradient.setColorAt(1, QColor(0, 0, 0, 240))
        else:
            gradient.setColorAt(0, QColor(240, 240, 240, 220))
            gradient.setColorAt(1, QColor(255, 255, 255, 240))
        painter.fillPath(path, gradient)
        
        if self.is_dragging_over:
            highlight_pen = QPen(QColor(0, 122, 255), 2)
            painter.setPen(highlight_pen)
            painter.drawPath(path)

        pen = QPen(QColor(255, 255, 255, 30) if self.is_dark_theme else QColor(0, 0, 0, 30))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawPath(path)
        
        shadow_path = QPainterPath()
        shadow_rect = QRectF(2, 2, self.width()-4, self.height()-4)
        shadow_path.addRoundedRect(shadow_rect, 18, 18)
        shadow_pen = QPen(QColor(0, 0, 0, 50))
        shadow_pen.setWidth(2)
        painter.setPen(shadow_pen)
        painter.drawPath(shadow_path)
        
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if not hasattr(self, '_last_move_time') or event.timestamp() - self._last_move_time > 16:
                self.move(event.globalPos() - self.drag_position)
                self._last_move_time = event.timestamp()
                event.accept()

    def activateWindow(self):
        super().activateWindow()
        self.raise_()
        self.input.setFocus()

def run_gui_jarvis():
    app = QApplication(sys.argv)
    overlay = CommandOverlay()
    sys.exit(app.exec_())