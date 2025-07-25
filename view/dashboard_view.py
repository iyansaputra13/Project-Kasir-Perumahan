# view/dashboard_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView, QLabel, QFrame, QLineEdit
)
from PySide6.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush
from PySide6.QtCore import Qt
from controller.transaksi_controller import TransaksiController
from view.form_input_dialog import FormInputDialog


class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Kasir Perumahan - RUBY")
        self.showMaximized()
        self.set_background_gradient()

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        sidebar = self.buat_sidebar()
        main_layout.addLayout(sidebar, 1)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(30, 20, 30, 20)
        content_layout.setSpacing(20)

        header_layout = QHBoxLayout()
        self.button_input = QPushButton("➕ Tambah Transaksi")
        self.button_input.setFixedHeight(42)
        self.button_input.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.button_input.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px;")
        self.button_input.clicked.connect(self.tampilkan_form_input)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Cari nama pembeli...")
        self.search_input.setFont(QFont("Segoe UI", 11))
        self.search_input.setFixedHeight(42)
        self.search_input.setStyleSheet("padding-left: 10px; border-radius: 10px; border: 1px solid #ccc;")
        header_layout.addWidget(self.button_input)
        header_layout.addWidget(self.search_input)
        content_layout.addLayout(header_layout)

        card_layout = QHBoxLayout()
        card_layout.setSpacing(20)
        self.card_transaksi = self.buat_card("🧾 Jumlah Transaksi", "0")
        self.card_penjualan = self.buat_card("💰 Total Penjualan", "Rp0")
        self.card_rumah = self.buat_card("🏡 Rumah Terjual", "0")
        card_layout.addWidget(self.card_transaksi)
        card_layout.addWidget(self.card_penjualan)
        card_layout.addWidget(self.card_rumah)
        content_layout.addLayout(card_layout)

        self.table = QTableWidget()
        self.table.setFont(QFont("Segoe UI", 12))
        self.table.setStyleSheet("QTableWidget { background-color: #fff; border: 1px solid #ddd; }")
        self.table.setAlternatingRowColors(True)
        content_layout.addWidget(self.table)

        main_layout.addLayout(content_layout, 5)

        self.controller = TransaksiController()
        self.load_data()

    def set_background_gradient(self):
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#f9f9f9"))
        gradient.setColorAt(1.0, QColor("#ffffff"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def buat_sidebar(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 30, 20, 20)

        label = QLabel("🏠 Kasir RUBY")
        label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(label)

        buttons = [
            ("📊 Dashboard", "#3498db"),
            ("📁 Laporan", "#9b59b6"),
            ("🚪 Keluar", "#e74c3c")
        ]

        for text, color in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(45)
            btn.setFont(QFont("Segoe UI", 11))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border-radius: 10px;
                }}
                QPushButton:hover {{
                    background-color: #2c3e50;
                }}
            """)
            layout.addWidget(btn)

        layout.addStretch()
        return layout

    def buat_card(self, title, value):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #f0f8ff;
                border-radius: 16px;
                padding: 16px;
                border: 1px solid #c4dbe2;
            }
        """)
        layout = QVBoxLayout()
        label_title = QLabel(title)
        label_title.setFont(QFont("Segoe UI", 10, QFont.Bold))
        label_value = QLabel(value)
        label_value.setFont(QFont("Segoe UI", 20, QFont.Bold))
        frame.value_label = label_value
        layout.addWidget(label_title)
        layout.addWidget(label_value)
        frame.setLayout(layout)
        return frame

    def tampilkan_form_input(self):
        form = FormInputDialog(self)
        if form.exec():
            self.load_data()

    def format_rupiah(self, nilai):
        try:
            return f"{int(nilai):,}".replace(",", ".")
        except:
            return str(nilai)

    def load_data(self):
        try:
            data = self.controller.ambil_semua_transaksi()
            headers = [
                "ID", "Nama", "NIK", "TTL", "Alamat", "No HP", "Email",
                "Nama Proyek", "Blok/Kavling", "Tipe Rumah", "Harga Jual",
                "UTJ", "DP 20%", "Sisa Setelah DP", "Cicilan per Bulan"
            ]
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)
            self.table.setRowCount(len(data))

            total_penjualan = 0

            for row_index, row_data in enumerate(data):
                if len(row_data) < len(headers):
                    continue  # Lewati jika datanya tidak lengkap

                for col_index in range(len(headers)):
                    item = row_data[col_index]
                    item_text = str(item) if item is not None else ""
                    if headers[col_index] in ["Harga Jual", "UTJ", "DP 20%", "Sisa Setelah DP", "Cicilan per Bulan"]:
                        item_text = self.format_rupiah(item)
                        if headers[col_index] == "Harga Jual":
                            try:
                                total_penjualan += int(item)
                            except:
                                pass

                    cell_item = QTableWidgetItem(item_text)
                    cell_item.setFont(QFont("Segoe UI", 11))
                    self.table.setItem(row_index, col_index, cell_item)

            self.table.resizeColumnsToContents()
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            self.card_transaksi.value_label.setText(str(len(data)))
            self.card_penjualan.value_label.setText("Rp" + self.format_rupiah(total_penjualan))
            self.card_rumah.value_label.setText(str(len(data)))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data: {str(e)}")
