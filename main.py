# main.py
import sys
from PySide6.QtWidgets import QApplication
from view.dashboard_view import DashboardView

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dashboard = DashboardView()  # <-- hanya ini, tanpa argumen
    dashboard.show()

    sys.exit(app.exec())
# main.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
from views.dashboard_view import DashboardView
from views.sidebar_view import SidebarView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KasirPerumahan v1.0")
        self.setMinimumSize(1280, 720)
        self.setStyleSheet("background-color: #f9f9f9;")

        # Layout utama
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # Sidebar
        self.sidebar = SidebarView()
        main_layout.addWidget(self.sidebar)

        # Konten utama (dashboard)
        self.dashboard = DashboardView()
        main_layout.addWidget(self.dashboard, 1)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
