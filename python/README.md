# Modul Analitik Python - Smart Sustainability Campus

Modul ini berisi implementasi sistem analitik data sensor IoT menggunakan bahasa pemrograman Python. Implementasi ini memanfaatkan fleksibilitas tipe data dinamis bawaan Python untuk memetakan rekaman sensor secara cepat dan ringkas.

## Komponen File
- `main.py`: Skrip utama Python yang mencakup pembacaan dataset dengan `csv.DictReader`, pengelompokan menggunakan `defaultdict`, serta ekspor data laporan akhir.

## Prasyarat Sistem
Program ini berjalan menggunakan standar *clean code* tanpa memerlukan instalasi library eksternal (hanya menggunakan modul bawaan seperti `csv`, `os`, dan `datetime`). Pastikan perangkat sudah terinstal Python 3.x.

## Panduan Eksekusi

1. Buka Terminal atau Command Prompt di komputer.
2. Masuk ke dalam direktori folder ini:
   ```bash
   cd python

## Jalankan skrip utama menggunakan perintah:

Bash
python main.py

## Jalur Akses Data (Pathing)

Modul ini dilengkapi fitur pelacakan otomatis berbasis lokasi file (os.path.abspath). Program akan mengunci target folder secara mandiri tanpa risiko file tidak ditemukan akibat perbedaan posisi terminal:

Jalur Input  : ../dataset/sustainability_data.csv
Jalur Output : ../output/laporan_sustainability.txt