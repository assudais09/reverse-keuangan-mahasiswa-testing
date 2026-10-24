# layanan/ringkasan.py

from config import RASIO_DEFISIT, RASIO_KRITIS, RASIO_IDEAL

def hitung_ringkasan_keuangan(transaksi_bulan_ini):
    pemasukan = sum(t["jumlah"] for t in transaksi_bulan_ini if t["jenis"] == "pemasukan")
    pengeluaran = sum(t["jumlah"] for t in transaksi_bulan_ini if t["jenis"] == "pengeluaran")
    selisih = pemasukan - pengeluaran
    
    # Rasio tabungan = selisih / pemasukan * 100 (1 desimal)
    rasio = round((selisih / pemasukan) * 100, 1) if pemasukan > 0 else 0
    
    return pemasukan, pengeluaran, selisih, rasio

def tentukan_nasihat(pemasukan, rasio):
    if pemasukan == 0:
        return "Belum ada pemasukan bulan ini."
    elif rasio < RASIO_DEFISIT:
        return "Pengeluaran melebihi pemasukan! Tinjau ulang kategori yang berstatus melebihi."
    elif rasio < RASIO_KRITIS:
        return "Rasio tabungan di bawah 10%. Coba sisihkan di awal bulan."
    elif rasio < RASIO_IDEAL:
        return "Cukup baik. Target ideal tabungan 20% dari pemasukan."
    else:
        return "Hebat! Tabungan Anda di atas 20%."
