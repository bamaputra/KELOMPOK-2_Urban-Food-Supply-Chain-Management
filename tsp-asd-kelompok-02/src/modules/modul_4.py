# bst_katalog.py
from models import product 
class bst node 

if (  def init unit  self. root

def _search_rec(self, node, kode):
        if node is None or node.produk.kode == kode:
            return node.produk if node else None
        if kode < node.produk.kode:
            return self._search_rec(node.left, kode)
        return self._search_rec(node.right, kode)
 
    def update_stok(self, kode, delta):
        produk = self.search(kode)
        if produk:
                import random
import time
from graph_rantai_pasok import GraphRantaiPasok
from bst_katalog import BSTKatalog
from queue_stack_buffer import PriorityQueueKirim, Stack, CircularQueue
from dijkstra import dijkstra_biaya, get_path, hitung_prioritas
from models import Produk, Pengiriman, KATEGORI_PRODUK
 
 
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
  etani
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
    graph = GraphRantaiPasok()
    bst_katalog = BSTKatalog()
    pg_kirim = PriorityQueueKirim()
    log_transaksi = Stack()
    buffer_gudang = {}
    kirim_counter = 0
 
   class PriorityQueueKirim:
    def __init__(self):
        self.head = None
        self._size = 0
 
    def enqueue(self, pengiriman):
        new_node = LLNode(pengiriman)
        if self.head is None or pengiriman.prioritas < self.head.data.prioritas:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while (current.next is not None
                   and current.next.data.prioritas <= pengiriman.prioritas):
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self._size += 1
 
    def dequeue(self):
        if self.head is None:
            return None
        pengiriman = self.head.data
        self.head = self.head.next
        self._size -= 1
        return pengiriman
 
    def __len__(self):
        return self._size
 
    def is_empty(self):
        return self.head is None




