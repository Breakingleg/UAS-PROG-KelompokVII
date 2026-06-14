"""
=============================================================
  SISTEM ANALITIK SUSTAINABILITY KAMPUS UNESA
=============================================================
"""

import csv
import os
from datetime import datetime

# ─────────────────────────────────────────────
#  STRUKTUR DATA
# ─────────────────────────────────────────────
class SensorRecord:
    def __init__(self, tanggal, lokasi, parameter, nilai, satuan):
        self.tanggal   = tanggal
        self.lokasi    = lokasi
        self.parameter = parameter
        self.nilai     = float(nilai)
        self.satuan    = satuan

    def __repr__(self):
        return (f"SensorRecord({self.tanggal}, {self.lokasi}, "
                f"{self.parameter}, {self.nilai} {self.satuan})")


# ─────────────────────────────────────────────
#  1. BACA DATASET
# ─────────────────────────────────────────────
def baca_dataset(filepath: str) -> list[SensorRecord]:
    """Membaca file CSV dan mengembalikan list SensorRecord."""
    records = []
    if not os.path.exists(filepath):
        print(f"[ERROR] File tidak ditemukan di jalur: \n{filepath}\nPastikan folder 'dataset' dan file CSV sudah benar.")
        return records

    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                rec = SensorRecord(
                    tanggal   = row['tanggal'],
                    lokasi    = row['lokasi'],
                    parameter = row['parameter'],
                    nilai     = row['nilai'],
                    satuan    = row['satuan']
                )
                records.append(rec)
            except (KeyError, ValueError) as e:
                pass # Skip baris error diam-diam biar terminal rapi

    print(f"[OK] Berhasil membaca {len(records)} record dari data CSV.")
    return records


# ─────────────────────────────────────────────
#  2. RINGKASAN DATA
# ─────────────────────────────────────────────
def ringkasan_data(records: list[SensorRecord]) -> dict:
    """Mengembalikan metadata ringkasan dataset."""
    jumlah_record   = len(records)
    jumlah_gedung   = len(set(r.lokasi for r in records))
    jumlah_parameter= len(set(r.parameter for r in records))
    daftar_gedung   = sorted(set(r.lokasi for r in records))
    daftar_parameter= sorted(set(r.parameter for r in records))
    tanggal_awal    = min(r.tanggal for r in records)
    tanggal_akhir   = max(r.tanggal for r in records)

    return {
        "jumlah_record"    : jumlah_record,
        "jumlah_gedung"    : jumlah_gedung,
        "jumlah_parameter" : jumlah_parameter,
        "daftar_gedung"    : daftar_gedung,
        "daftar_parameter" : daftar_parameter,
        "tanggal_awal"     : tanggal_awal,
        "tanggal_akhir"    : tanggal_akhir,
    }


# ─────────────────────────────────────────────
#  3. ANALISIS STATISTIK PER PARAMETER
# ─────────────────────────────────────────────
def analisis_statistik(records: list[SensorRecord]) -> dict:
    """Hitung rata-rata, maksimum, minimum per parameter."""
    from collections import defaultdict
    data_per_param = defaultdict(list)

    for r in records:
        data_per_param[r.parameter].append(r.nilai)

    statistik = {}
    for param, values in data_per_param.items():
        statistik[param] = {
            "rata_rata" : sum(values) / len(values),
            "maksimum"  : max(values),
            "minimum"   : min(values),
            "total"     : sum(values),
            "jumlah"    : len(values),
        }
    return statistik


# ─────────────────────────────────────────────
#  4. ANALISIS KAMPUS (per gedung per parameter)
# ─────────────────────────────────────────────
def analisis_kampus(records: list[SensorRecord]) -> dict:
    """Hitung total nilai per gedung per parameter, lalu cari tertinggi."""
    from collections import defaultdict
    total = defaultdict(lambda: defaultdict(float))

    for r in records:
        total[r.lokasi][r.parameter] += r.nilai

    # Cari gedung tertinggi untuk setiap parameter
    parameters = ["Energy", "Water", "CO2", "Waste"]
    hasil = {}

    for param in parameters:
        gedung_tertinggi = max(total.keys(), key=lambda g: total[g][param])
        hasil[param] = {
            "gedung" : gedung_tertinggi,
            "total"  : total[gedung_tertinggi][param],
        }

    # Kembalikan juga tabel lengkap per gedung
    hasil["tabel_per_gedung"] = {
        gedung: dict(params) for gedung, params in total.items()
    }
    return hasil


# ─────────────────────────────────────────────
#  5. SUSTAINABILITY RATING
# ─────────────────────────────────────────────
def hitung_sustainability_rating(records: list[SensorRecord]) -> dict:
    """Normalisasi nilai ke 0-100%, klasifikasi: Green, Warning, Critical"""
    from collections import defaultdict

    total = defaultdict(lambda: defaultdict(float))
    for r in records:
        total[r.lokasi][r.parameter] += r.nilai

    parameters = ["Energy", "Water", "CO2", "Waste"]

    # Hitung min & max global per parameter
    semua_nilai = {p: [] for p in parameters}
    for gedung in total:
        for p in parameters:
            semua_nilai[p].append(total[gedung][p])

    global_min = {p: min(semua_nilai[p]) for p in parameters}
    global_max = {p: max(semua_nilai[p]) for p in parameters}

    rating_result = {}
    for gedung in sorted(total.keys()):
        skor_list = []
        for p in parameters:
            mn, mx = global_min[p], global_max[p]
            if mx == mn:
                normalized = 0.0
            else:
                normalized = (total[gedung][p] - mn) / (mx - mn) * 100
            skor_list.append(normalized)

        skor_rata = sum(skor_list) / len(skor_list)

        if skor_rata <= 40:
            kategori = "[ GREEN ]"
        elif skor_rata <= 70:
            kategori = "[ WARNING ]"
        else:
            kategori = "[ CRITICAL ]"

        rating_result[gedung] = {
            "skor"     : skor_rata,
            "kategori" : kategori,
            "detail"   : {p: skor_list[i] for i, p in enumerate(parameters)},
        }

    return rating_result


# ─────────────────────────────────────────────
#  6. CETAK & SIMPAN HASIL
# ─────────────────────────────────────────────
def cetak_dan_simpan(ringkasan, statistik, kampus, rating, output_file):
    lines = []

    def tulis(teks=""):
        lines.append(teks)
        print(teks)

    border = "=" * 65

    tulis(border)
    tulis("   SISTEM ANALITIK SUSTAINABILITY KAMPUS UNESA")
    tulis("   [ >>> OUTPUT VERSI PYTHON <<< ]")
    tulis(f"   Dibuat pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    tulis(border)

    # ── Ringkasan ──
    tulis()
    tulis("[ RINGKASAN DATA ]")
    tulis("-" * 40)
    tulis(f"  Jumlah Record    : {ringkasan['jumlah_record']:,}")
    tulis(f"  Jumlah Gedung    : {ringkasan['jumlah_gedung']}")
    tulis(f"  Jumlah Parameter : {ringkasan['jumlah_parameter']}")
    tulis(f"  Periode          : {ringkasan['tanggal_awal']} s.d. {ringkasan['tanggal_akhir']}")
    tulis(f"  Daftar Gedung    : {', '.join(ringkasan['daftar_gedung'])}")
    tulis(f"  Daftar Parameter : {', '.join(ringkasan['daftar_parameter'])}")

    # ── Statistik ──
    tulis()
    tulis("[ ANALISIS STATISTIK PER PARAMETER ]")
    tulis("-" * 40)
    satuan_map = {"Energy": "kWh", "Water": "L", "CO2": "ppm", "Waste": "kg"}
    for param, stat in statistik.items():
        sat = satuan_map.get(param, "")
        tulis(f"  {param} ({sat})")
        tulis(f"    Rata-rata : {stat['rata_rata']:.2f}")
        tulis(f"    Maksimum  : {stat['maksimum']:.2f}")
        tulis(f"    Minimum   : {stat['minimum']:.2f}")
        tulis(f"    Total     : {stat['total']:,.2f}")
        tulis()

    # ── Analisis Kampus ──
    tulis("[ ANALISIS KAMPUS – GEDUNG TERTINGGI ]")
    tulis("-" * 40)
    label_map = {
        "Energy": "Konsumsi Energi Tertinggi",
        "Water" : "Penggunaan Air Tertinggi",
        "CO2"   : "Emisi CO₂ Tertinggi",
        "Waste" : "Produksi Sampah Tertinggi",
    }
    for param, info in kampus.items():
        if param == "tabel_per_gedung":
            continue
        sat = satuan_map.get(param, "")
        tulis(f"  {label_map[param]}")
        tulis(f"    Gedung : {info['gedung']}")
        tulis(f"    Total  : {info['total']:,.2f} {sat}")
        tulis()

    # ── Sustainability Rating ──
    tulis()
    tulis("[ SUSTAINABILITY RATING PER GEDUNG ]")
    tulis("  Skala: 0-40% = Green | 40-70% = Warning | >70% = Critical")
    tulis("-" * 65)
    tulis(f"  {'Gedung':<12} {'Skor (%)':>10}  {'Kategori':<20}")
    tulis("  " + "-" * 45)
    for gedung, info in sorted(rating.items()):
        tulis(f"  {gedung:<12} {info['skor']:>9.2f}%  {info['kategori']}")

    tulis()
    tulis(border)
    tulis("  Analisis selesai.")
    tulis(border)

    # Simpan ke file .txt (Otomatis bikin file kalau belum ada)
    # Pastikan folder output-nya sudah ada
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"\n[SAVED] Hasil disimpan ke folder output!")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    # --- GPS OTOMATIS: Anti nyasar jalur folder ---
    # 1. Dapatkan lokasi folder tempat main.py ini berada (folder 'python')
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Naik satu folder ke folder utama tugas
    root_dir = os.path.dirname(base_dir)
    
    # 3. Kunci target lokasi dataset dan output secara mutlak
    input_csv  = os.path.join(root_dir, "dataset", "sustainability_data.csv")
    output_txt = os.path.join(root_dir, "output", "laporan_sustainability_python.txt")
    # ----------------------------------------------

    # 1. Baca data
    records = baca_dataset(input_csv)
    if not records:
        return

    # 2. Ringkasan
    ringkasan = ringkasan_data(records)

    # 3. Statistik
    statistik = analisis_statistik(records)

    # 4. Analisis kampus
    kampus = analisis_kampus(records)

    # 5. Rating
    rating = hitung_sustainability_rating(records)

    # 6. Cetak & simpan
    cetak_dan_simpan(ringkasan, statistik, kampus, rating, output_txt)


if __name__ == "__main__":
    main()