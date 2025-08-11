# view/detail_pembayaran_view.py

from PySide6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
)
from PySide6.QtCore import Qt

class DetailPembayaranView(QDialog):
    def __init__(self, data_transaksi, parent=None):
        super().__init__(parent)
        self.data = data_transaksi
        self.setWindowTitle("Detail Pembayaran")
        self.setGeometry(300, 150, 500, 400)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Judul
        title = QLabel("💰 Detail Pembayaran Pembeli")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        label_data = [
            ("Nama", self.data[1]),
            ("NIK", self.data[2]),
            ("Proyek", self.data[8]),
            ("Tipe Rumah", self.data[10]),
            ("Harga Jual", f"Rp {int(self.data[11]):,}"),
            ("Skema", self.data[12]),
            ("UTJ", f"Rp {int(self.data[13]):,}"),
            ("DP", f"Rp {int(self.data[14]):,}"),
            ("Cicilan/Bulan", f"Rp {int(self.data[15]):,}")
        ]

        # Tampilkan semua informasi dalam bentuk label
        for label, value in label_data:
            row = QHBoxLayout()
            lbl1 = QLabel(f"{label}:")
            lbl1.setFixedWidth(130)
            lbl2 = QLabel(str(value))
            row.addWidget(lbl1)
            row.addWidget(lbl2)
            layout.addLayout(row)

            # Tambahkan garis pemisah
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            layout.addWidget(separator)

        layout.addStretch()

        # Tombol Tutup
        close_btn = QPushButton("Tutup")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)

        self.setLayout(layout)
