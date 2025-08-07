import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                              QHBoxLayout, QMessageBox, QSplashScreen)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QPixmap
from view.dashboard_view import DashboardView
from view.login_view import LoginView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KasirPerumahan v1.0")
        self.setMinimumSize(1280, 720)
        self.current_user = None
        self.dashboard = None
        self.login_window = None
        
        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        """Initialize application UI components"""
        self.setup_splash_screen()
        self.apply_styles()
        QTimer.singleShot(1500, self.show_login)  # Show login after splash

    def setup_splash_screen(self):
        """Show application splash screen"""
        try:
            pixmap = QPixmap("assets/splash.png")
            self.splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
            self.splash.show()
        except Exception as e:
            print(f"Error loading splash screen: {str(e)}")

    def apply_styles(self):
        """Apply application-wide styles"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
                font-family: 'Segoe UI';
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QStatusBar {
                background-color: #3498db;
                color: white;
                padding: 5px;
                font-size: 10pt;
            }
            QMessageBox {
                font-family: 'Segoe UI';
            }
        """)

    def show_login(self):
        """Show login window and hide main window"""
        self.cleanup_dashboard()
        
        if hasattr(self, 'splash') and self.splash:
            self.splash.close()
        
        self.login_window = LoginView()
        self.login_window.login_success.connect(self.handle_login_success)
        self.login_window.login_closed.connect(self.close_application)
        self.login_window.show()
        self.hide()

    def cleanup_dashboard(self):
        """Clean up dashboard resources safely"""
        if self.dashboard:
            try:
                # Disconnect signals first
                if hasattr(self.dashboard, 'logout_requested'):
                    self.dashboard.logout_requested.disconnect()
                self.dashboard.deleteLater()
            except RuntimeError as e:
                print(f"Dashboard cleanup error: {str(e)}")
            finally:
                self.dashboard = None

    def handle_login_success(self, user_data):
        """Handle successful login"""
        self.current_user = user_data
        try:
            self.show_dashboard(user_data)
            self.update_status_message(user_data)
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Login Error", 
                f"Failed to initialize dashboard:\n{str(e)}"
            )
            self.show_login()

    def show_dashboard(self, user_data):
        """Initialize and show dashboard"""
        self.cleanup_dashboard()
        
        try:
            self.dashboard = DashboardView(user_data)
            self.dashboard.logout_requested.connect(self.handle_logout)
            
            # Clean up existing central widget
            if self.centralWidget():
                self.centralWidget().deleteLater()
                
            self.setCentralWidget(self.dashboard)
            self.showMaximized()
            
            # Close login window if exists
            if self.login_window:
                self.login_window.close()
                self.login_window = None
                
        except Exception as e:
            self.cleanup_dashboard()
            QMessageBox.critical(
                self,
                "Dashboard Error",
                f"Failed to create dashboard:\n{str(e)}"
            )
            raise

    def update_status_message(self, user_data):
        """Update status bar with user info"""
        if hasattr(self, 'statusBar'):
            status_message = (
                f"User: {user_data.get('username', 'N/A')} | "
                f"Role: {user_data.get('role', 'user')}"
            )
            self.statusBar().showMessage(status_message)

    def handle_logout(self):
        """Langsung logout tanpa konfirmasi ulang"""
        self.current_user = None
        self.show_login()

    def close_application(self):
        """Handle application close request"""
        self.close()

    def closeEvent(self, event):
        """Handle main window close event with confirmation"""
        # Create a custom QMessageBox with Indonesian text and buttons
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Konfirmasi Keluar")
        msg_box.setText("Apakah Anda yakin ingin menutup aplikasi?")
        
        # Create custom buttons with Indonesian text
        yes_button = msg_box.addButton("Ya", QMessageBox.YesRole)
        no_button = msg_box.addButton("Tidak", QMessageBox.NoRole)
        msg_box.setDefaultButton(no_button)
        
        msg_box.exec()
        
        if msg_box.clickedButton() == yes_button:
            self.cleanup_dashboard()
            if self.login_window:
                self.login_window.close()
            event.accept()
        else:
            event.ignore()

def apply_global_styles(app):
    """Apply consistent styles across the application"""
    app.setStyleSheet("""
        QWidget {
            font: 10pt 'Segoe UI';
        }
        QLineEdit, QComboBox, QDateEdit, QSpinBox {
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 3px;
            min-width: 100px;
        }
        QPushButton {
            padding: 5px 10px;
            min-width: 80px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #e0e0e0;
        }
        QTableWidget {
            border: 1px solid #ddd;
            alternate-background-color: #f9f9f9;
        }
        QHeaderView::section {
            background-color: #3498db;
            color: white;
            padding: 5px;
        }
        QTabWidget::pane {
            border: 1px solid #ddd;
        }
        QTabBar::tab {
            padding: 8px;
            background: #f1f1f1;
            border: 1px solid #ddd;
        }
        QTabBar::tab:selected {
            background: white;
        }
    """)

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        apply_global_styles(app)
        
        window = MainWindow()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)
