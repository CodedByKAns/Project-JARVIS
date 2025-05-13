from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint
from PyQt5.QtWidgets import QLabel, QWidget, QGraphicsDropShadowEffect, QVBoxLayout, QSizePolicy, QApplication
from PyQt5.QtGui import QFont, QColor, QFontDatabase, QFontMetrics, QTextDocument
from markdown_it import MarkdownIt
import re
import sys

class TypingPopup(QWidget):
    def __init__(self, full_text, speed=30, duration=3000, max_width=600):
        super().__init__()
        self.full_text = full_text
        self.displayed_text = ""
        self.index = 0
        self.speed = speed
        self.duration = duration
        self.max_width = max_width

        self.init_ui()
        self.setup_typing()
        self.start_slide_in()
        self.show()

    def init_ui(self):
        """Initialize the UI with proper window settings and layout."""
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("", self)
        self.label.setWordWrap(True)
        self.label.setTextFormat(Qt.RichText)
        self.label.setMaximumWidth(self.max_width)

        font_db = QFontDatabase()
        font_path = "Data/fonts/plain-text.ttf"  # Adjust path as needed
        font_id = font_db.addApplicationFont(font_path)
        if font_id == -1:
            print(f"Error: Could not load font from {font_path}")
            font = QFont("Segoe UI Semibold", 12, QFont.Bold)
        else:
            font_families = font_db.applicationFontFamilies(font_id)
            font = QFont(font_families[0], 12, QFont.Bold) if font_families else QFont("Segoe UI Semibold", 12, QFont.Bold)

        self.label.setFont(font)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(30, 30, 30, 220);
                padding: 15px 25px;
                border-radius: 15px;
                border: 2px solid white;
            }
        """)
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)

        self.font_metrics = QFontMetrics(self.label.font())

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.label.setGraphicsEffect(shadow)

        layout.addWidget(self.label)
        layout.setContentsMargins(40, 40, 40, 40)

        self.label.setText(" ")
        self.adjustSize()
        self.label.setText("")
        self.setMinimumSize(self.sizeHint())
        self.move_to_top_center()
        self.setWindowOpacity(0)

    def move_to_top_center(self):
        """Position the popup at the top center of the screen."""
        screen = self.screen().geometry()
        self.move(int((screen.width() - self.width()) / 2), 50)

    def start_slide_in(self):
        """Start the slide-in animation and delay typing until it finishes."""
        start_pos = QPoint(self.x(), -100)
        end_pos = QPoint(self.x(), 50)

        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(600)
        self.anim.setStartValue(start_pos)
        self.anim.setEndValue(end_pos)
        self.anim.finished.connect(self.start_typing)
        self.anim.start()

        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(600)
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)
        self.fade_anim.start()

    def setup_typing(self):
        """Set up the typing timer without starting it."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)

    def start_typing(self):
        """Start the typing timer."""
        self.timer.start(self.speed)

    def parse_markdown(self, text):
        """Convert markdown text to HTML, removing images and links."""
        md = MarkdownIt()
        html = md.render(text)
        html = re.sub(r'<img[^>]*>', '', html)
        html = re.sub(r'<a[^>]*>(.*?)</a>', r'\1', html)
        return html

    def update_text(self):
        """Update the displayed text and adjust size dynamically."""
        if self.index < len(self.full_text):
            self.displayed_text += self.full_text[self.index]
            processed_html = self.parse_markdown(self.displayed_text)
            
            # Calculate width based on rendered HTML
            doc = QTextDocument()
            doc.setHtml(processed_html)
            ideal_width = int(doc.idealWidth())  # Convert float to int
            new_width = min(ideal_width + 50, self.max_width)  # Add padding (25px left + 25px right)
            self.label.setFixedWidth(new_width)
            self.label.setText(processed_html)

            self.adjustSize()
            self.setMinimumSize(self.sizeHint())
            self.move_to_top_center()
            self.index += 1
        else:
            self.timer.stop()
            QTimer.singleShot(self.duration, self.fade_out)

    def fade_out(self):
        """Start the fade-out animation and close the widget when done."""
        self.fade_anim_out = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim_out.setDuration(800)
        self.fade_anim_out.setStartValue(1)
        self.fade_anim_out.setEndValue(0)
        self.fade_anim_out.finished.connect(self.close)
        self.fade_anim_out.start()

    def closeEvent(self, event):
        """Ensure all timers and animations are stopped before closing."""
        if self.timer.isActive():
            self.timer.stop()
        if hasattr(self, 'fade_anim_out') and self.fade_anim_out.state() == QPropertyAnimation.Running:
            self.fade_anim_out.stop()
        super().closeEvent(event)

