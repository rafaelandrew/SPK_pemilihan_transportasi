# 🚆 Sistem Pendukung Keputusan (SPK) Pemilihan Transportasi

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)
![Method](https://img.shields.io/badge/Metode-AHP-green)

Aplikasi web Sistem Pendukung Keputusan (DSS) untuk merekomendasikan moda transportasi terbaik di wilayah Jabodetabek menggunakan metode **Analytic Hierarchy Process (AHP)**. Proyek ini dibangun menggunakan Python dan Framework Streamlit.

🔗 **[Lihat Demo Aplikasi Disini]([https://spkpemilihantransportasi-dhpwdmrzsv8kjfmdhvaspe.streamlit.app/])**

---

## 📖 Tentang Proyek
Sistem ini dibuat untuk membantu pengguna (komuter) memilih transportasi yang paling sesuai dengan preferensi mereka di antara berbagai pilihan yang tersedia (seperti MRT, KRL, Ojek Online, dll). Sistem menggunakan algoritma AHP untuk membobot kriteria dan merangking alternatif.

### Fitur Utama:
- **Kustomisasi Kriteria:** Pengguna dapat menentukan kriteria dan alternatif sendiri.
- **Pairwise Comparison:** Perbandingan berpasangan antar kriteria (AHP).
- **Rating Model:** Penilaian skor alternatif menggunakan skala 1-10.
- **Visualisasi Hasil:** Menampilkan tabel ranking, matriks ternormalisasi, dan data input.
- **Responsive UI:** Tampilan yang ramah pengguna berbasis Web.

---

## ⚙️ Metodologi
Sistem ini menerapkan metode **AHP (Analytic Hierarchy Process)** dengan tahapan:
1.  **Definisi Masalah:** Menentukan Kriteria (Biaya, Waktu, Keamanan, dll) dan Alternatif.
2.  **Pembobotan Kriteria:** Menghitung *Eigen Vector* dari matriks perbandingan berpasangan.
3.  **Normalisasi:** Menghitung konsistensi dan menormalisasi matriks.
4.  **Perangkingan:** Mengalikan bobot kriteria dengan skor alternatif (*Rating Model*).

---

## 🛠️ Teknologi yang Digunakan
* **Bahasa Pemrograman:** [Python](https://www.python.org/)
* **Web Framework:** [Streamlit](https://streamlit.io/)
* **Data Manipulation:** Pandas & NumPy
* **Visualisasi:** Matplotlib (via Pandas Styler)

---

## 🚀 Cara Menjalankan di Lokal (Localhost)

Ikuti langkah ini jika Anda ingin menjalankan aplikasi di komputer Anda sendiri:

1.  **Clone Repository**
    ```bash
    git clone [https://github.com/username-anda/nama-repo-anda.git](https://github.com/username-anda/nama-repo-anda.git)
    cd nama-repo-anda
    ```

2.  **Install Library**
    Pastikan Python sudah terinstall, lalu jalankan:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Jalankan Aplikasi**
    ```bash
    streamlit run spk_pemilihan_transportasi.py
    ```

---

## 📂 Struktur File
```text
├── spk_pemilihan_transportasi.py              # File utama aplikasi (Logika AHP & UI)
├── requirements.txt    # Daftar library yang dibutuhkan
├── README.md           # Dokumentasi proyek
└── .gitignore          # File yang diabaikan oleh Git
