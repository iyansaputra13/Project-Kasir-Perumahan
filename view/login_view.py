from PySide6.QtCore import Signal, Qt, QTimer, QPropertyAnimation, QPoint
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QHBoxLayout,
    QApplication
)
from controller.auth_controller import AuthController
import os

class LoginView(QMainWindow):
    login_success = Signal(dict)
    login_closed = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Kasir Perumahan")
        self.setFixedSize(450, 430)
        self.setStyleSheet("background-color: #ecf0f1;")
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        self.auth_controller = AuthController()
        self.login_attempts = 0
        self.max_attempts = 3
        self.lockout_duration = 30000  # 30 detik
        self._login_successful = False

        self.init_ui()
        QTimer.singleShot(100, self.username_input.setFocus)

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(12)

        # === Logo ===
        logo_path = "assets/splash.png"
        if os.path.exists(logo_path):
            logo = QLabel()
            pixmap = QPixmap(logo_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
            logo.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo)

        # === Header ===
        header = QLabel("LOGIN")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(header)

        # === Username Input ===
        username_row = QHBoxLayout()
        username_label = QLabel("Username:")
        username_label.setFixedWidth(100)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Masukkan username")
        self.username_input.setMinimumHeight(35)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background: white;
                padding-left: 6px;
                border-radius: 5px;
            }
        """)
        username_row.addWidget(username_label)
        username_row.addWidget(self.username_input)
        layout.addLayout(username_row)

        # === Password Input ===
        password_row = QHBoxLayout()
        password_label = QLabel("Password:")
        password_label.setFixedWidth(100)

        password_container = QWidget()
        password_container.setFixedHeight(35)
        password_container.setStyleSheet("background: white; border-radius: 5px;")

        password_layout = QHBoxLayout(password_container)
        password_layout.setContentsMargins(6, 0, 6, 0)
        password_layout.setSpacing(0)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Masukkan password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("border: none;")
        self.password_input.returnPressed.connect(self.try_login)

        self.toggle_password_btn = QPushButton("👁️")
        self.toggle_password_btn.setCheckable(True)
        self.toggle_password_btn.setFixedSize(30, 30)
        self.toggle_password_btn.setStyleSheet("""
    QPushButton {
        border: none;
        background: transparent;
        font-size: 14px;
        margin-left: 6px;
    }
    QPushButton:checked { color: #2980b9; }
     """)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)

        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_password_btn)

        password_row.addWidget(password_label)
        password_row.addWidget(password_container)
        layout.addLayout(password_row)

        # === Login Button ===
        self.login_btn = QPushButton("LOGIN")
        self.login_btn.setMinimumHeight(40)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton:disabled { background-color: #95a5a6; }
        """)
        self.login_btn.clicked.connect(self.try_login)
        layout.addWidget(self.login_btn)

        layout.addStretch()

        # === Footer ===
        footer = QLabel("Kawasan New City Malang")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #7f8c8d; font-size: 10px;")
        layout.addWidget(footer)

    def toggle_password_visibility(self):
        if self.toggle_password_btn.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_btn.setText("🙈")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_btn.setText("👁️")

    def try_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username:
            return self.show_error("Username tidak boleh kosong!", self.username_input)
        if not password:
            return self.show_error("Password tidak boleh kosong!", self.password_input)

        if self.login_attempts >= self.max_attempts:
            return self.lockout()

        self.set_loading(True)

        try:
            user = self.auth_controller.authenticate(username, password)
            if user:
                self._login_successful = True
                self.login_success.emit(user)
                self.close()
            else:
                self.login_attempts += 1
                if self.login_attempts < self.max_attempts:
                    remaining = self.max_attempts - self.login_attempts
                    self.show_error(f"Username atau password salah!\nPercobaan tersisa: {remaining}", self.password_input)
                else:
                    self.lockout()
        except Exception as e:
            self.show_error(f"Terjadi kesalahan sistem:\n{str(e)}")
        finally:
            self.set_loading(False)

    def lockout(self):
        QMessageBox.critical(self, "Akses Ditolak", f"Batas login {self.max_attempts} kali tercapai.\nSilakan coba lagi dalam 30 detik.")
        self.setDisabled(True)
        QTimer.singleShot(self.lockout_duration, self.reset_lockout)

    def reset_lockout(self):
        self.login_attempts = 0
        self.setDisabled(False)
        self.username_input.clear()
        self.password_input.clear()
        self.username_input.setFocus()
        QMessageBox.information(self, "Coba Lagi", "Silakan coba login kembali.")

    def show_error(self, message, focus_widget=None):
        QMessageBox.warning(self, "Peringatan", message)
        if focus_widget:
            focus_widget.selectAll()
            focus_widget.setFocus()
        self.shake_window()

    def set_loading(self, loading):
        self.login_btn.setDisabled(loading)
        self.login_btn.setText("Memproses..." if loading else "LOGIN")
        QApplication.processEvents()

    def shake_window(self):
        animation = QPropertyAnimation(self, b"pos")
        animation.setDuration(300)
        animation.setLoopCount(2)
        start_pos = self.pos()
        offset = 10
        animation.setKeyValueAt(0, start_pos)
        animation.setKeyValueAt(0.25, start_pos + QPoint(-offset, 0))
        animation.setKeyValueAt(0.5, start_pos + QPoint(offset, 0))
        animation.setKeyValueAt(0.75, start_pos + QPoint(-offset, 0))
        animation.setKeyValueAt(1, start_pos)
        animation.start()

    def closeEvent(self, event):
        if not self._login_successful:
            self.login_closed.emit()
        super().closeEvent(event)
