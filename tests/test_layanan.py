
import unittest

from layanan.ringkasan import (
    hitung_ringkasan_keuangan,
    tentukan_nasihat
)

from layanan.anggaran import hitung_status_anggaran
from utils.format import format_rupiah


# ==================================
# UNIT TEST RINGKASAN KEUANGAN
# ==================================

class TestRingkasanKeuangan(unittest.TestCase):

    def test_hitung_ringkasan_normal(self):
        transaksi = [
            {"jenis": "pemasukan", "jumlah": 1000000},
            {"jenis": "pengeluaran", "jumlah": 300000}
        ]

        hasil = hitung_ringkasan_keuangan(transaksi)

        self.assertEqual(
            hasil,
            (1000000, 300000, 700000, 70.0)
        )

    def test_tidak_ada_pemasukan(self):
        transaksi = [
            {"jenis": "pengeluaran", "jumlah": 50000}
        ]

        hasil = hitung_ringkasan_keuangan(transaksi)

        self.assertEqual(
            hasil,
            (0, 50000, -50000, 0)
        )


# ==================================
# UNIT TEST NASIHAT KEUANGAN
# ==================================

class TestNasihatKeuangan(unittest.TestCase):

    def test_tanpa_pemasukan(self):
        hasil = tentukan_nasihat(0, 0)

        self.assertEqual(
            hasil,
            "Belum ada pemasukan bulan ini."
        )

    def test_kondisi_defisit(self):
        hasil = tentukan_nasihat(1000000, -5)

        self.assertIn(
            "Pengeluaran melebihi pemasukan",
            hasil
        )

    def test_rasio_di_bawah_10(self):
        hasil = tentukan_nasihat(1000000, 5)

        self.assertIn("di bawah 10%", hasil)

    def test_rasio_antara_10_dan_20(self):
        hasil = tentukan_nasihat(1000000, 15)

        self.assertIn("Cukup baik", hasil)

    def test_rasio_minimal_20(self):
        hasil = tentukan_nasihat(1000000, 20)

        self.assertIn("Hebat", hasil)


# ==================================
# UNIT TEST ANGGARAN
# ==================================

class TestAnggaran(unittest.TestCase):

    def test_anggaran_aman(self):
        hasil = hitung_status_anggaran(79000, 100000)

        self.assertEqual(hasil, (79.0, "aman"))

    def test_anggaran_waspada(self):
        hasil = hitung_status_anggaran(80000, 100000)

        self.assertEqual(hasil, (80.0, "waspada"))

    def test_anggaran_batas_100_persen(self):
        hasil = hitung_status_anggaran(100000, 100000)

        self.assertEqual(hasil, (100.0, "waspada"))

    def test_anggaran_melebihi(self):
        hasil = hitung_status_anggaran(110000, 100000)

        self.assertEqual(hasil, (110.0, "melebihi"))


# ==================================
# UNIT TEST FORMAT RUPIAH
# ==================================

class TestFormatRupiah(unittest.TestCase):

    def test_format_rupiah(self):
        hasil = format_rupiah(1500000)

        self.assertEqual(hasil, "Rp 1.500.000")

    def test_format_rupiah_nol(self):
        hasil = format_rupiah(0)

        self.assertEqual(hasil, "Rp 0")


if __name__ == "__main__":
    unittest.main()
