# controller/ocr_helper.py
from PIL import Image, UnidentifiedImageError
import pytesseract
import os

# Set lokasi folder tessdata agar bisa load bahasa Indonesia
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract/'

def extract_ktp_data(image_path):
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        print(f"File tidak ditemukan: {image_path}")
        return None
    except UnidentifiedImageError:
        print(f"Gambar tidak dapat dibaca: {image_path}")
        return None
    except Exception as e:
        print(f"Terjadi kesalahan saat membuka gambar: {e}")
        return None

    try:
        # Gunakan bahasa Indonesia (ind)
        text = pytesseract.image_to_string(image, lang='ind')
    except pytesseract.TesseractError as e:
        print(f"Gagal membaca gambar:\n{e}")
        return None

    # Pisah teks menjadi baris dan bersihkan
    lines = text.split('\n')
    lines = [line.strip() for line in lines if line.strip()]

    data = {
        'nik': '',
        'nama': '',
        'ttl': '',
        'alamat': '',
    }

    for i, line in enumerate(lines):
        if 'NIK' in line or line.replace(" ", "").isdigit():
            data['nik'] = line.strip()
        elif i == 1:
            data['nama'] = line.strip()
        elif 'Tempat/Tgl Lahir' in line or 'TTL' in line:
            data['ttl'] = lines[i + 1] if i + 1 < len(lines) else ''
        elif 'Alamat' in line:
            data['alamat'] = lines[i + 1] if i + 1 < len(lines) else ''

    return data
