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
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI, sans-serif;
                font-size: 13px;
            }
            QTableWidget {
                gridline-color: #ecf0f1;
                background-color: #ffffff;
                alternate-background-color: #f9f9f9;
                border: 1px solid #ddd;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
            }
            QLabel#statusBar {
                background-color: #f4f6f7;
                border-top: 1px solid #dcdcdc;
                color: #7f8c8d;
                padding: 5px;
                font-size: 11px;
            }
        """)

        # === Header ===
        header_layout = QHBoxLayout()

        title = QLabel("🏠 Dashboard Transaksi Rumah")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")

        self.user_info_label = QLabel(
            f"{self.user_data.get('full_name', '')} "
            f"({self.user_data.get('role', 'user')})"
        )
        self.user_info_label.setStyleSheet("font-size: 12px; color: #7f8c8d; padding: 5px;")

        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 6px 14px;
                border-radius: 6px;
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

        # === Search bar ===
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Cari nama, NIK, proyek, atau tipe rumah...")
        self.search_input.textChanged.connect(self.load_data)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        # === Tombol Tambah dan Refresh ===
        button_layout = QHBoxLayout()

        tambah_button = QPushButton("➕ Tambah Transaksi")
        tambah_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 18px;
                border-radius: 6px;
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
                padding: 8px 18px;
                border-radius: 6px;
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

        # === Tabel Transaksi ===
        self.tabel = QTableWidget()
        self.tabel.setAlternatingRowColors(True)
        self.tabel.setColumnCount(17)  # 16 data + 1 kolom aksi
        self.tabel.setHorizontalHeaderLabels([
            "ID", "Nama", "NIK", "Tempat Lahir", "Tanggal Lahir",
            "Alamat", "No HP", "Email", "Proyek", "Blok/Kavling",
            "Tipe Rumah", "Harga Jual", "Skema", "UTJ", "DP",
            "Cicilan/Bulan", "Aksi"
        ])
        header = self.tabel.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        self.tabel.setSortingEnabled(True)
        main_layout.addWidget(self.tabel)

        # === Status Bar ===
        self.status_label = QLabel("✅ Sistem siap")
        self.status_label.setObjectName("statusBar")
        main_layout.addWidget(self.status_label)

    def update_status(self, message):
        self.status_label.setText(message)

    def load_data(self):
        try:
            self.tabel.setSortingEnabled(False)
            self.tabel.setRowCount(0)
            self.update_status("⏳ Memuat data...")

            transaksi_list = self.controller.ambil_semua_transaksi()
            query = self.search_input.text().strip().lower()

            if not transaksi_list:
                self.update_status("⚠ Tidak ada data transaksi")
                return

            filtered = []
            for t in transaksi_list:
                if query:
                    search_fields = [
                        str(t.get("nama", "")).lower(),
                        str(t.get("nik", "")).lower(),
                        str(t.get("proyek", "")).lower(),
                        str(t.get("tipe_rumah", "")).lower()
                    ]
                    if not any(query in field for field in search_fields):
                        continue
                filtered.append(t)

            for row_index, t in enumerate(filtered):
                self.tabel.insertRow(row_index)

                # Isi kolom data
                fields = [
                    "id", "nama", "nik", "tempat_lahir", "tanggal_lahir",
                    "alamat", "no_hp", "email", "nama_proyek", "blok_kavling",
                    "tipe_rumah", "harga_rumah", "skema_pembayaran", "utj", "dp", "cicilan_per_bulan"
                ]

                for col_index, field in enumerate(fields):
                    item = QTableWidgetItem()
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    val = t.get(field)
                    if val is None:
                        item.setText("-")
                    elif field in ["harga", "harga_rumah", "utj", "dp", "cicilan", "cicilan_per_bulan"]:
                        try:
                            item.setText(f"Rp {int(val):,}".replace(",", "."))
                        except Exception:
                            item.setText(str(val))
                    else:
                        item.setText(str(val)[:40])  # Batasi panjang teks
                    self.tabel.setItem(row_index, col_index, item)

                # === Kolom Aksi ===
                aksi_layout = QHBoxLayout()
                aksi_widget = QWidget()

                btn_detail = QPushButton("👁")
                btn_detail.setToolTip("Lihat detail")
                btn_detail.setStyleSheet("background-color: #f39c12; color: white; border-radius: 4px; padding:4px;")
                btn_detail.clicked.connect(lambda _, data=t: self.buka_detail_pembayaran(data))

                btn_edit = QPushButton("✏")
                btn_edit.setToolTip("Edit data")
                btn_edit.setStyleSheet("background-color: #2980b9; color: white; border-radius: 4px; padding:4px;")
                btn_edit.clicked.connect(lambda _, data=t: self.edit_transaksi(data))

                btn_hapus = QPushButton("🗑")
                btn_hapus.setToolTip("Hapus data")
                btn_hapus.setStyleSheet("background-color: #c0392b; color: white; border-radius: 4px; padding:4px;")
                btn_hapus.clicked.connect(lambda _, data=t: self.hapus_transaksi(data))

                for b in [btn_detail, btn_edit, btn_hapus]:
                    aksi_layout.addWidget(b)
                aksi_layout.setContentsMargins(0, 0, 0, 0)
                aksi_widget.setLayout(aksi_layout)

                self.tabel.setCellWidget(row_index, 16, aksi_widget)

            self.update_status(f"✅ Data berhasil dimuat ({len(filtered)} transaksi)")

        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Gagal memuat data transaksi:\n{str(e)}")
        finally:
            self.tabel.setSortingEnabled(True)

    def tampilkan_form_input(self):
        dialog = FormInputDialog(self)
        if dialog.exec():
            self.load_data()
            self.update_status("✅ Transaksi baru ditambahkan")
            QMessageBox.information(self, "Sukses", "Transaksi berhasil disimpan.")

    def edit_transaksi(self, data):
        dialog = FormInputDialog(self)
        if hasattr(dialog, "load_data"):
            dialog.load_data(data)
        if dialog.exec():
            self.load_data()
            self.update_status("✏ Transaksi berhasil diperbarui")

    def hapus_transaksi(self, data):
        konfirmasi = QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Yakin ingin menghapus transaksi atas nama {data.get('nama', '')}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if konfirmasi == QMessageBox.Yes:
            self.controller.hapus_transaksi(data.get("id"))
            self.load_data()
            QMessageBox.information(self, "Info", "🗑 Data berhasil dihapus")

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
