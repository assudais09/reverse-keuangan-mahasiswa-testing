import json
from config import DATA_FILE

def ambil_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)

def simpan_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
