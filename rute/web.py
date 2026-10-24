from flask import Blueprint, request, render_template, redirect, Response
import datetime
from repositori.json_repo import ambil_data, simpan_data
from layanan.ringkasan import hitung_ringkasan_keuangan, tentukan_nasihat
from layanan.anggaran import hitung_status_anggaran
from utils.format import format_rupiah

web_bp = Blueprint('web', __name__)

@web_bp.route("/")
def index():
    data = ambil_data()
    bulan = request.args.get("bulan", datetime.date.today().strftime("%Y-%m"))
    transaksi = [t for t in data["transaksi"] if t["tanggal"][:7] == bulan]
    
    # Panggil layanan bisnis
    pemasukan, pengeluaran, selisih, rasio = hitung_ringkasan_keuangan(transaksi)
    nasihat = tentukan_nasihat(pemasukan, rasio)
    
    anggaran = []
    for k in data["kategori"]:
        if k["jenis"] == "pengeluaran" and k["anggaran"] > 0:
            terpakai = sum(t["jumlah"] for t in transaksi if t["kategori"] == k["nama"] and t["jenis"] == "pengeluaran")
            persen, status = hitung_status_anggaran(terpakai, k["anggaran"])
            anggaran.append({
                "kategori": k["nama"], 
                "terpakai": format_rupiah(terpakai),
                "anggaran": format_rupiah(k["anggaran"]), 
                "persen": str(persen) + "%", 
                "status": status
            })
            
    for t in transaksi:
        t["tampil"] = ("+" if t["jenis"] == "pemasukan" else "-") + format_rupiah(t["jumlah"])
        
    return render_template("index.html", bulan=bulan, transaksi=transaksi, kategori=data["kategori"], 
                           anggaran=anggaran, nasihat=nasihat,
                           pemasukan=format_rupiah(pemasukan), pengeluaran=format_rupiah(pengeluaran),
                           selisih=format_rupiah(selisih), rasio=rasio, pesan=request.args.get("pesan", ""))

@web_bp.route("/tambah", methods=["POST"])
def tambah():
    data = ambil_data()
    tanggal = request.form.get("tanggal", "")
    jenis = request.form.get("jenis", "")
    kategori = request.form.get("kategori", "")
    try:
        jumlah = int(request.form.get("jumlah", "0"))
    except ValueError:
        jumlah = 0
        
    kat = [k for k in data["kategori"] if k["nama"] == kategori]
    if jumlah <= 0:
        return redirect("/?pesan=Jumlah harus lebih dari 0")
    if len(kat) == 0 or kat[0]["jenis"] != jenis:
        return redirect("/?pesan=Kategori tidak sesuai jenis transaksi")
        
    nomor = max([int(t["id"][1:]) for t in data["transaksi"]] + [0]) + 1
    baru = {"id": "T" + str(nomor).zfill(3), "tanggal": tanggal, "jenis": jenis, "kategori": kategori, "jumlah": jumlah, "catatan": request.form.get("catatan", "")}
    data["transaksi"].append(baru)
    
    simpan_data(data)
    return redirect("/?bulan=" + tanggal[:7])

@web_bp.route("/export.csv")
def export_csv():
    data = ambil_data()
    bulan = request.args.get("bulan", datetime.date.today().strftime("%Y-%m"))
    isi = "id;tanggal;jenis;kategori;jumlah;catatan\n"
    for t in data["transaksi"]:
        if t["tanggal"][:7] == bulan:
            isi += ";".join([t["id"], t["tanggal"], t["jenis"], t["kategori"], str(t["jumlah"]), t["catatan"].replace(";", ",")]) + "\n"
    return Response(isi, mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=dompet-" + bulan + ".csv"})
