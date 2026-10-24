# utils/format.py

def format_rupiah(angka):
    """Mengubah angka (int) menjadi string format rupiah, contoh: Rp 1.500.000"""
    return "Rp {:,}".format(angka).replace(",", ".")
