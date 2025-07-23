from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
)
from controller.transaksi_controller import TransaksiController
from view.form_input_dialog import FormInputDialog

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Kasir Perumahan - RUBY")
        self.resize(900, 600)

        # Layout utama
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Tombol untuk tambah transaksi baru
        self.button_input = QPushButton("Tambah Transaksi Baru")
        self.button_input.clicked.connect(self.tampilkan_form_input)
        self.layout.addWidget(self.button_input)

        # Tabel untuk menampilkan data transaksi
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Inisialisasi controller dan muat data awal
        self.controller = TransaksiController()
        self.load_data()

    def tampilkan_form_input(self):
        """Menampilkan form input transaksi sebagai modal"""
        form = FormInputDialog(self)
        if form.exec():  # Jika form disubmit
            self.load_data()  # Reload tabel setelah simpan

    def load_data(self):
        """Memuat data dari model melalui controller ke tabel"""
        data_transaksi = self.controller.ambil_semua_transaksi()

        headers = [
            "ID", "Nama", "NIK", "TTL", "Alamat", "HP", "Email",
            "Proyek", "Blok", "Tipe", "Harga"
        ]

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(data_transaksi))

        for row_index, row_data in enumerate(data_transaksi):
            for col_index, item in enumerate(row_data):
                item_text = str(item) if item is not None else ""
                self.table.setItem(row_index, col_index, QTableWidgetItem(item_text))
