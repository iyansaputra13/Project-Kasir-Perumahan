from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PySide6.QtGui import QFont
from controller.transaksi_controller import TransaksiController
from view.form_input_dialog import FormInputDialog

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Kasir Perumahan - RUBY")
        self.resize(1200, 600)

        # Layout utama
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Layout tombol
        button_layout = QHBoxLayout()

        # Tombol tambah transaksi
        self.button_input = QPushButton("Tambah Transaksi Baru")
        self.button_input.clicked.connect(self.tampilkan_form_input)
        button_layout.addWidget(self.button_input)

        # Tombol refresh data
        self.button_refresh = QPushButton("Refresh Data")
        self.button_refresh.clicked.connect(self.load_data)
        button_layout.addWidget(self.button_refresh)

        # Tambahkan tombol ke layout utama
        self.layout.addLayout(button_layout)

        # Tabel data transaksi
        self.table = QTableWidget()
        self.table.setFont(QFont("Arial", 11))  # Membesarkan font
        self.layout.addWidget(self.table)

        # Controller
        self.controller = TransaksiController()

        # Muat data awal
        self.load_data()

    def tampilkan_form_input(self):
        """Menampilkan form input transaksi sebagai modal"""
        form = FormInputDialog(self)
        if form.exec():  # Jika user klik Submit
            self.load_data()  # Perbarui tabel

    def format_rupiah(self, nilai):
        """Format angka menjadi format rupiah dengan titik"""
        try:
            return f"Rp{int(nilai):,}".replace(",", ".")
        except:
            return str(nilai)

    def load_data(self):
        """Mengambil semua data transaksi dan menampilkannya di tabel"""
        try:
            data_transaksi = self.controller.ambil_semua_transaksi()

            headers = [
                "ID", "Nama", "NIK", "TTL", "Alamat", "No HP", "Email",
                "Nama Proyek", "Blok/Kavling", "Tipe Rumah", "Harga Jual",
                "UTJ", "DP 20%", "Sisa Setelah DP", "Cicilan per Bulan"
            ]

            kolom_uang = [11, 12, 13, 14, 15]  # Kolom yang mengandung nilai uang

            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)
            self.table.setRowCount(len(data_transaksi))

            for row_index, row_data in enumerate(data_transaksi):
                for col_index, item in enumerate(row_data):
                    item_text = ""
                    if item is not None:
                        if col_index in kolom_uang:
                            item_text = self.format_rupiah(item)
                        else:
                            item_text = str(item)
                    self.table.setItem(row_index, col_index, QTableWidgetItem(item_text))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data: {str(e)}")
