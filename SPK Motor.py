import streamlit as st
import pandas as pd
import numpy as np

st.title("Sistem Pendukung Keputusan Pemilihan Sepeda Motor")
st.subheader("Metode: Simple Additive Weighting (SAW)")

st.write("Silakan isi preferensi Anda terhadap motor yang diinginkan, lalu klik tombol Submit.")

# Form input dengan tombol Submit
with st.form("input_form"):
    harga_max = st.number_input("1. Berapa harga maksimal motor yang Anda inginkan? (dalam Rp juta)", min_value=10.0, max_value=50.0, value=30.0, step=0.5)
    min_konsumsi = st.number_input("2. Berapa konsumsi bahan bakar minimal yang Anda inginkan? (km/liter)", min_value=30, max_value=70, value=45)
    min_kapasitas = st.number_input("3. Berapa kapasitas mesin minimal yang Anda inginkan? (cc)", min_value=100, max_value=200, value=125)
    desain = st.slider("4. Seberapa penting desain/tampilan bagi Anda?", 1, 5, 3)
    tanki_min = st.number_input("5. Berapa kapasitas tangki minimal yang Anda inginkan? (liter)", min_value=3.0, max_value=6.0, value=4.0)
    fitur = st.slider("6. Seberapa penting fitur keselamatan (ABS, CBS, dll)?", 1, 5, 3)

    submitted = st.form_submit_button("Submit")

if submitted:
    # Data Alternatif (Harga diubah dari ribu ke juta)
    data = {
        'Alternatif': ['Honda Vario 160', 'Yamaha NMAX', 'Suzuki Avenis', 'Honda Beat Street', 'Yamaha Aerox'],
        'C1': [26.0, 32.0, 24.0, 19.0, 29.0],  # Harga (Rp juta)
        'C2': [46, 40, 54, 60, 45],            # Konsumsi (km/l)
        'C3': [160, 155, 125, 110, 155],       # Kapasitas Mesin (cc)
        'C4': [4, 5, 3, 4, 5],                 # Desain (skala)
        'C5': [5.5, 7.1, 5.2, 4.0, 4.5],       # Tangki (L)
        'C6': [5, 5, 4, 3, 4]                  # Fitur keselamatan (skala)
    }

    df = pd.DataFrame(data)

    # Bobot kriteria
    weights = np.array([0.25, 0.20, 0.15, 0.15, 0.10, 0.15])
    cost_criteria = [True, False, False, False, False, False]  # True jika cost

    # Normalisasi
    normalized_df = df.copy()
    for i, col in enumerate(['C1', 'C2', 'C3', 'C4', 'C5', 'C6']):
        if cost_criteria[i]:
            normalized_df[col] = df[col].min() / df[col]
        else:
            normalized_df[col] = df[col] / df[col].max()

    # Hitung skor SAW
    scores = normalized_df[['C1', 'C2', 'C3', 'C4', 'C5', 'C6']].values @ weights
    df['Skor SAW'] = scores

    # Filter berdasarkan preferensi user (saringan awal)
    filtered_df = df[
        (df['C1'] <= harga_max) &
        (df['C2'] >= min_konsumsi) &
        (df['C3'] >= min_kapasitas) &
        (df['C4'] >= desain) &
        (df['C5'] >= tanki_min) &
        (df['C6'] >= fitur)
    ]

    # Tampilkan hasil
    st.subheader("Rekomendasi Motor Berdasarkan Preferensi Anda:")
    if not filtered_df.empty:
        hasil = filtered_df.sort_values(by='Skor SAW', ascending=False).reset_index(drop=True)
        st.dataframe(hasil[['Alternatif', 'Skor SAW']])
    else:
        st.warning("Tidak ada motor yang sesuai dengan preferensi Anda.")
