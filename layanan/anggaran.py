# layanan/anggaran.py

from config import ANGGARAN_WASPADA, ANGGARAN_MELEBIHI

def hitung_status_anggaran(terpakai, anggaran):
    persen = round((terpakai / anggaran) * 100, 1)
    
    if persen > ANGGARAN_MELEBIHI:
        status = "melebihi"
    elif persen >= ANGGARAN_WASPADA:
        status = "waspada"
    else:
        status = "aman"
        
    return persen, status
