import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu

# Load the air quality data
df = pd.read_csv('Dashboard/world_air_quality.csv', sep=";")

# Define a function to classify air quality
def classify_air_quality(value, unit):
    if unit == 'ppm':
        if value < 0.001:
            return 'Sehat'
        elif value < 0.005:
            return 'Sedang'
        elif value < 0.010:
            return 'Buruk'
        else:
            return 'Beracun'
    elif unit == 'µg/m³':
        if value < 50:
            return 'Sehat'
        elif value < 100:
            return 'Sedang'
        elif value < 150:
            return 'Buruk'
        else:
            return 'Beracun'
    return 'Tidak Diketahui'

# Classify air quality for each record
df['Klasifikasi Kualitas Udara'] = df.apply(lambda row: classify_air_quality(row['Value'], row['Unit']), axis=1)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Home", "Air Quality Monitor", "Test Sensor", "Profile"],
        icons=["house", "bar-chart", "thermometer", "person-circle"],
        menu_icon="cast",
        default_index=0,
    )

# Home page
if selected == "Home":
    st.title("Dashboard Kualitas Udara Dunia")
    st.header("Informasi Kualitas Udara")
    st.write("""
    Kualitas udara adalah ukuran seberapa bersih atau tercemarnya udara di suatu lokasi. 
    Polusi udara dapat berdampak negatif pada kesehatan manusia, hewan, dan tumbuhan.
    
    Berikut adalah klasifikasi kualitas udara berdasarkan jenis polutan:
    
    - **Sehat:** Udara bersih dan tidak berdampak negatif terhadap kesehatan.
    - **Sedang:** Udara yang kualitasnya cukup baik, tetapi mungkin sedikit berdampak pada kelompok sensitif.
    - **Buruk:** Udara tercemar dan dapat menyebabkan dampak kesehatan pada sebagian besar populasi.
    - **Beracun:** Udara sangat tercemar dan berbahaya bagi kesehatan manusia dalam jangka pendek maupun panjang.
    
    Unit pengukuran polutan udara:
    - **ppm (parts per million):** Digunakan untuk mengukur konsentrasi gas polutan.
    - **µg/m³ (micrograms per cubic meter):** Digunakan untuk mengukur konsentrasi partikel polutan.
    """)

# Air Quality Monitor page
elif selected == "Air Quality Monitor":
    st.title("Air Quality Monitor")
    
    # Sort the countries in alphabetical order
    sorted_countries = df['Country Label'].sort_values().unique()

    # Select a country
    country = st.selectbox('Pilih Negara', sorted_countries)

    # Filter data based on the selected country
    country_data = df[df['Country Label'] == country]

    # Display the data
    st.dataframe(country_data[['City', 'Location', 'Pollutant', 'Value', 'Unit', 'Klasifikasi Kualitas Udara']])

    # Display summary information
    air_quality_summary = country_data['Klasifikasi Kualitas Udara'].value_counts()
    st.write('Ringkasan Kualitas Udara:')
    st.bar_chart(air_quality_summary)

    # Select a city for more details
    city = st.selectbox('Pilih Kota', country_data['City'].unique())

    # Filter data based on the selected city
    city_data = country_data[country_data['City'] == city]

    # Display detailed information for the selected city
    st.write(f'Detail Kualitas Udara di {city}:')
    st.dataframe(city_data[['Pollutant', 'Value', 'Unit', 'Klasifikasi Kualitas Udara']])

# Test Sensor page
elif selected == "Test Sensor":
    st.title("Test Sensor")
    st.header("Masukkan Nilai Sensor Anda")

    # Input fields for sensor values
    humidity = st.number_input('Kelembaban (%)', min_value=0.0, max_value=100.0, step=0.1)
    mq135_value = st.number_input('Nilai Sensor MQ135 (ppm)', min_value=0.0, step=0.001)
    temperature = st.number_input('Suhu (°C)', min_value=-50.0, max_value=50.0, step=0.1)

    # Display the sensor values
    st.write(f"Kelembaban: {humidity}%")
    st.write(f"Nilai Sensor MQ135: {mq135_value} ppm")
    st.write(f"Suhu: {temperature} °C")

    # Classify air quality based on MQ135 sensor value
    air_quality_classification = classify_air_quality(mq135_value, 'ppm')
    st.write(f"Klasifikasi Kualitas Udara Berdasarkan Nilai Sensor MQ135: {air_quality_classification}")

# Profile page
elif selected == "Profile":
    st.title("Profile Pengembang Aplikasi")
    st.header("Pengembang 1")
    st.write("""
    Nama: Pengembang 1
    
    Peran: Data Scientist
    
    Deskripsi: Bertanggung jawab dalam analisis data dan pembuatan model prediksi kualitas udara.
    """)

    st.header("Pengembang 2")
    st.write("""
    Nama: Pengembang 2
    
    Peran: Frontend Developer
    
    Deskripsi: Bertanggung jawab dalam desain antarmuka pengguna dan pengembangan fitur interaktif.
    """)

    st.header("Pengembang 3")
    st.write("""
    Nama: Pengembang 3
    
    Peran: Backend Developer
    
    Deskripsi: Bertanggung jawab dalam pengelolaan database dan integrasi data ke dalam aplikasi.
    """)
