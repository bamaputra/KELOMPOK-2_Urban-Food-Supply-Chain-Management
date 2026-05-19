# modul6_cli.py
import random
import time
from typing import List, Tuple
 
# Import dari modul lain
from modul1_graph import GraphRantaiPasok
from modul2_circular_queue import CircularQueue
from modul3_priority_queue import PriorityQueueKirim, hitung_prioritas, get_prioritas_text
from modul4_bst_katalog import BSTKatalog, Produk
from modul5_dijkstra import dijkstra_biaya, get_path
 
 
# Data kelas tambahan
@dataclass
class Pengiriman:
    pengiriman_id: int
    dari_node: str
    ke_node: str
    kode_produk: str
    jumlah: int
    prioritas: int
    waktu_kirim: float
 
 
# Stack untuk log transaksi (menggunakan linked list sederhana)
class LLNodeLog:
    def __init__(self, data=None):
        self.data = data
        self.next = None
 
 
class Stack:
    def __init__(self):
        self.top = None
        self._size = 0
 
    def push(self, data):
        new_node = LLNodeLog(data)
        new_node.next = self.top
        self.top = new_node
        self._size += 1
 
    def pop(self):
        if self.top is None:
            return None
        data = self.top.data
        self.top = self.top.next
        self._size -= 1
        return data
 
    def is_empty(self):
        return self.top is None
 
 
# Generator Rantai Pasok
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
        u = nodes[indices[i - 1]][0]
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
    nama_p = ['Beras', 'Cabai', 'Tomat', 'Ayam', 'Ikan Lele', 'Kangkung',
              'Wortel', 'Kentang', 'Telur', 'Tahu', 'Tempe', 'Minyak']
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
    """CLI Rantai Pasok - Implementasi semua perintah"""
    graph = GraphRantaiPasok()
    bst_katalog = BSTKatalog()
    pg_kirim = PriorityQueueKirim()
    log_transaksi = Stack()
    buffer_gudang = {}
    kirim_counter = 0
 
    nodes, edges, produk_list = generate_rantai_pasok(seed=61)
 
    for nid, tipe in nodes:
        graph.tambah_node(nid, tipe)
        buffer_gudang[nid] = CircularQueue(kapasitas=50)
 
    for u, v, j, b in edges:
        graph.tambah_jalur(u, v, j, b)
 
    for p in produk_list:
        bst_katalog.insert(p)
 
    # Hitung statistik edge untuk info
    total_outgoing = 0
    pasar_outgoing = 0
    for nid in graph.adj:
        count = len(graph.tetangga(nid))
        total_outgoing += count
        if graph.tipe_node[nid] == 'PASAR':
            pasar_outgoing += count
 
    print('=' * 65)
    print('  Food Supply Chain Management System')
    print('  [ATURAN: PASAR hanya bisa MENERIMA, TIDAK bisa MENGIRIM]')
    print('=' * 65)
    print(f'  Total Node   : {len(nodes)}')
    print(f'    PETANI      : {sum(1 for _, t in nodes if t == "PETANI")}')
    print(f'    DISTRIBUTOR : {sum(1 for _, t in nodes if t == "DISTRIBUTOR")}')
    print(f'    PASAR       : {sum(1 for _, t in nodes if t == "PASAR")} (sink-only)')
    print(f'    GUDANG      : {sum(1 for _, t in nodes if t == "GUDANG")}')
    print(f'  Total Produk : {len(produk_list)}')
    print(f'  Edge keluar dari PASAR: {pasar_outgoing} (blokir)')
    print('=' * 65)
    print('Perintah yang tersedia:')
    print('  KIRIM <dari> <ke> <kode> <jumlah>')
    print('  PROSES_KIRIM')
    print('  RUTE_MURAH <dari> <ke>')
    print('  CEK_STOK <kode>')
    print('  KADALUARSA <maks_hari>')
    print('  LAPORAN_DISTRIBUSI')
    print('  BUFFER <node>')
    print('  INFO_JARINGAN')
    print('  BANTUAN')
    print('  KELUAR')
    print('=' * 65)
 
    while True:
        try:
            cmd = input('\n> ').strip().split()
            if not cmd:
                continue
 
            # KELUAR
            if cmd[0].upper() == 'KELUAR':
                print('Terima kasih telah menggunakan sistem manajemen rantai pasok!')
                break
 
            # BANTUAN
            elif cmd[0].upper() == 'BANTUAN':
                print('\nDaftar Perintah:')
                print('  KIRIM <dari> <ke> <kode> <jumlah>')
                print('      Kirim produk dari node ke node')
                print('      *** PASAR tidak bisa menjadi pengirim! ***')
                print('  PROSES_KIRIM')
                print('      Proses pengiriman dengan prioritas tertinggi')
                print('  RUTE_MURAH <dari> <ke>')
                print('      Cari rute termurah antara dua node')
                print('      *** Tidak bisa mencari rute dari PASAR! ***')
                print('  CEK_STOK <kode>')
                print('      Cek stok produk di katalog')
                print('  KADALUARSA <maks_hari>')
                print('      Lihat produk dengan kadaluarsa <= maks_hari')
                print('  LAPORAN_DISTRIBUSI')
                print('      Tampilkan semua transaksi pengiriman')
                print('  BUFFER <node>')
                print('      Lihat isi buffer gudang suatu node')
                print('  INFO_JARINGAN')
                print('      Tampilkan struktur jaringan & aturan PASAR')
                print('  KELUAR')
                print('      Keluar dari sistem')
 
            # INFO_JARINGAN
            elif cmd[0].upper() == 'INFO_JARINGAN':
                print('\n' + '=' * 65)
                print('INFORMASI JARINGAN RANTAI PASOK')
                print('=' * 65)
 
                print('\nDaftar Node:')
                print(f'  {"ID":<8} {"TIPE":<14} {"Bisa Kirim?":<14} {"Jml Tetangga Keluar"}')
                print('  ' + '-' * 55)
                for nid, tipe in nodes:
                    bisa = 'YA' if tipe != 'PASAR' else 'TIDAK (PASAR)'
                    jml = len(graph.tetangga(nid))
                    print(f'  {nid:<8} {tipe:<14} {bisa:<14} {jml}')
 
                print('\nAlur Rantai Pasok:')
                print('  PETANI ──► DISTRIBUTOR ──► PASAR  (PASAR = ujung/sink)')
                print('              DISTRIBUTOR ──► GUDANG')
                print('              GUDANG ──► PASAR')
                print('  *** PASAR TIDAK PERNAH MENJADI PENGIRIM ***')
                print('=' * 65)
 
            # KIRIM
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
 
                if jumlah <= 0:
                    print('Jumlah harus lebih dari 0!')
                    continue
 
                if dari not in graph.adj or ke not in graph.adj:
                    print('Node tidak ditemukan!')
                    continue
 
                if graph.tipe_node.get(dari) == 'PASAR':
                    print(f'✗ DITOLAK! Node {dari} adalah PASAR.')
                    print('  PASAR hanya bisa MENERIMA produk, tidak bisa MENGIRIM!')
                    continue
 
                produk = bst_katalog.search(kode)
                if not produk:
                    print(f'Produk dengan kode {kode} tidak ditemukan!')
                    continue
 
                if produk.stok < jumlah:
                    print(f'Stok tidak mencukupi! Stok tersedia: {produk.stok}')
                    continue
 
                bst_katalog.update_stok(kode, -jumlah)
 
                prioritas = hitung_prioritas(produk.masa_kadaluarsa_hari)
                prioritas_text = get_prioritas_text(prioritas)
 
                kirim_counter += 1
                pengiriman = Pengiriman(
                    pengiriman_id=kirim_counter,
                    dari_node=dari,
                    ke_node=ke,
