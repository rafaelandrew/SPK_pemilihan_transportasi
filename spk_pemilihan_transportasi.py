import streamlit as st
import numpy as np
import pandas as pd

# ==========================================
# 1. KONFIGURASI HALAMAN & CSS
# ==========================================
st.set_page_config(
    page_title="SPK Pemilihan Transportasi",
    page_icon="🚆",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        font-weight: 700;
        margin-bottom: 20px;
    }
    div[data-testid="stMetric"] {
        background-color: #f0f2f6;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FUNGSI LOGIKA (BACKEND)
# ==========================================
def hitung_bobot_ahp(matriks):
    """Menghitung Eigen Vector Normalisasi"""
    col_sums = matriks.sum(axis=0) # 1. Jumlahkan setiap kolom ke bawah
    norm_matrix = matriks / col_sums # 2. Bagi setiap sel dengan jumlah kolomnya (Normalisasi)
    bobot = norm_matrix.mean(axis=1) # 3. Ambil rata-rata baris (Eigen Vector)
    return bobot

# Catatan: Fungsi hitung_skor_akhir kita hapus/ganti logikanya langsung di Step 3
# agar kita bisa mengambil matriks ternormalisasinya untuk ditampilkan.

# ==========================================
# 3. STATE MANAGEMENT
# ==========================================
if 'step' not in st.session_state:
    st.session_state.step = 0 # Menyimpan kita sedang di halaman mana
if 'bobot_kriteria' not in st.session_state:
    st.session_state.bobot_kriteria = [] # Menyimpan hasil hitungan bobot

# ==========================================
# 4. SIDEBAR (INPUT DATA)
# ==========================================
with st.sidebar:
    st.header("⚙️ Konfigurasi Sistem")
    st.info("Atur kriteria dan alternatif di sini sebelum memulai.")

    def_kriteria = "Biaya, Waktu, Keselamatan, Kenyamanan, Ketersediaan"
    def_alternatif = "Mobil Online, Motor Online, KRL, MRT, TransJakarta"

    in_kriteria = st.text_area("Daftar Kriteria", value=def_kriteria, height=100)
    in_alternatif = st.text_area("Daftar Alternatif", value=def_alternatif, height=100)

    if st.button("Mulai Analisa Baru", type="primary"):
        list_k = [x.strip() for x in in_kriteria.split(',') if x.strip()]
        list_a = [x.strip() for x in in_alternatif.split(',') if x.strip()]
        
        if len(list_k) < 2 or len(list_a) < 2:
            st.error("Minimal 2 kriteria & 2 alternatif!")
        else:
            st.session_state.kriteria = list_k
            st.session_state.alternatif = list_a
            st.session_state.step = 1
            st.rerun()

    st.divider()
    st.caption("Andrew Riza Rafhael & Jose Garcia Puglisi")

# ==========================================
# 5. HALAMAN UTAMA (MAIN CONTENT)
# ==========================================

st.markdown('<div class="main-header">🚆 Sistem Pendukung Keputusan Transportasi</div>', unsafe_allow_html=True)

# LOGIKA STEP 0 (WELCOME)
if st.session_state.step == 0:
    st.info("👈 Silakan masukkan data Kriteria dan Alternatif di Sidebar sebelah kiri, lalu klik tombol **'Mulai Analisa Baru'**.")

# LOGIKA STEP 1 (PAIRWISE COMPARISON)
elif st.session_state.step == 1:
    st.subheader("Langkah 1: Perbandingan Tingkat Kepentingan (Kriteria)")
    
    kriteria = st.session_state.kriteria
    n = len(kriteria)
    matriks = np.ones((n, n))
    
    with st.form("matrix_input"):
        inputs = {}
        for i in range(n):
            for j in range(i + 1, n):
                c1, c2, c3 = st.columns([3, 2, 3])
                with c1: st.write(f"**{kriteria[i]}**")
                with c3: st.write(f"**{kriteria[j]}**", unsafe_allow_html=True)
                with c2:
                    val = st.number_input(f"Nilai {i}-{j}", 1, 9, 1, key=f"n{i}{j}")
                    dom = st.radio(f"Dominan {i}-{j}", [kriteria[i], kriteria[j]], horizontal=True, label_visibility="collapsed", key=f"r{i}{j}")
                    inputs[(i,j)] = (val, dom)
                st.divider()
        
        submitted = st.form_submit_button("Hitung Bobot Kriteria ➡️")
        
        if submitted:
            for i in range(n):
                for j in range(i+1, n):
                    val, dom = inputs[(i,j)]
                    if dom == kriteria[i]:
                        matriks[i][j] = val # Jika A lebih penting dari B nilai = 3
                        matriks[j][i] = 1/val # Maka B terhadap A otomatis = 1/3
                    else:
                        matriks[i][j] = 1/val
                        matriks[j][i] = val
            
            st.session_state.bobot_kriteria = hitung_bobot_ahp(matriks)
            st.session_state.step = 2
            st.rerun()

# LOGIKA STEP 2 (RATING ALTERNATIF)
elif st.session_state.step == 2:
    st.subheader("Langkah 2: Penilaian Alternatif")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.write("##### Bobot Prioritas:")
        df_bobot = pd.DataFrame({
            'Kriteria': st.session_state.kriteria,
            'Bobot': st.session_state.bobot_kriteria
        })
        st.dataframe(df_bobot.style.format({'Bobot': '{:.2%}'}).background_gradient(cmap="Blues"), use_container_width=True)
    with c2:
        st.bar_chart(df_bobot.set_index('Kriteria'))

    st.divider()
    st.write("##### Isi Skor Performa (1-10)")
    st.caption("💡 Tips: Isi angka 1-10. Angka semakin besar = Semakin Bagus/Murah/Cepat/Aman.")
    
    df_input = pd.DataFrame(index=st.session_state.alternatif, columns=st.session_state.kriteria)
    df_input = df_input.fillna(5)

    with st.form("rating_form"):
        edited_df = st.data_editor(
            df_input,
            column_config={c: st.column_config.NumberColumn(c, min_value=1, max_value=10) for c in st.session_state.kriteria},
            use_container_width=True,
            height=300
        )
        
        calc_btn = st.form_submit_button("🏁 Hitung Keputusan Akhir")
        
        if calc_btn:
            st.session_state.rating_data = edited_df
            st.session_state.step = 3
            st.rerun()

# LOGIKA STEP 3 (HASIL AKHIR & DETAIL)
elif st.session_state.step == 3:
    st.balloons()
    st.subheader("🏆 Hasil Rekomendasi & Detail Perhitungan")
    
    # --- PROSES PERHITUNGAN DI SINI ---
    
    # 1. Ambil Matriks Keputusan (Raw Data)
    raw_df = st.session_state.rating_data
    
    # 2. Hitung Matriks Ternormalisasi
    norm_df = raw_df.copy()
    for col in raw_df.columns:
        # Membagi setiap nilai dengan jumlah total kolom tersebut
        norm_df[col] = raw_df[col] / raw_df[col].sum()

    # 3. Hitung Skor Akhir (Dot Product)
    final_scores = np.dot(norm_df.values, st.session_state.bobot_kriteria)
    
    # 4. Buat DataFrame Hasil Akhir
    df_res = pd.DataFrame({
        'Alternatif': st.session_state.alternatif,
        'Skor Akhir': final_scores
    })
    
    # Urutkan Ranking
    df_res = df_res.sort_values(by='Skor Akhir', ascending=False).reset_index(drop=True)
    df_res.index += 1
    
    # --- TAMPILAN MENGGUNAKAN TABS ---
    
    tab1, tab2, tab3 = st.tabs(["🥇 Hasil Perangkingan", "📊 Matriks Ternormalisasi", "📝 Matriks Keputusan Awal"])
    
    with tab1:
        st.success(f"Rekomendasi Terbaik: **{df_res.iloc[0]['Alternatif']}**")
        st.dataframe(
            df_res.style
            .format({'Skor Akhir': '{:.4f}'})
            .highlight_max(subset=['Skor Akhir'], color='#b2fab4', axis=0),
            use_container_width=True
        )
        
        if st.button("🔄 Ulangi dari Awal"):
            st.session_state.step = 0
            st.rerun()

    with tab2:
        st.write("Nilai alternatif setelah dibagi dengan total kolom masing-masing kriteria.")
        st.dataframe(norm_df.style.format("{:.4f}").background_gradient(cmap="Blues"), use_container_width=True)
        
    with tab3:
        st.write("Nilai input asli (skala 1-10) yang Anda masukkan.")
        st.dataframe(raw_df, use_container_width=True)