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


@dataclass
class Pengiriman:
    pengiriman_id: int
    dari_node: str
    ke_node: str
    kode_produk: str
    jumlah: int
    prioritas: int
    waktu_kirim: float
    
    def __init__(self, pengiriman_id, dari_node, ke_node, kode_produk, jumlah, prioritas, waktu_kirim=None):
        self.pengiriman_id = pengiriman_id
        self.dari_node = dari_node
        self.ke_node = ke_node
        self.kode_produk = kode_produk
        self.jumlah = jumlah
        self.prioritas = prioritas
        self.waktu_kirim = waktu_kirim if waktu_kirim else time.time()


# Konstanta
KATEGORI_PRODUK = ['SAYUR', 'BUAH', 'DAGING', 'IKAN', 'BAHAN_POKOK']
TIPE_NODE = ['PETANI', 'DISTRIBUTOR', 'PASAR', 'GUDANG']


def generate_rantai_pasok(seed=61):
    """Generate rantai pasok tanpa numpy"""
    random.seed(seed)
    
    nodes = []
    # 10 petani
    for i in range(10):
        nodes.append((f'PTN{i:02d}', 'PETANI'))
    # 5 distributor
    for i in range(5):
        nodes.append((f'DST{i:02d}', 'DISTRIBUTOR'))
    # 8 pasar
    for i in range(8):
        nodes.append((f'PSR{i:02d}', 'PASAR'))
    # 3 gudang
    for i in range(3):
        nodes.append((f'GDG{i:02d}', 'GUDANG'))
    
    n = len(nodes)
    
    # Generate edges dengan random
    edges = []
    
    # Buat jalur spanning tree dasar
    indices = list(range(n))
    random.shuffle(indices)
    
    for i in range(1, n):
        u = nodes[indices[i-1]][0]
        v = nodes[indices[i]][0]
        jarak = random.randint(5, 200)
        biaya = round(random.uniform(500, 3000), 0)
        edges.append((u, v, jarak, biaya))
    
    # Tambah jalur tambahan
    for _ in range(12):
        i, j = random.sample(range(n), 2)
        jarak = random.randint(5, 200)
        biaya = round(random.uniform(500, 3000), 0)
        edges.append((nodes[i][0], nodes[j][0], jarak, biaya))
    
    # Generate produk
    produk = []
    for i, nm in enumerate(nama_p):
        produk.append(Produk(
            kode=f'PRD-{i:03d}',
            nama=nm,
            kategori=random.choice(KATEGORI_PRODUK),
            harga_satuan=round(random.uniform(2000, 50000), -2),
            stok=random.randint(50, 500),
            masa_kadaluarsa_hari=random.randint(1, 30)
        ))
    
    return nodes, edges, produk


def main():
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
                        elif p.masa_kadaluarsa_hari <= 7:
                            status = 'Perhatikan'
                        else:
                            status = 'Normal'
                        print(f'  {p.kode} | {p.nama:12} | Stok: {p.stok:3} | Kadaluarsa: {p.masa_kadaluarsa_hari:2} hari | {status}')

            elif cmd[0].upper() == 'LAPORAN_DISTRIBUSI':
                print('\n' + '=' * 60)
                print('LAPORAN TRANSAKSI DISTRIBUSI')
                print('=' * 60)

                transaksi_list = log_transaksi.get_all()

                if not transaksi_list:
                    print('Belum ada transaksi distribusi')
                else:
                    for i, transaksi in enumerate(transaksi_list, 1):
                        print(f'{i}. {transaksi}')
                print('=' * 60)

            elif cmd[0].upper() == 'BUFFER':
                if len(cmd) != 2:
                    print('Format: BUFFER <node>')
                    continue

                _, node = cmd

                if node not in buffer_gudang:
                    print(f'Node {node} tidak ditemukan atau bukan gudang')
                    continue

                buffer = buffer_gudang[node]
                if buffer.is_empty():
                    print(f'Buffer gudang {node} kosong')
                else:
                    print(f'\nIsi buffer gudang {node}:')
                    print('-' * 50)
                    for i, p in enumerate(buffer.get_all(), 1):
                        print(f'  {i}. {p.kode} | {p.nama} | Stok: {p.stok} | Kadaluarsa: {p.masa_kadaluarsa_hari} hari')

            else:
                print(f'Perintah tidak dikenal: {cmd[0]}. Ketik BANTUAN untuk daftar perintah.')

        except KeyboardInterrupt:
            print('\nKeluar dari sistem...')
            break
        except Exception as e:
            print(f'Terjadi kesalahan: {e}')


if __name__ == '__main__':
    main()
