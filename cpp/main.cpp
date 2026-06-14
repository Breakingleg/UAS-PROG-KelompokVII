#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <set>
#include <map>
#include <algorithm>
#include <iomanip>

using namespace std;

// Struktur Data
struct SensorRecord {
    string tanggal;
    string lokasi;
    string parameter;
    double nilai;
    string satuan;
};

// Fungsi Baca CSV
vector<SensorRecord> baca_dataset(string filepath) {
    vector<SensorRecord> records;
    ifstream file(filepath);
    if (!file.is_open()) return records;

    string line;
    getline(file, line); // Skip header

    while (getline(file, line)) {
        stringstream ss(line);
        string tgl, lok, param, val_str, sat;
        
        getline(ss, tgl, ',');
        getline(ss, lok, ',');
        getline(ss, param, ',');
        getline(ss, val_str, ',');
        getline(ss, sat, ',');

        if (!tgl.empty() && !val_str.empty()) {
            try {
                records.push_back({tgl, lok, param, stod(val_str), sat});
            } catch (...) {}
        }
    }
    file.close();
    return records;
}

// Fungsi Utama Analisis
int main() {
    // Ini yang diubah ↓
    string input_csv = "../dataset/sustainability_data.csv";
    string output_txt = "../output/laporan_sustainability.txt";

    vector<SensorRecord> records = baca_dataset(input_csv);
    if (records.empty()) {
        cout << "[ERROR] Gagal membaca data!\n";
        return 1;
    }

    ofstream out(output_txt);
    auto tulis = [&](string teks) {
        cout << teks << endl;
        out << teks << endl;
    };

    // Variabel Penampung
    set<string> gedung_unik, param_unik;
    map<string, vector<double>> stat_param;
    map<string, map<string, double>> total_per_gedung;

    for (const auto& r : records) {
        gedung_unik.insert(r.lokasi);
        param_unik.insert(r.parameter);
        stat_param[r.parameter].push_back(r.nilai);
        total_per_gedung[r.lokasi][r.parameter] += r.nilai;
    }

    tulis("=================================================================");
    tulis("   SISTEM ANALITIK SUSTAINABILITY KAMPUS UNESA");
    tulis("=================================================================\n");

    // 1. RINGKASAN
    tulis("[ RINGKASAN DATA ]");
    tulis("----------------------------------------");
    tulis("  Jumlah Record    : " + to_string(records.size()));
    tulis("  Jumlah Gedung    : " + to_string(gedung_unik.size()));
    tulis("  Jumlah Parameter : " + to_string(param_unik.size()) + "\n");

    // 2. STATISTIK
    tulis("[ ANALISIS STATISTIK PER PARAMETER ]");
    tulis("----------------------------------------");
    out << fixed << setprecision(2);
    cout << fixed << setprecision(2);
    
    for (const auto& p : param_unik) {
        auto& vals = stat_param[p];
        
        
        double sum = 0;
        double max_v = vals.front();
        double min_v = vals.front();
        
        
        for (double v : vals) {
            sum += v;
            if (v > max_v) max_v = v;
            if (v < min_v) min_v = v;
        }
        tulis("  " + p);
        tulis(" Rata-rata : " + to_string(sum / vals.size()));
        tulis(" Maksimum  : " + to_string(max_v));
        tulis(" Minimum   : " + to_string(min_v) + "\n");
    }

    // 3. ANALISIS KAMPUS
    tulis("[ ANALISIS KAMPUS - GEDUNG TERTINGGI ]");
    tulis("----------------------------------------");
    for (const auto& p : param_unik) {
        string max_g = "";
        double max_v = -1;
        for (const auto& g : total_per_gedung) {
            if (g.second.count(p) && g.second.at(p) > max_v) {
                max_v = g.second.at(p);
                max_g = g.first;
            }
        }
        tulis("  Tertinggi " + p + " : " + max_g + " (" + to_string(max_v) + ")\n");
    }

    // 4. SUSTAINABILITY RATING
    tulis("[ SUSTAINABILITY RATING PER GEDUNG ]");
    tulis("  Skala: 0-40% = Green | 40-70% = Warning | >70% = Critical");
    tulis("---------------------------------------------------------");
    
    map<string, double> global_min, global_max;
    for (const auto& p : param_unik) {
        global_min[p] = 1e9; global_max[p] = -1e9;
        for (const auto& g : total_per_gedung) {
            double val = g.second.count(p) ? g.second.at(p) : 0;
            global_min[p] = min(global_min[p], val);
            global_max[p] = max(global_max[p], val);
        }
    }

    for (const auto& g : total_per_gedung) {
        double total_skor = 0;
        for (const auto& p : param_unik) {
            double val = g.second.count(p) ? g.second.at(p) : 0;
            double min_v = global_min[p], max_v = global_max[p];
            double norm = (max_v == min_v) ? 0 : ((val - min_v) / (max_v - min_v)) * 100;
            total_skor += norm;
        }
        double skor_rata = total_skor / param_unik.size();
        
        string kategori = "[ CRITICAL ]";
        if (skor_rata <= 40) kategori = "[ GREEN ]";
        else if (skor_rata <= 70) kategori = "[ WARNING ]";

        // Kunci desimal jadi 2 digit biar lurus rata kanan
        stringstream ss;
        ss << fixed << setprecision(2); 
        ss << "  " << left << setw(12) << g.first 
           << " " << right << setw(7) << skor_rata << "%   " << kategori;
        tulis(ss.str());
    }

    tulis("\n=================================================================");
    tulis(" Analisis selesai. Hasil disimpan di " + output_txt);
    
    out.close();
    return 0;
}