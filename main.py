# main.py
import sys
from PySide6.QtWidgets import QApplication
from view.dashboard_view import DashboardView

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dashboard = DashboardView()  # <-- hanya ini, tanpa argumen
    dashboard.show()

    sys.exit(app.exec())
