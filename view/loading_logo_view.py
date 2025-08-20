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

        # Hilangkan border & background default
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Path ke logo default
        if logo_path is None:
            logo_path = Path(__file__).parent.parent / "assets" / "splash.png"
        else:
            logo_path = Path(logo_path)

        # Layout transparan
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Label untuk menampilkan logo
        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("background: transparent;")

        # Load dan resize logo
        pixmap = QPixmap(str(logo_path))
        if not pixmap.isNull():
            pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(pixmap)

        layout.addWidget(label)
        self.setLayout(layout)

        # Auto close setelah durasi tertentu
        QTimer.singleShot(duration, self.accept)
