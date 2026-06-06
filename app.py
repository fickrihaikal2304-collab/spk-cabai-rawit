import streamlit as st
import pandas as pd

# =====================================
# KONFIGURASI HALAMAN
# =====================================

st.set_page_config(
    page_title="SPK Penentuan Waktu Tanam Cabai Rawit",
    page_icon="🌶️",
    layout="wide"
)

# =====================================
# CSS CUSTOM
# =====================================

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.kpi-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    text-align:center;
}

.big-title {
    text-align:center;
    color:#c62828;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# DATA PREDIKSI
# =====================================

data_prediksi = {
    "Pancor":[34945,50261,59072,65256,70877,71979,64597,60665,59525,52333,50465,49932],
    "Aikmel":[35380,44202,56032,66030,69530,69942,67212,64764,63945,60257,51070,49545],
    "Paok Motong":[40567,53985,61639,70014,75063,76512,74365,65670,58315,52094,46407,42126],
    "Sakra":[34238,46429,59489,64487,66233,66401,64098,62493,60187,54090,50113,48637]
}

# =====================================
# SIDEBAR
# =====================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/2909/2909764.png",
    width=120
)

st.sidebar.title("🌶️ SPK Cabai Rawit")

menu = st.sidebar.radio(
    "Menu Navigasi",
    [
        "Dashboard",
        "Analisis Harga",
        "Rekomendasi Waktu Tanam",
        "Tentang Sistem"
    ]
)

# =====================================
# DASHBOARD
# =====================================

if menu == "Dashboard":

    st.markdown(
        "<h1 class='big-title'>🌶️ Sistem Pendukung Keputusan Penentuan Waktu Tanam Cabai Rawit</h1>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    jumlah_pasar = len(data_prediksi)

    harga_tertinggi = 0
    pasar_tertinggi = ""

    for pasar, harga in data_prediksi.items():

        if max(harga) > harga_tertinggi:
            harga_tertinggi = max(harga)
            pasar_tertinggi = pasar

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📍 Jumlah Pasar",
            jumlah_pasar
        )

    with col2:
        st.metric(
            "💰 Harga Prediksi Tertinggi",
            f"Rp {harga_tertinggi:,.0f}"
        )

    with col3:
        st.metric(
            "🏆 Pasar Tertinggi",
            pasar_tertinggi
        )

    st.markdown("---")

    st.subheader("Tujuan Sistem")

    st.info(
        """
        Sistem ini membantu petani dalam menentukan waktu tanam cabai rawit
        yang optimal berdasarkan hasil prediksi harga selama 12 minggu ke depan.

        Sistem memanfaatkan model Random Forest untuk menghasilkan prediksi
        harga dan memberikan rekomendasi waktu tanam yang lebih menguntungkan.
        """
    )

# =====================================
# ANALISIS HARGA
# =====================================

elif menu == "Analisis Harga":

    st.title("📈 Analisis Prediksi Harga")

    pasar = st.selectbox(
        "Pilih Pasar",
        list(data_prediksi.keys())
    )

    prediksi = data_prediksi[pasar]

    df = pd.DataFrame({
        "Minggu": range(1,13),
        "Prediksi Harga (Rp)": prediksi
    })

    st.subheader(f"Prediksi Harga Pasar {pasar}")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("Grafik Prediksi Harga")

    st.line_chart(
        df.set_index("Minggu")
    )

    harga_puncak = max(prediksi)
    minggu_puncak = prediksi.index(harga_puncak) + 1

    st.success(
        f"Harga tertinggi diprediksi sebesar Rp {harga_puncak:,.0f} pada minggu ke-{minggu_puncak}"
    )

# =====================================
# REKOMENDASI TANAM
# =====================================

elif menu == "Rekomendasi Waktu Tanam":

    st.title("🌱 Rekomendasi Waktu Tanam")

    pasar = st.selectbox(
        "Pilih Pasar",
        list(data_prediksi.keys())
    )

    prediksi = data_prediksi[pasar]

    harga_puncak = max(prediksi)
    minggu_puncak = prediksi.index(harga_puncak) + 1

    st.subheader("Hasil Analisis")

    st.success(
        f"Harga tertinggi di pasar {pasar} diperkirakan terjadi pada minggu ke-{minggu_puncak}"
    )

    st.metric(
        "Harga Puncak",
        f"Rp {harga_puncak:,.0f}"
    )

    st.info(
        f"""
        Berdasarkan hasil prediksi, harga tertinggi diperkirakan terjadi pada minggu ke-{minggu_puncak}.

        Dengan asumsi masa budidaya cabai rawit ±10 minggu,
        maka petani disarankan mulai melakukan penanaman sekitar
        10 minggu sebelum periode harga puncak agar panen
        bertepatan dengan kondisi harga yang tinggi.
        """
    )

# =====================================
# TENTANG SISTEM
# =====================================

elif menu == "Tentang Sistem":

    st.title("ℹ️ Tentang Sistem")

    st.markdown("""
    ### Sistem Pendukung Keputusan Penentuan Waktu Tanam Cabai Rawit

    Sistem ini dikembangkan untuk membantu petani menentukan
    waktu tanam yang optimal berdasarkan prediksi harga cabai rawit.

    ### Data Pasar
    - Pancor
    - Aikmel
    - Paok Motong
    - Sakra

    ### Metode Prediksi
    Random Forest Regressor

    ### Output Sistem
    - Prediksi harga 12 minggu
    - Analisis harga puncak
    - Rekomendasi waktu tanam
    """)