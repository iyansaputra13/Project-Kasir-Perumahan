import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
from view.dashboard_view import DashboardView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KasirPerumahan v1.0")
        self.setMinimumSize(1280, 720)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
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
        """)

        # Widget utama
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Tambahkan Dashboard
        self.dashboard = DashboardView()
        main_layout.addWidget(self.dashboard)

        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Style umum untuk seluruh aplikasi
    app.setStyleSheet("""
        QLabel {
            font: 10pt "Segoe UI";
        }
        QLineEdit, QComboBox, QDateEdit {
            padding: 5px;
            font: 10pt "Segoe UI";
            border: 1px solid #ccc;
            border-radius: 3px;
        }
        QPushButton {
            font: 10pt "Segoe UI";
        }
        QTableWidget {
            font: 10pt "Segoe UI";
            border: 1px solid #ddd;
        }
        QHeaderView::section {
            background-color: #3498db;
            color: white;
            padding: 5px;
        }
    """)

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())
