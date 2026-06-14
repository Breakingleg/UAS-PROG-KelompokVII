# UAS-ALPROG-Kelompok VII

## Anggota Kelompok
1. Abiyu Nandana - 25050874213 
2. Mas Iqbal Gusti Mahardhika - 25050874148
3. Muhammad Akbar Ferdiansyah - 25050874123
4. Zhulumanus Ghulammanar - 25050874127

## Deskripsi Proyek
Analisis Smart Sustainability Campus menggunakan C++ dan Python untuk memantau emisi CO₂, konsumsi energi, produksi sampah, dan penggunaan air di 20 gedung kampus. Sistem ini mengolah 29.200 baris data sensor (periode satu tahun) untuk memberikan *Sustainability Rating* tiap gedung dengan klasifikasi Green (0-40%), Warning (40-70%), dan Critical (>70%). Laporan ini bertujuan membantu pimpinan kampus mengambil keputusan operasional berbasis data yang ramah lingkungan.

## Struktur Folder
- `cpp/` : Skrip utama C++ (`main.cpp`) dan dokumentasinya.
- `python/` : Skrip utama Python (`main.py`) dan dokumentasinya.
- `dataset/` : File data mentah sensor IoT (`sustainability_data.csv`).
- `output/` : Lokasi penyimpanan otomatis laporan hasil analisis (`laporan_sustainability.txt`). dan laporan_sustainability_python.txt
- `docs/` : Berisi gambar flowchart alur program.

## Cara Menjalankan Program

### C++
Pastikan posisi terminal berada di dalam folder `cpp/`, lalu jalankan:

```Bash
## g++ main.cpp -o main
./main       # (Atau gunakan .\main.exe jika di Windows)

## Python
Pastikan posisi terminal berada di dalam folder python/, lalu jalankan:

```Bash
python main.py

## Ringkasan Hasil Analisis
Penyumbang Tertinggi: Gedung_O tercatat sangat boros Air (265.906 L) dan Energi (62.629 kWh). Gedung_E memiliki emisi CO₂ tertinggi (233.090 ppm), dan Gedung_A mencatat produksi sampah tertinggi (12.496 kg).

## Rating Kampus:

1 Gedung [ CRITICAL ]: Gedung_O (Skor 73.73%), butuh evaluasi segera.

14 Gedung [ WARNING ]: Berada di tahap peringatan dan butuh efisiensi.

5 Gedung [ GREEN ]: Gedung C, D, G, H, dan J menunjukkan performa sustainability yang sangat baik.

## Perbandingan C++ dan Python
Parsing Data: Python jauh lebih praktis karena memiliki library csv bawaan. Di C++, pemisahan teks CSV harus di-handle manual menggunakan fungsi stringstream dan getline.

Struktur Data: Python sangat fleksibel dengan tipe data dinamis. Sebaliknya, C++ lebih ketat karena mewajibkan deklarasi tipe data secara eksplisit di awal (menggunakan struct, map, dan vector).

Performa Eksekusi: Sebagai bahasa compiled, C++ terasa lebih cepat dan ringan memori saat melakukan perulangan pada 29.200 baris data dibandingkan Python yang merupakan bahasa interpreted.

Link Video Presentasi
https://youtu.be/xxxxxxxx


