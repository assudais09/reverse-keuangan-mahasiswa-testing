
import unittest
import json
import os
import tempfile

from unittest.mock import patch
from repositori import json_repo


class TestJsonRepository(unittest.TestCase):

    # ==================================
    # PERSIAPAN TEST
    # ==================================

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

    # ==================================
    # TEST AMBIL DATA
    # ==================================

    def test_ambil_data_berhasil(self):

        data = {
            "kategori": [],
            "transaksi": [
                {
                    "id": "T001",
                    "jenis": "pemasukan",
                    "jumlah": 1000000
                }
            ]
        }

        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump(data, file)

        hasil = json_repo.ambil_data()

        self.assertEqual(hasil, data)

    def test_ambil_data_file_tidak_ditemukan(self):

        with self.assertRaises(FileNotFoundError):
            json_repo.ambil_data()

    def test_ambil_data_json_rusak(self):

        with open(self.test_file, "w", encoding="utf-8") as file:
            file.write("{data tidak valid")

        with self.assertRaises(json.JSONDecodeError):
            json_repo.ambil_data()

    # ==================================
    # TEST SIMPAN DATA
    # ==================================

    def test_simpan_data_berhasil(self):

        data = {
            "kategori": [],
            "transaksi": [
                {
                    "id": "T002",
                    "jenis": "pengeluaran",
                    "jumlah": 50000
                }
            ]
        }

        json_repo.simpan_data(data)

        with open(self.test_file, "r", encoding="utf-8") as file:
            hasil = json.load(file)

        self.assertEqual(hasil, data)

    def test_simpan_data_unicode(self):

        data = {
            "kategori": [],
            "transaksi": [
                {
                    "catatan": "Pengeluaran – kebutuhan kuliah"
                }
            ]
        }

        json_repo.simpan_data(data)

        with open(self.test_file, "r", encoding="utf-8") as file:
            isi_file = file.read()

        self.assertIn("kebutuhan kuliah", isi_file)
        self.assertIn("–", isi_file)

        hasil = json_repo.ambil_data()

        self.assertEqual(hasil, data)

    # ==================================
    # TEST SIMPAN DAN AMBIL DATA
    # ==================================

    def test_simpan_dan_ambil_data(self):

        data = {
            "kategori": [
                {
                    "nama": "Makan",
                    "jenis": "pengeluaran",
                    "anggaran": 500000
                }
            ],
            "transaksi": [
                {
                    "id": "T003",
                    "jenis": "pengeluaran",
                    "jumlah": 25000
                }
            ]
        }

        json_repo.simpan_data(data)

        hasil = json_repo.ambil_data()

        self.assertEqual(hasil, data)

    # ==================================
    # TEST MENIMPA DATA LAMA
    # ==================================

    def test_simpan_data_menimpa_data_lama(self):

        data_lama = {
            "transaksi": [{"id": "LAMA"}]
        }

        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump(data_lama, file)

        data_baru = {
            "transaksi": [{"id": "BARU"}]
        }

        json_repo.simpan_data(data_baru)

        hasil = json_repo.ambil_data()

        self.assertEqual(hasil, data_baru)


if __name__ == "__main__":
    unittest.main()
