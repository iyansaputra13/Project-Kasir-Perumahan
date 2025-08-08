from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer
from pathlib import Path

class LoadingLogoView(QDialog):
    def __init__(self, logo_path=None, duration=1500, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Loading")
        self.setModal(True)
        self.setFixedSize(300, 300)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # ✅ Hilangkan background putih

        # Set path ke logo
        if logo_path is None:
            logo_path = Path(__file__).parent.parent / "assets" / "splash.png"
        else:
            logo_path = Path(logo_path)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # ✅ Hilangkan margin
        layout.setSpacing(0)

        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("background: transparent;")  # ✅ Pastikan label juga transparan

        pixmap = QPixmap(str(logo_path))
        if not pixmap.isNull():
            pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(pixmap)

        layout.addWidget(label)
        self.setLayout(layout)

        # Auto-close setelah waktu tertentu
        QTimer.singleShot(duration, self.accept)
