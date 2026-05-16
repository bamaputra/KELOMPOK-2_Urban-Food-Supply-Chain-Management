"""
Module 6: CLI Rantai Pasok
Implementasi perintah:
- KIRIM <dari> <ke> <kode> <jumlah>
- PROSES_KIRIM
- RUTE_MURAH <dari> <ke>
- CEK_STOK <kode>
- KADALUARSA <maks_hari>
- LAPORAN_DISTRIBUSI
- BUFFER <node>
- KELUAR
"""

import random
import time
from dataclasses import dataclass

# Import modules
from 1_graph_rantai_pasok import GraphRantaiPasok
from 2_circular_queue import CircularQueue
from 3_priority_queue import PriorityQueueKirim, Stack
from 4_bst_katalog import BSTKatalog
from 5_dijkstra_biaya import dijkstra_biaya, get_path, hitung_prioritas, prioritas_to_text


@dataclass
class Produk:
    kode: str
    nama: str
    kategori: str
    harga_satuan: float
    stok: int
    masa_kadaluarsa_hari: int




# Konstanta
KATEGORI_PRODUK = ['SAYUR', 'BUAH', 'DAGING', 'IKAN', 'BAHAN_POKOK']
TIPE_NODE = ['PETANI', 'DISTRIBUTOR', 'PASAR', 'GUDANG']



    # Inisialisasi semua komponen
    graph = GraphRantaiPasok()
    bst_katalog = BSTKatalog()
    pg_kirim = PriorityQueueKirim()
    log_transaksi = Stack()
    buffer_gudang = {}
    kirim_counter = 0

    # Generate data awal
    nodes, edges, produk_list = generate_rantai_pasok(seed=61)
    
    # Inisialisasi graph dan buffer
    for nid, tipe in nodes:
        graph.tambah_node(nid, tipe)
        buffer_gudang[nid] = CircularQueue(kapasitas=50)
    
    for u, v, j, b in edges:
        graph.tambah_jalur(u, v, j, b)
    
    for p in produk_list:
        bst_katalog.insert(p)

    # Tampilkan menu
    print('=' * 60)
    print('Food Supply Chain Management System')
    print('=' * 60)
    print('Perintah yang tersedia:')
    print('  KIRIM <dari> <ke> <kode> <jumlah>')
    print('  PROSES_KIRIM')
    print('  RUTE_MURAH <dari> <ke>')
    print('  CEK_STOK <kode>')
    print('  KADALUARSA <maks_hari>')
    print('  LAPORAN_DISTRIBUSI')
    print('  BUFFER <node>')
    print('  BANTUAN')
    print('  KELUAR')
    print('=' * 60)

    while True:
        try:
            cmd = input('\n> ').strip().split()
            if not cmd:
                continue

            if cmd[0].upper() == 'KELUAR':
                print('Terima kasih telah menggunakan sistem manajemen rantai pasok!')
                break

            elif cmd[0].upper() == 'BANTUAN':
                print('\nDaftar Perintah:')
                print('  KIRIM <dari> <ke> <kode> <jumlah> - Kirim produk dari node ke node')
                print('  PROSES_KIRIM - Proses pengiriman dengan prioritas tertinggi')
                print('  RUTE_MURAH <dari> <ke> - Cari rute termurah antara dua node')
                print('  CEK_STOK <kode> - Cek stok produk di katalog')
                print('  KADALUARSA <maks_hari> - Lihat produk dengan kadaluarsa <= maks_hari')
                print('  LAPORAN_DISTRIBUSI - Tampilkan semua transaksi pengiriman')
                print('  BUFFER <node> - Lihat isi buffer gudang suatu node')

            elif cmd[0].upper() == 'KIRIM':
                if len(cmd) != 5:
                    print('Format: KIRIM <dari> <ke> <kode> <jumlah>')
                    continue

                _, dari, ke, kode, jumlah_str = cmd
                try:
                    jumlah = int(jumlah_str)
                except ValueError:
                    print('Jumlah harus berupa angka!')
                    continue

                if dari not in graph.adj or ke not in graph.adj:
                    print('Node tidak ditemukan!')
                    continue

                produk = bst_katalog.search(kode)
                if not produk:
                    print(f'Produk dengan kode {kode} tidak ditemukan!')
                    continue

                if produk.stok < jumlah:
                    print(f'Stok tidak mencukupi! Stok tersedia: {produk.stok}')
                    continue

                # Kurangi stok
                bst_katalog.update_stok(kode, -jumlah)

                prioritas = hitung_prioritas(produk.masa_kadaluarsa_hari)
                prioritas_text = prioritas_to_text(prioritas)

                kirim_counter += 1
                pengiriman = Pengiriman(
                    pengiriman_id=kirim_counter,
                    dari_node=dari,
                    ke_node=ke,
                    kode_produk=kode,
                    jumlah=jumlah,
                    prioritas=prioritas
                )

                pg_kirim.enqueue(pengiriman)
                print(f'Pengiriman #{kirim_counter} ditambahkan ke antrian prioritas {prioritas_text}')

            elif cmd[0].upper() == 'PROSES_KIRIM':
                if pg_kirim.is_empty():
                    print('Tidak ada pengiriman dalam antrian')
                    continue

                pengiriman = pg_kirim.dequeue()
                if not pengiriman:
                    print('Gagal memproses pengiriman')
                    continue

                tipe_tujuan = graph.tipe_node.get(pengiriman.ke_node, '')
                if tipe_tujuan == 'GUDANG':
                    produk = bst_katalog.search(pengiriman.kode_produk)
                    if produk:
                        # Clone produk untuk buffer
                        produk_copy = Produk(
                            kode=produk.kode,
                            nama=produk.nama,
                            kategori=produk.kategori,
                            harga_satuan=produk.harga_satuan,
                            stok=pengiriman.jumlah,
                            masa_kadaluarsa_hari=produk.masa_kadaluarsa_hari
                        )
                        buffer_gudang[pengiriman.ke_node].enqueue(produk_copy)
                        print(f'Produk disimpan ke buffer gudang {pengiriman.ke_node}')
                else:
                    print(f'Pengiriman ke {pengiriman.ke_node} ({tipe_tujuan}) diproses')

                prioritas_text = prioritas_to_text(pengiriman.prioritas)
                log_entry = f'[ID:{pengiriman.pengiriman_id}] {pengiriman.dari_node} -> {pengiriman.ke_node} | {pengiriman.kode_produk} x{pengiriman.jumlah} | Prioritas:{prioritas_text}'
                log_transaksi.push(log_entry)

                print(f'Pengiriman #{pengiriman.pengiriman_id} diproses')

            elif cmd[0].upper() == 'RUTE_MURAH':
                if len(cmd) != 3:
                    print('Format: RUTE_MURAH <dari> <ke>')
                    continue

                _, dari, ke = cmd

                if dari not in graph.adj or ke not in graph.adj:
                    print('Node tidak ditemukan!')
                    continue

                dist, parent = dijkstra_biaya(graph, dari)

                if dist[ke] == float('inf'):
                    print(f'Tidak ada jalur dari {dari} ke {ke}')
                    continue

                path = get_path(parent, ke)
                print(f'\nJalur termurah dari {dari} ke {ke}:')
                print(' -> '.join(path))
                print(f'Total biaya: Rp {dist[ke]:,.2f}')

            elif cmd[0].upper() == 'CEK_STOK':
                if len(cmd) != 2:
                    print('Format: CEK_STOK <kode>')
                    continue

                _, kode = cmd
                produk = bst_katalog.search(kode)

                if not produk:
                    print(f'Produk dengan kode {kode} tidak ditemukan!')
                else:
                    print(f'\nDetail Produk:')
                    print(f'  Kode: {produk.kode}')
                    print(f'  Nama: {produk.nama}')
                    print(f'  Kategori: {produk.kategori}')
                    print(f'  Harga: Rp {produk.harga_satuan:,.2f}')
                    print(f'  Stok: {produk.stok}')
                    print(f'  Masa Kadaluarsa: {produk.masa_kadaluarsa_hari} hari')

            elif cmd[0].upper() == 'KADALUARSA':
                if len(cmd) != 2:
                    print('Format: KADALUARSA <maks_hari>')
                    continue

                try:
                    maks_hari = int(cmd[1])
                except ValueError:
                    print('Maks hari harus berupa angka!')
                    continue

                produk_kadaluarsa = bst_katalog.filter_kadaluarsa(maks_hari)

                if not produk_kadaluarsa:
                    print(f'Tidak ada produk dengan masa kadaluarsa <= {maks_hari} hari')
                else:
                    print(f'\nProduk dengan masa kadaluarsa <= {maks_hari} hari:')
                    print('-' * 60)
                    for p in produk_kadaluarsa:
                        if p.masa_kadaluarsa_hari <= 3:
                            status = 'MENDESAK!'
                     

if __name__ == '__main__':
    main()
