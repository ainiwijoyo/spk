import streamlit as st
import pandas as pd
from pymongo import MongoClient

# Koneksi ke db
client = MongoClient("mongodb://localhost:27017")
db = client["mydatabase"]
collection = db["spkdss"]

# Mengambil data dari database
data = list(collection.find()) #konversi ke list
df = pd.DataFrame(data) #buat df

# Menghapus kolom _id
df.drop(columns=["_id"], inplace=True, errors="ignore")
#lakukan perubahan langsung tanpa membuat salinan baru

def show_table():
    st.title("Data Mahasiswa")

    df.columns = df.columns.str.replace("_", " ").str.title()

    st.dataframe(df)


def normalisasi_matriks(R):
    # Mencari nilai maksimum tiap kolom
    maksimum = R.max(axis=0)

    # Normalisasi matriks R simpan ke var R_norm
    R_norm = R / maksimum

    #kembalikan nilai R_norm
    return R_norm

def tambah_data(nama, tes_bahasa_inggris, tes_kemampuan_dasar, tes_psikologi, tes_buta_warna):
    if nama:
        data = {
            "nama": nama,
            "tes_bahasa_inggris": tes_bahasa_inggris,
            "tes_kemampuan_dasar": tes_kemampuan_dasar,
            "tes_psikologi": tes_psikologi,
            "tes_buta_warna": tes_buta_warna
        }
        collection.insert_one(data)
        st.success("Data berhasil ditambahkan")
    else:
        st.warning("Nama harus diisi!")

def tampilkan_data():
    st.header("Tampilkan Data")

    # Tampilkan form pencarian berdasarkan nama di sidebar
    search_term = st.sidebar.text_input("Cari berdasarkan nama")

    # pencarian nama
    if search_term:
        data = list(collection.find({"nama": {"$regex": search_term, "$options": "i"}}))
    else:
        data = list(collection.find())

    # urutkan baru ke lama
    data.reverse()

    st.subheader("Data:")

    if len(data) > 0:
        # Tampilkan data
        for i, item in enumerate(data):
            nama = st.text_input("Nama", item["nama"], key=f"nama_{i}")
            tes_bahasa_inggris = st.number_input("Tes Bahasa Inggris", min_value=0, max_value=100, value=item["tes_bahasa_inggris"], key=f"bahasa_inggris_{i}")
            tes_kemampuan_dasar = st.number_input("Tes Kemampuan Dasar", min_value=0, max_value=100, value=item["tes_kemampuan_dasar"], key=f"kemampuan_dasar_{i}")
            tes_psikologi = st.number_input("Tes Psikologi", min_value=0, max_value=100, value=item["tes_psikologi"], key=f"psikologi_{i}")
            tes_buta_warna = st.number_input("Tes Buta Warna", min_value=0, max_value=100, value=item["tes_buta_warna"], key=f"buta_warna_{i}")
            
            if st.button("Perbarui", key=f"perbarui_{i}"):
                update_data(item["_id"], nama, tes_bahasa_inggris, tes_kemampuan_dasar, tes_psikologi, tes_buta_warna)
            if st.button("Hapus", key=f"hapus_{i}"):
                hapus_data(item["_id"])
            st.write("---")
    else:
        st.write("Data tidak ditemukan")

def update_data(id, nama, tes_bahasa_inggris, tes_kemampuan_dasar, tes_psikologi, tes_buta_warna):
    if nama:
        collection.update_one({"_id": id}, {"$set": {
            "nama": nama,
            "tes_bahasa_inggris": tes_bahasa_inggris,
            "tes_kemampuan_dasar": tes_kemampuan_dasar,
            "tes_psikologi": tes_psikologi,
            "tes_buta_warna": tes_buta_warna
        }})
        st.success("Data berhasil diperbarui")
    else:
        st.warning("Nama harus diisi!")
        
def hapus_data(id):
    query = {"_id": id}
    collection.delete_one(query)
    st.success("Data berhasil dihapus")

# Tampilan menu
menu = ["Home", "Tambah Data", "Tampilkan Data"]
pilihan = st.sidebar.selectbox("Pilih menu", menu)

if pilihan == "Home":
    show_table()
    st.subheader("Analisis Data")
    st.write("Klik 'Analisis' untuk menganalisis data")

    if st.button("Analisis"):
        # Mengambil data tes
        tes_cols = ["Tes Kemampuan Dasar", "Tes Buta Warna", "Tes Bahasa Inggris", "Tes Psikologi"]
        tes = df[tes_cols].values

        # Normalisasi matriks tes
        tes_norm = normalisasi_matriks(tes) #panggil fungsi R

        # Bobot kriteria
        bobot_kemampuan_dasar = 0.35
        bobot_buta_warna = 0.3
        bobot_bahasa_inggris = 0.1
        bobot_psikologi = 0.25

        # Menghitung nilai preferensi V (simpan ke var V)
        V = (
            bobot_kemampuan_dasar * tes_norm[:, 0]
            + bobot_buta_warna * tes_norm[:, 1]
            + bobot_bahasa_inggris * tes_norm[:, 2]
            + bobot_psikologi * tes_norm[:, 3]
        )

        # Menambah kolom skor pada dataframe
        df["Skor"] = V

        # Mengurutkan data berdasarkan skor
        df = df.sort_values("Skor", ascending=False)

        # Tampilkan 3 mahasiswa terbaik
        st.subheader("Hasil Analisis:")
        st.dataframe(df.head(3).reset_index(drop=True))


elif pilihan == "Tambah Data":
    st.header("Tambah Data")
    nama = st.text_input("Nama")
    tes_bahasa_inggris = st.number_input("Tes Bahasa Inggris", min_value=0, max_value=100)
    tes_kemampuan_dasar = st.number_input("Tes Kemampuan Dasar", min_value=0, max_value=100)
    tes_psikologi = st.number_input("Tes Psikologi", min_value=0, max_value=100)
    tes_buta_warna = st.number_input("Tes Buta Warna", min_value=0, max_value=100)
    
    if st.button("Tambah"):
        tambah_data(nama, tes_bahasa_inggris, tes_kemampuan_dasar, tes_psikologi, tes_buta_warna)

elif pilihan == "Tampilkan Data":
    tampilkan_data()
