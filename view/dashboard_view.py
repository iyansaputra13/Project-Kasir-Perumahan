from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView, QLabel, QLineEdit
)
from PySide6.QtCore import Qt, Signal
from view.form_input_dialog import FormInputDialog
from view.detail_pembayaran_view import DetailPembayaranView
from controller.transaksi_controller import TransaksiController

class DashboardView(QWidget):
    logout_requested = Signal()

    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.controller = TransaksiController()
        self._logging_out = False
        self.init_ui()
        self.load_data()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        header_layout = QHBoxLayout()

        title = QLabel("\U0001F4CB Daftar Transaksi Penjualan Rumah")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")

        self.user_info_label = QLabel(
            f"User: {self.user_data.get('full_name', '')} | "
            f"Role: {self.user_data.get('role', 'user')}"
        )
        self.user_info_label.setStyleSheet("""
            font-size: 12px;
            color: #7f8c8d;
            padding: 5px;
            background-color: #f0f0f0;
            border-radius: 3px;
        """)

        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        logout_btn.clicked.connect(self.confirm_logout)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.user_info_label)
        header_layout.addWidget(logout_btn)

        main_layout.addLayout(header_layout)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari nama, NIK, proyek, atau tipe rumah...")
        self.search_input.textChanged.connect(self.load_data)
        search_layout.addWidget(QLabel("🔍"))
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        # Tombol Tambah dan Refresh
        button_layout = QHBoxLayout()
        tambah_button = QPushButton("➕ Tambah Transaksi")
        tambah_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        tambah_button.clicked.connect(self.tampilkan_form_input)

        refresh_button = QPushButton("🔄 Refresh Data")
        refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        refresh_button.clicked.connect(self.load_data)

        button_layout.addWidget(tambah_button)
        button_layout.addWidget(refresh_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Tabel Transaksi
        self.tabel = QTableWidget()
        self.tabel.setColumnCount(18)
        self.tabel.setHorizontalHeaderLabels([
            "ID", "Nama", "NIK", "Tempat Lahir", "Tanggal Lahir", 
            "Alamat", "No HP", "Email", "Proyek", "Blok/Kavling", 
            "Tipe Rumah", "Harga Jual", "Skema", "UTJ", "DP", "Cicilan/Bulan", "Aksi"
        ])
        header = self.tabel.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)
        self.tabel.setSortingEnabled(True)
        main_layout.addWidget(self.tabel)

        # Status
        self.status_label = QLabel("Sistem siap")
        self.status_label.setStyleSheet("font-size: 10px; color: #7f8c8d; border-top: 1px solid #ddd; padding: 5px;")
        main_layout.addWidget(self.status_label)

    def update_status(self, message):
        self.status_label.setText(message)

    def load_data(self):
        try:
            self.tabel.setSortingEnabled(False)
            self.tabel.setRowCount(0)
            self.update_status("Memuat data...")

            transaksi_list = self.controller.ambil_semua_transaksi()
            query = self.search_input.text().strip().lower()

            if not transaksi_list:
                self.update_status("Tidak ada data transaksi")
                return

            filtered = []
            for t in transaksi_list:
                if query:
                    search_fields = [str(t[i]).lower() for i in [1, 2, 8, 10] if t[i] is not None]
                    if not any(query in field for field in search_fields):
                        continue
                filtered.append(t)

            for row_index, t in enumerate(filtered):
                self.tabel.insertRow(row_index)
                for col_index in range(16):  # 0 - 15
                    item = QTableWidgetItem()
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    val = t[col_index]
                    if val is None:
                        item.setText("-")
                    elif col_index in [11, 13, 14, 15]:
                        item.setText(f"Rp {int(val):,}")
                    else:
                        item.setText(str(val)[:30])  # Potong jika terlalu panjang
                    self.tabel.setItem(row_index, col_index, item)

                # Kolom Aksi
                aksi_layout = QHBoxLayout()
                aksi_widget = QWidget()

                btn_detail = QPushButton("Lihat")
                btn_detail.setStyleSheet("background-color: #f39c12; color: white; border-radius: 4px;")
                btn_detail.clicked.connect(lambda _, data=t: self.buka_detail_pembayaran(data))

                btn_edit = QPushButton("Edit")
                btn_edit.setStyleSheet("background-color: #2980b9; color: white; border-radius: 4px;")
                btn_edit.clicked.connect(lambda _, data=t: self.edit_transaksi(data))

                btn_hapus = QPushButton("Hapus")
                btn_hapus.setStyleSheet("background-color: #c0392b; color: white; border-radius: 4px;")
                btn_hapus.clicked.connect(lambda _, data=t: self.hapus_transaksi(data))

                for b in [btn_detail, btn_edit, btn_hapus]:
                    aksi_layout.addWidget(b)
                aksi_layout.setContentsMargins(0, 0, 0, 0)
                aksi_widget.setLayout(aksi_layout)

                self.tabel.setCellWidget(row_index, 16, aksi_widget)

            self.update_status(f"Data berhasil dimuat ({len(filtered)} transaksi)")

        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Gagal memuat data transaksi:\n{str(e)}")
        finally:
            self.tabel.setSortingEnabled(True)

    def tampilkan_form_input(self):
        dialog = FormInputDialog(self)
        if dialog.exec():
            self.load_data()
            self.update_status("Transaksi baru ditambahkan")
            QMessageBox.information(self, "Sukses", "Transaksi berhasil disimpan.")

    def edit_transaksi(self, data):
        dialog = FormInputDialog(self)
        dialog.load_data(data)  # Fungsi ini harus kamu tambahkan di form dialog
        if dialog.exec():
            self.load_data()
            self.update_status("Transaksi berhasil diperbarui")

    def hapus_transaksi(self, data):
        konfirmasi = QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Yakin ingin menghapus transaksi atas nama {data[1]}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if konfirmasi == QMessageBox.Yes:
            self.controller.hapus_transaksi(data[0])
            self.load_data()
            QMessageBox.information(self, "Info", "Data berhasil dihapus")

    def buka_detail_pembayaran(self, data_transaksi):
        self.detail_view = DetailPembayaranView(data_transaksi)
        self.detail_view.show()

    def confirm_logout(self):
        confirm = QMessageBox.question(
            self,
            "Konfirmasi Logout",
            "Apakah Anda yakin ingin logout?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self._logging_out = True
            self.close()

    def closeEvent(self, event):
        if self._logging_out:
            self.logout_requested.emit()
            event.accept()
        else:
            confirm = QMessageBox.question(
                self,
                "Konfirmasi Keluar",
                "Apakah Anda yakin ingin keluar dari aplikasi ini?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
