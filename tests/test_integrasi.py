
import unittest
import tempfile
import os

from unittest.mock import patch
from repositori import json_repo
from layanan.ringkasan import hitung_ringkasan_keuangan


class TestIntegrasiKeuangan(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.test_file = os.path.join(
            self.temp_dir.name,
            "data_test.json"
        )

        self.patcher = patch(
            "repositori.json_repo.DATA_FILE",
            self.test_file
        )

        self.patcher.start()

        self.addCleanup(self.patcher.stop)
        self.addCleanup(self.temp_dir.cleanup)

    def test_integrasi_data_dan_ringkasan(self):

        data = {
            "kategori": [],
            "transaksi": [
                {
                    "jenis": "pemasukan",
                    "jumlah": 1000000
                },
                {
                    "jenis": "pengeluaran",
                    "jumlah": 300000
                }
            ]
        }

        # Menyimpan data
        json_repo.simpan_data(data)

        # Membaca data dari repository
        data_tersimpan = json_repo.ambil_data()

        # Menghitung ringkasan dari data yang dibaca
        hasil = hitung_ringkasan_keuangan(
            data_tersimpan["transaksi"]
        )

        # Memastikan hasil integrasi benar
        self.assertEqual(
            hasil,
            (1000000, 300000, 700000, 70.0)
        )


if __name__ == "__main__":
    unittest.main()
