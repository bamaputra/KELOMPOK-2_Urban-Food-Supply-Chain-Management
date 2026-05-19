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
 
