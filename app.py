import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================

st.set_page_config(
    page_title="SPK Penentuan Waktu Tanam Cabai Rawit",
    page_icon="🌶️",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

[data-testid="stSidebar"] {
    background-color: #B71C1C;
}

[data-testid="stSidebar"] * {
    color: white;
}

.main-title {
    text-align:center;
    color:#B71C1C;
    font-size:40px;
    font-weight:bold;
}

.sub-title {
    text-align:center;
    color:gray;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# DATA PREDIKSI
# =====================================================

data_prediksi = {
    "Pancor":[34945,50261,59072,65256,70877,71979,64597,60665,59525,52333,50465,49932],
    "Aikmel":[35380,44202,56032,66030,69530,69942,67212,64764,63945,60257,51070,49545],
    "Paok Motong":[40567,53985,61639,70014,75063,76512,74365,65670,58315,52094,46407,42126],
    "Sakra":[34238,46429,59489,64487,66233,66401,64098,62493,60187,54090,50113,48637]
}

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🌶️ SPK Cabai Rawit")

menu = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Analisis Harga",
        "Peta Spasial",
        "Rekomendasi Waktu Tanam",
        "Tentang Sistem"
    ]
)

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.markdown(
        """
        <div class='main-title'>
        🌶️ Sistem Pendukung Keputusan
        Penentuan Waktu Tanam Cabai Rawit
        </div>

        <div class='sub-title'>
        Berbasis Prediksi Harga Cabai Rawit
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    harga_tertinggi = 0
    pasar_tertinggi = ""

    for pasar, harga in data_prediksi.items():

        if max(harga) > harga_tertinggi:
            harga_tertinggi = max(harga)
            pasar_tertinggi = pasar

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Jumlah Pasar",
            len(data_prediksi)
        )

    with col2:
        st.metric(
            "Harga Tertinggi",
            f"Rp {harga_tertinggi:,.0f}"
        )

    with col3:
        st.metric(
            "Pasar Tertinggi",
            pasar_tertinggi
        )

    st.markdown("---")

    st.info("""
    Sistem ini membantu petani menentukan waktu tanam cabai rawit
    berdasarkan prediksi harga 12 minggu ke depan menggunakan
    metode Random Forest.
    """)

# =====================================================
# ANALISIS HARGA
# =====================================================

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

    st.dataframe(
        df,
        use_container_width=True
    )

    st.line_chart(
        df.set_index("Minggu")
    )

    harga_puncak = max(prediksi)
    minggu_puncak = prediksi.index(harga_puncak) + 1

    st.success(
        f"Harga puncak diprediksi Rp {harga_puncak:,.0f} pada minggu ke-{minggu_puncak}"
    )

# =====================================================
# PETA SPASIAL
# =====================================================

elif menu == "Peta Spasial":

    st.title("🗺️ Peta Spasial Pasar Cabai Rawit")

    m = folium.Map(
        location=[-8.64, 116.52],
        zoom_start=11
    )

    data_peta = [
        ["Pancor",-8.65329,116.52276,71979],
        ["Aikmel",-8.60753,116.53173,69942],
        ["Paok Motong",-8.62293,116.52089,76512],
        ["Sakra",-8.66073,116.47507,66401]
    ]

    for pasar, lat, lon, harga in data_peta:

        folium.Marker(
            location=[lat, lon],
            popup=f"""
            <b>{pasar}</b><br>
            Harga Puncak: Rp {harga:,.0f}
            """,
            tooltip=pasar
        ).add_to(m)

    st_folium(
        m,
        width=1200,
        height=600
    )

# =====================================================
# REKOMENDASI TANAM
# =====================================================

elif menu == "Rekomendasi Waktu Tanam":

    st.title("🌱 Rekomendasi Waktu Tanam")

    pasar = st.selectbox(
        "Pilih Pasar",
        list(data_prediksi.keys())
    )

    prediksi = data_prediksi[pasar]

    harga_puncak = max(prediksi)
    minggu_puncak = prediksi.index(harga_puncak) + 1

    st.metric(
        "Harga Puncak",
        f"Rp {harga_puncak:,.0f}"
    )

    st.success(
        f"Harga tertinggi diperkirakan terjadi pada minggu ke-{minggu_puncak}"
    )

    st.info(
        f"""
        Dengan asumsi masa budidaya cabai rawit ±10 minggu,
        maka waktu tanam disarankan sekitar 10 minggu sebelum
        minggu ke-{minggu_puncak}.
        """
    )

# =====================================================
# TENTANG SISTEM
# =====================================================

elif menu == "Tentang Sistem":

    st.title("ℹ️ Tentang Sistem")

    st.markdown("""
    ### Sistem Pendukung Keputusan Penentuan Waktu Tanam Cabai Rawit

    Sistem ini dikembangkan untuk membantu petani menentukan
    waktu tanam yang optimal berdasarkan prediksi harga.

    ### Pasar yang Dianalisis
    - Pancor
    - Aikmel
    - Paok Motong
    - Sakra

    ### Metode
    Random Forest Regressor

    ### Output
    - Prediksi harga 12 minggu
    - Analisis harga puncak
    - Peta spasial pasar
    - Rekomendasi waktu tanam
    """)
