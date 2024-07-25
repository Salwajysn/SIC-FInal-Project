import streamlit as st
import pandas as pd
import altair as alt
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

# Define health tips based on air quality classification
def get_health_tips(classification):
    if classification in ['Sehat', 'Sedang']:
        return """
        **Tips untuk menjaga kesehatan**
        - **Tetaplah berolahraga secara teratur:** Aktivitas fisik dapat membantu menjaga kesehatan jantung dan paru-paru.
        - **Konsumsi makanan bergizi:** Pastikan untuk mengonsumsi makanan yang seimbang dan kaya nutrisi untuk memperkuat sistem kekebalan tubuh.
        - **Hindari merokok dan paparan asap rokok:** Hindari kebiasaan merokok dan paparan asap rokok untuk menjaga kesehatan paru-paru.
        - **Jaga pola tidur yang baik:** Tidur yang cukup dan berkualitas penting untuk pemulihan tubuh dan kesehatan secara keseluruhan.
        - **Rutin lakukan pemeriksaan kesehatan:** Pemeriksaan kesehatan secara berkala dapat membantu mendeteksi masalah kesehatan sejak dini.
        - **Pertahankan hidrasi yang baik:** Minum cukup air setiap hari untuk menjaga fungsi tubuh dan kesehatan kulit.
        - **Berjemur di bawah sinar matahari:** Paparan sinar matahari pagi membantu tubuh memproduksi vitamin D yang penting untuk kesehatan tulang dan sistem kekebalan tubuh.
        - **Kurangi stres:** Lakukan aktivitas yang Anda nikmati untuk mengurangi stres dan menjaga keseimbangan mental.
        """
    elif classification in ['Buruk', 'Beracun']:
        return """
        **Dampak kesehatan dari kualitas udara buruk**
        - Dapat menyebabkan masalah pernapasan seperti asma dan bronkitis.
        - Meningkatkan risiko penyakit jantung dan paru-paru.
        - Mengurangi kapasitas paru-paru dan fungsi pernapasan.
        - Meningkatkan risiko kanker paru-paru dalam jangka panjang.

        **Saran untuk Menjaga Kesehatan**
        - **Gunakan masker pelindung:** Saat kualitas udara sangat buruk, gunakan masker dengan filter HEPA untuk melindungi saluran pernapasan.
        - **Batasi aktivitas luar ruangan:** Kurangi waktu di luar ruangan, terutama pada saat kualitas udara sangat buruk.
        - **Gunakan pembersih udara:** Pertimbangkan menggunakan pembersih udara di dalam ruangan untuk mengurangi paparan polusi udara.
        - **Perbanyak konsumsi makanan kaya antioksidan:** Makanan seperti buah-buahan dan sayuran dapat membantu melawan dampak polusi udara pada tubuh.
        - **Hidrasi yang baik:** Minum cukup air untuk membantu tubuh dalam proses detoksifikasi.

        """
    return ""

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Home", "Air Quality Monitor", "Test Sensor", "Air Quality Check", "Profile"],
        icons=["house", "bar-chart", "thermometer", "cloud", "person-circle"],
        menu_icon="cast",
        default_index=0,
    )

# Home page
if selected == "Home":
    st.title("Air Quality Monitoring Sensing for Healthier People")
    
    # Input for user name
    user_name = st.text_input("Masukkan Nama Kamu")
    
    if user_name:
        # Display welcome message with larger font and blue color
        st.markdown(f"""
        <h3>Selamat datang, <span style="color: blue;">{user_name}</span>! ✨</h3>
        <p style="font-size: 20px;">Silakan lihat informasi tentang kualitas udara di bawah ini.</p>
        """, unsafe_allow_html=True)
    
    # Display air quality information
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

    st.write("")  # Menambahkan paragraf kosong
    st.write("")  # Menambahkan paragraf kosong

    # Create an interactive chart for air quality
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Country Label:O', sort=None),
        y='count():Q',
        color='Klasifikasi Kualitas Udara:N',
        tooltip=['Country Label:N', 'count():Q', 'Klasifikasi Kualitas Udara:N']
    ).properties(
        title='Jumlah Data Kualitas Udara Berdasarkan Negara'
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

    # Determine the healthiest and most polluted countries
    summary = df.groupby('Country Label').agg(
        Average_Value=('Value', 'mean'),
        Classification=('Klasifikasi Kualitas Udara', lambda x: x.mode()[0])
    ).reset_index()

    st.write(f"### Negara dengan Kualitas Udara Terbaik")
    st.write(f"- **Deskripsi:** Negara yang memiliki rata-rata nilai polutan yang paling rendah, menunjukkan kualitas udara yang sangat baik. Faktor-faktor yang mungkin berkontribusi pada kualitas udara yang baik termasuk kebijakan lingkungan yang ketat, rendahnya tingkat industri polutan, dan praktik konservasi yang baik.")

    st.write(f"### Negara dengan Kualitas Udara Paling Beracun")
    st.write(f"- **Deskripsi:** Negara yang memiliki rata-rata nilai polutan yang tertinggi, menunjukkan kualitas udara yang sangat buruk. Faktor-faktor yang mungkin berkontribusi termasuk tingkat polusi industri yang tinggi, penggunaan kendaraan bermotor yang besar, dan kurangnya regulasi lingkungan yang efektif.")

# Air Quality Monitor page
elif selected == "Air Quality Monitor":
    st.title("World Air Quality Monitor")
    
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
    st.header("Masukkan Nilai Sensor")

    # Input fields for sensor values
    humidity = st.number_input('Kelembaban (%)', min_value=0.0, max_value=100.0, step=0.1)
    mq135_value = st.number_input('Nilai Sensor MQ135 (ppm)', min_value=0.0, step=0.001)
    temperature = st.number_input('Suhu (°C)', min_value=0.0, max_value=60.0, step=0.1)

    if st.button('Submit'):
        # Display the sensor values
        st.write(f"Kelembaban: {humidity}%")
        st.write(f"Nilai Sensor MQ135: {mq135_value} ppm")
        st.write(f"Suhu: {temperature} °C")

        # Classify air quality based on MQ135 sensor value
        air_quality_classification = classify_air_quality(mq135_value, 'ppm')

        # Display classification result with a brief introduction
        st.write(f"Klasifikasi Kualitas Udara Berdasarkan Nilai Sensor MQ135: {air_quality_classification}")

        st.write("")  # Menambahkan paragraf kosong

        if air_quality_classification in ['Sehat', 'Sedang']:
            st.write(f"Berdasarkan hasil pengukuran sensor, kualitas udara saat ini adalah {air_quality_classification}.")
            st.write("Untuk menjaga kesehatan, berikut beberapa tips yang bisa Anda lakukan:")
        elif air_quality_classification in ['Buruk', 'Beracun']:
            st.write(f"Berdasarkan hasil pengukuran sensor, kualitas udara saat ini menunjukkan kondisi {air_quality_classification}.")
            st.write("Berikut dampak kesehatan dari kualitas udara tersebut:")

        st.write("")  # Menambahkan paragraf kosong

        # Display health tips or impacts based on air quality classification
        health_tips = get_health_tips(air_quality_classification)
        st.write(health_tips)

# Air Quality Check page
elif selected == "Air Quality Check":
    st.title("Air Quality Check")
    st.header("Periksa Kualitas Udara di Daerah Anda")

    # Select a country
    country = st.selectbox('Pilih Negara', df['Country Label'].sort_values().unique())

    # Input for user name
    user_name = st.text_input('Masukkan Nama Kamu')

    if st.button('Submit'):
        # Simulate fetching data from a database
        # For demonstration, we'll use the dataset to get air quality information
        country_data = df[df['Country Label'] == country]

        if not country_data.empty:
            # Assume we get the average air quality value from the database
            average_value = country_data['Value'].mean()
            average_unit = country_data['Unit'].iloc[0]  # Assume unit is the same for all

            air_quality_classification = classify_air_quality(average_value, average_unit)

            st.write(f"Hasil kualitas udara menunjukkan bahwa kualitas udara di {country} adalah {air_quality_classification}.")

            if air_quality_classification in ['Sehat', 'Sedang']:
                st.write(f"Berdasarkan hasil tersebut, ada beberapa hal yang bisa Anda lakukan, {user_name}, untuk tetap menjaga kesehatan:")
                st.write("")  # Menambahkan paragraf kosong
                health_tips = get_health_tips(air_quality_classification)
                st.write(health_tips)
            elif air_quality_classification in ['Buruk', 'Beracun']:
                st.write(f"Berdasarkan hasil tersebut, kualitas udara di {country} menunjukkan kondisi yang berbahaya, {user_name}. Berikut dampak kesehatan dari kualitas udara tersebut:")
                st.write("")  # Menambahkan paragraf kosong
                health_tips = get_health_tips(air_quality_classification)
                st.write(health_tips)
        else:
            st.write("Data untuk negara yang dipilih tidak tersedia.")


# Profile page
elif selected == "Profile":
    st.title("Profile Pengembang Aplikasi")
    st.header("Pengembang 1 👩🏻‍💻")
    st.write("""
    Nama: Adinda Rizki Sya'bana Diva
    
    Peran: Data Scientist
             
    Deskripsi: Bertanggung jawab dalam analisis data dan pembuatan model prediksi kualitas udara.
    """)

    st.header("Pengembang 2 👩🏻‍💻")
    st.write("""
    Nama: Salwa Nafisa
             
    Peran: Frontend Developer
             
    Deskripsi: Bertanggung jawab dalam desain antarmuka pengguna dan pengembangan fitur interaktif.
    """)

    st.header("Pengembang 3 👨🏻‍💻")
    st.write("""
    Nama: Rahman Ilyas Alkahfi
             
    Peran: Backend Developer
             
    Deskripsi: Bertanggung jawab dalam pengelolaan database dan integrasi data ke dalam aplikasi.
    """)


