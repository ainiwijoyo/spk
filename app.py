import streamlit as st
import pandas as pd
from pymongo import MongoClient

# Koneksi ke db
client = MongoClient("mongodb://localhost:27017")
db = client["mydatabase"]
collection = db["spkdss"]

# Mengambil data dari database
data = list(collection.find())
df = pd.DataFrame(data)

# Menghapus kolom _id
df.drop(columns=["_id"], inplace=True)

def show_table():
    st.title("Data Mahasiswa")
    df.columns = df.columns.str.replace("_", " ").str.title()
    st.dataframe(df)

# Tampilan menu
menu = ["Home", "Tambah Data", "Tampilkan Data"]
pilihan = st.sidebar.selectbox("Pilih menu", menu)

if pilihan == "Home":
    show_table()
    st.subheader("Analisis Data")
    st.write("Klik 'Analisis' untuk menganalisis data")

    if st.button("Analisis"):
        # Tambahkan logika analisis di sini
        pass

elif pilihan == "Tambah Data":
    st.header("Tambah Data")
    # Tambahkan form tambah data di sini
    pass

elif pilihan == "Tampilkan Data":
    st.header("Tampilkan Data")
    # Tambahkan tampilan data di sini
    pass
