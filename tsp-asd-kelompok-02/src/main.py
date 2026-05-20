import random
import time
import math
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple

random.seed(61)

KATEGORI_PRODUK = ['SAYUR', 'BUAH', 'DAGING', 'IKAN', 'BAHAN_POKOK']
TIPE_NODE = ['PETANI', 'DISTRIBUTOR', 'PASAR', 'GUDANG']


# ================================================================
# DATA CLASSES
# ================================================================
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


# ================================================================
# GENERATOR RANTAI PASOK YANG LEBIH BAIK
# ================================================================
def generate_rantai_pasok(seed=61):
    """Generate rantai pasok dengan struktur hierarki yang jelas"""
    random.seed(seed)
    
    # Node dengan hierarki yang jelas
    petani = [f'PTN{i:02d}' for i in range(10)]
    distributor = [f'DST{i:02d}' for i in range(5)]
    pasar = [f'PSR{i:02d}' for i in range(8)]
    gudang = [f'GDG{i:02d}' for i in range(3)]
    
    nodes = []
    for p in petani:
        nodes.append((p, 'PETANI'))
    for d in distributor:
        nodes.append((d, 'DISTRIBUTOR'))
    for p in pasar:
        nodes.append((p, 'PASAR'))
    for g in gudang:
        nodes.append((g, 'GUDANG'))
    
    edges = []
    
    # === JALUR HIERARKI YANG TERSTRUKTUR ===
    
    # 1. PETANI → DISTRIBUTOR (setiap petani terhubung ke 2-3 distributor)
    for p in petani:
        num_connections = random.randint(2, 3)
        distributors_connected = random.sample(distributor, num_connections)
        for d in distributors_connected:
            jarak = random.randint(10, 100)
            biaya = round(random.uniform(500, 2000), 0)
            edges.append((p, d, jarak, biaya))
    
    # 2. DISTRIBUTOR → DISTRIBUTOR (saling terhubung untuk distribusi)
    for i, d1 in enumerate(distributor):
        for d2 in distributor[i+1:]:
            if random.random() < 0.4:  # 40% kemungkinan terhubung
                jarak = random.randint(20, 150)
                biaya = round(random.uniform(800, 2500), 0)
                edges.append((d1, d2, jarak, biaya))
                edges.append((d2, d1, jarak, biaya))
    
    # 3. DISTRIBUTOR → PASAR (setiap distributor terhubung ke 3-4 pasar)
    for d in distributor:
        num_connections = random.randint(3, 4)
        markets_connected = random.sample(pasar, min(num_connections, len(pasar)))
        for m in markets_connected:
            jarak = random.randint(5, 80)
            biaya = round(random.uniform(400, 1500), 0)
            edges.append((d, m, jarak, biaya))
    
    # 4. DISTRIBUTOR → GUDANG (setiap distributor terhubung ke 1-2 gudang)
    for d in distributor:
        num_connections = random.randint(1, 2)
        warehouses_connected = random.sample(gudang, min(num_connections, len(gudang)))
        for g in warehouses_connected:
            jarak = random.randint(10, 60)
            biaya = round(random.uniform(300, 1200), 0)
            edges.append((d, g, jarak, biaya))
    
    # 5. GUDANG → PASAR (setiap gudang terhubung ke 2-3 pasar)
    for g in gudang:
        num_connections = random.randint(2, 3)
        markets_connected = random.sample(pasar, min(num_connections, len(pasar)))
        for m in markets_connected:
            jarak = random.randint(5, 50)
            biaya = round(random.uniform(300, 1000), 0)
            edges.append((g, m, jarak, biaya))
    
    # 6. PETANI → GUDANG (opsional, jalur langsung)
    for p in petani:
        if random.random() < 0.3:  # 30% petani punya akses langsung ke gudang
            g = random.choice(gudang)
            jarak = random.randint(15, 80)
            biaya = round(random.uniform(600, 1800), 0)
            edges.append((p, g, jarak, biaya))
    
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


# ================================================================
# LINKED LIST NODE
# ================================================================
class LLNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None


# ================================================================
# CIRCULAR QUEUE — Buffer Gudang
# ================================================================
class CircularQueue:
    def __init__(self, kapasitas):
        self.kapasitas = kapasitas
        self.buffer = [None] * kapasitas
        self.front = 0
        self.rear = 0
        self._size = 0

    def enqueue(self, produk):
        if self.is_full():
            return False
        self.buffer[self.rear] = produk
        self.rear = (self.rear + 1) % self.kapasitas
        self._size += 1
        return True

    def dequeue(self):
        if self.is_empty():
            return None
        produk = self.buffer[self.front]
        self.buffer[self.front] = None
        self.front = (self.front + 1) % self.kapasitas
        self._size -= 1
        return produk

    def is_full(self):
        return self._size == self.kapasitas

    def is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size

    def get_all(self):
        result = []
        if self.is_empty():
            return result
        idx = self.front
        for _ in range(self._size):
            if self.buffer[idx] is not None:
                result.append(self.buffer[idx])
            idx = (idx + 1) % self.kapasitas
        return result


# ================================================================
# PRIORITY QUEUE — Antrian Pengiriman (Linked List)
# ================================================================
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


# ================================================================
# STACK — Log Transaksi (Linked List)
# ================================================================
class Stack:
    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, data):
        new_node = LLNode(data)
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

    def __len__(self):
        return self._size

    def is_empty(self):
        return self.top is None


# ================================================================
# BST — Katalog Produk
# ================================================================
class BSTNodeProd:
    def __init__(self, produk):
        self.produk = produk
        self.left = None
        self.right = None


class BSTKatalog:
    def __init__(self):
        self.root = None

    def insert(self, produk):
        self.root = self._insert_rec(self.root, produk)

    def _insert_rec(self, node, produk):
        if node is None:
            return BSTNodeProd(produk)
        if produk.kode < node.produk.kode:
            node.left = self._insert_rec(node.left, produk)
        elif produk.kode > node.produk.kode:
            node.right = self._insert_rec(node.right, produk)
        return node

    def search(self, kode):
        return self._search_rec(self.root, kode)

    def _search_rec(self, node, kode):
        if node is None or node.produk.kode == kode:
            return node.produk if node else None
        if kode < node.produk.kode:
            return self._search_rec(node.left, kode)
        return self._search_rec(node.right, kode)

    def update_stok(self, kode, delta):
        produk = self.search(kode)
        if produk:
            produk.stok += delta
            if produk.stok < 0:
                produk.stok = 0
            return True
        return False

    def filter_kadaluarsa(self, maks_hari):
        result = []
        self._filter_rec(self.root, maks_hari, result)
        return result

    def _filter_rec(self, node, maks_hari, result):
        if node is None:
            return
        self._filter_rec(node.left, maks_hari, result)
        if node.produk.masa_kadaluarsa_hari <= maks_hari:
            result.append(node.produk)
        self._filter_rec(node.right, maks_hari, result)

    def inorder(self):
        result = []
        self._inorder_rec(self.root, result)
        return result

    def _inorder_rec(self, node, result):
        if node is None:
            return
        self._inorder_rec(node.left, result)
        result.append(node.produk)
        self._inorder_rec(node.right, result)


# ================================================================
# GRAPH — Rantai Pasok (Directed dengan aturan yang jelas)
# ================================================================
class Edge:
    def __init__(self, dest, jarak_km, biaya_per_km):
        self.dest = dest
        self.jarak_km = jarak_km
        self.biaya_per_km = biaya_per_km
        self.next = None


class GraphRantaiPasok:
    """
    Graph berarah untuk rantai pasok.
    ATURAN:
    - PETANI bisa mengirim ke DISTRIBUTOR, GUDANG, PASAR
    - DISTRIBUTOR bisa mengirim ke DISTRIBUTOR, GUDANG, PASAR
    - GUDANG bisa mengirim ke PASAR
    - PASAR TIDAK BISA mengirim (sink node)
    """
    
    def __init__(self):
        self.adj = {}
        self.tipe_node = {}

    def tambah_node(self, node_id, tipe):
        if node_id not in self.adj:
            self.adj[node_id] = None
            self.tipe_node[node_id] = tipe

    def tambah_jalur(self, u, v, jarak, biaya_km):
        """
        Menambahkan jalur dengan aturan:
        - PASAR tidak bisa memiliki edge keluar
        - Validasi berdasarkan hierarki rantai pasok
        """
        tipe_u = self.tipe_node.get(u, '')
        tipe_v = self.tipe_node.get(v, '')
        
        # VALIDASI: PASAR tidak boleh mengirim
        if tipe_u == 'PASAR':
            return
        
        # VALIDASI HIERARKI (opsional, untuk menjaga struktur)
        # PETANI hanya bisa ke DISTRIBUTOR atau GUDANG atau PASAR
        if tipe_u == 'PETANI' and tipe_v not in ['DISTRIBUTOR', 'GUDANG', 'PASAR']:
            return
        
        # DISTRIBUTOR bisa ke DISTRIBUTOR, GUDANG, PASAR
        if tipe_u == 'DISTRIBUTOR' and tipe_v not in ['DISTRIBUTOR', 'GUDANG', 'PASAR']:
            return
        
        # GUDANG hanya bisa ke PASAR
        if tipe_u == 'GUDANG' and tipe_v != 'PASAR':
            return
        
        # Tambahkan edge u → v
        new_edge = Edge(v, jarak, biaya_km)
        new_edge.next = self.adj[u]
        self.adj[u] = new_edge

    def tetangga(self, u):
        """Mengembalikan daftar tetangga yang bisa dicapai dari u (outgoing edges)"""
        neighbors = []
        current = self.adj.get(u, None)
        while current:
            neighbors.append((current.dest, current.jarak_km, current.biaya_per_km))
            current = current.next
        return neighbors

    def bisa_mengirim(self, node_id):
        """Cek apakah sebuah node boleh mengirim produk"""
        return self.tipe_node.get(node_id, '') != 'PASAR'
    
    def bisa_menerima(self, node_id):
        """Cek apakah node bisa menerima produk"""
        # Semua node bisa menerima
        return True

    def info_node(self, node_id):
        """Mengembalikan informasi tipe node"""
        return self.tipe_node.get(node_id, 'TIDAK DIKENAL')
    
    def get_all_nodes(self):
        return list(self.adj.keys())


# ================================================================
# DIJKSTRA — Jalur Termurah
# ================================================================
def dijkstra_biaya(graph, asal):
    INF = float('inf')
    dist = {v: INF for v in graph.adj}
    parent = {v: None for v in graph.adj}
    dist[asal] = 0.0
    visited = set()

    while len(visited) < len(graph.adj):
        min_dist = INF
        u = None
        for v in graph.adj:
            if v not in visited and dist[v] < min_dist:
                min_dist = dist[v]
                u = v

        if u is None:
            break

        visited.add(u)

        current = graph.adj[u]
        while current:
            v = current.dest
            if v not in visited:
                weight = current.jarak_km * current.biaya_per_km
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    parent[v] = u
            current = current.next

    return dist, parent


def get_path(parent, target):
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = parent.get(current, None)
    return list(reversed(path))


# ================================================================
# HELPER
# ================================================================
def hitung_prioritas(masa_kadaluarsa):
    if masa_kadaluarsa <= 3:
        return 1
    elif masa_kadaluarsa <= 7:
        return 2
    else:
        return 3


def tampilkan_rute_dengan_biaya(graph, path):
    """Menampilkan rute dengan biaya per segmen"""
    total_biaya = 0
    segments = []
    
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        # Cari edge dari u ke v
        current = graph.adj[u]
        while current:
            if current.dest == v:
                biaya_segmen = current.jarak_km * current.biaya_per_km
                total_biaya += biaya_segmen
                segments.append({
                    'from': u,
                    'to': v,
                    'jarak': current.jarak_km,
                    'biaya_km': current.biaya_per_km,
                    'biaya': biaya_segmen
                })
                break
            current = current.next
    
    return segments, total_biaya


# ================================================================
# MAIN
# ================================================================
def main():
    graph = GraphRantaiPasok()
    bst_katalog = BSTKatalog()
    pg_kirim = PriorityQueueKirim()
    log_transaksi = Stack()
    buffer_gudang = {}
    kirim_counter = 0

    nodes, edges, produk_list = generate_rantai_pasok(seed=61)

    # Tambahkan semua node
    for nid, tipe in nodes:
        graph.tambah_node(nid, tipe)
        buffer_gudang[nid] = CircularQueue(kapasitas=50)

    # Tambahkan semua edge
    for u, v, j, b in edges:
        graph.tambah_jalur(u, v, j, b)

    # Tambahkan produk ke BST
    for p in produk_list:
        bst_katalog.insert(p)

    # Statistik awal
    print('=' * 75)
    print('  🏭 FOOD SUPPLY CHAIN MANAGEMENT SYSTEM 🏪')
    print('  Sistem Manajemen Rantai Pasok Bahan Makanan')
    print('=' * 75)
    print(f'\n📊 STATISTIK SISTEM:')
    print(f'  ├─ Total Node      : {len(nodes)}')
    print(f'  │  ├─ PETANI       : {sum(1 for _, t in nodes if t == "PETANI")}')
    print(f'  │  ├─ DISTRIBUTOR  : {sum(1 for _, t in nodes if t == "DISTRIBUTOR")}')
    print(f'  │  ├─ PASAR        : {sum(1 for _, t in nodes if t == "PASAR")} (sink only)')
    print(f'  │  └─ GUDANG       : {sum(1 for _, t in nodes if t == "GUDANG")}')
    print(f'  ├─ Total Produk    : {len(produk_list)}')
    print(f'  ├─ Total Jalur     : {len(edges)}')
    print(f'  └─ Struktur        : Hierarkis dengan PASAR sebagai sink node')
    
    print('\n' + '=' * 75)
    print('📝 DAFTAR PERINTAH:')
    print('  ┌─────────────────────────────────────────────────────────────┐')
    print('  │ KIRIM <dari> <ke> <kode> <jumlah>                           │')
    print('  │     Menambahkan pengiriman ke antrian prioritas             │')
    print('  │                                                             │')
    print('  │ PROSES_KIRIM                                                │')
    print('  │     Memproses pengiriman dengan prioritas tertinggi         │')
    print('  │                                                             │')
    print('  │ RUTE_MURAH <dari> <ke>                                      │')
    print('  │     Mencari rute termurah (Dijkstra)                        │')
    print('  │                                                             │')
    print('  │ CEK_STOK <kode>                                             │')
    print('  │     Mengecek stok produk di katalog                         │')
    print('  │                                                             │')
    print('  │ KADALUARSA <maks_hari>                                      │')
    print('  │     Menampilkan produk yang akan kadaluarsa                 │')
    print('  │                                                             │')
    print('  │ LAPORAN_DISTRIBUSI                                          │')
    print('  │     Menampilkan semua transaksi pengiriman                  │')
    print('  │                                                             │')
    print('  │ BUFFER <node>                                               │')
    print('  │     Melihat isi buffer gudang                               │')
    print('  │                                                             │')
    print('  │ INFO_JARINGAN                                               │')
    print('  │     Menampilkan informasi jaringan                          │')
    print('  │                                                             │')
    print('  │ CEK_KONEKSI <dari> <ke>                                     │')
    print('  │     Memeriksa koneksi langsung antar node                   │')
    print('  │                                                             │')
    print('  │ BANTUAN                                                     │')
    print('  │     Menampilkan bantuan ini                                 │')
    print('  │                                                             │')
    print('  │ KELUAR                                                      │')
    print('  │     Keluar dari sistem                                      │')
    print('  └─────────────────────────────────────────────────────────────┘')
    print('=' * 75)

    while True:
        try:
            cmd = input('\n🍽️  [SCM] > ').strip().split()
            if not cmd:
                continue

            # ────────────── KELUAR ──────────────
            if cmd[0].upper() == 'KELUAR':
                print('\n👋 Terima kasih telah menggunakan sistem manajemen rantai pasok!')
                print('   Total transaksi diproses:', len(log_transaksi))
                break

            # ────────────── BANTUAN ──────────────
            elif cmd[0].upper() == 'BANTUAN':
                print('\n' + '=' * 75)
                print('📖 DAFTAR PERINTAH LENGKAP:')
                print('=' * 75)
                print('  KIRIM <dari> <ke> <kode> <jumlah>')
                print('      → Tambah pengiriman ke antrian (prioritas: MENDESAK/NORMAL/REGULER)')
                print('  PROSES_KIRIM')
                print('      → Proses pengiriman prioritas tertinggi')
                print('  RUTE_MURAH <dari> <ke>')
                print('      → Cari rute dengan biaya terendah')
                print('  CEK_STOK <kode>')
                print('      → Cek stok dan info produk')
                print('  KADALUARSA <maks_hari>')
                print('      → Filter produk berdasarkan kadaluarsa')
                print('  LAPORAN_DISTRIBUSI')
                print('      → Lihat histori transaksi')
                print('  BUFFER <node>')
                print('      → Lihat buffer gudang')
                print('  INFO_JARINGAN')
                print('      → Informasi struktur jaringan')
                print('  CEK_KONEKSI <dari> <ke>')
                print('      → Cek koneksi langsung antar node')
                print('  BANTUAN')
                print('      → Tampilkan bantuan ini')
                print('  KELUAR')
                print('      → Keluar dari aplikasi')
                print('=' * 75)

            # ────────────── INFO_JARINGAN ──────────────
            elif cmd[0].upper() == 'INFO_JARINGAN':
                print('\n' + '=' * 75)
                print('🌐 INFORMASI JARINGAN RANTAI PASOK')
                print('=' * 75)

                print('\n📋 DAFTAR NODE:')
                print(f'  {"ID":<10} {"TIPE":<14} {"Status":<15} {"Outgoing Edges":>15}')
                print('  ' + '-' * 60)
                for nid, tipe in nodes:
                    status = '✅ Bisa Kirim' if tipe != 'PASAR' else '⛔ Sink Only'
                    jml = len(graph.tetangga(nid))
                    print(f'  {nid:<10} {tipe:<14} {status:<15} {jml:>15}')
                
                print('\n🔗 CONTOH KONEKSI:')
                shown = set()
                for nid in graph.adj[:5]:  # Tampilkan 5 node pertama
                    tetangga = graph.tetangga(nid)
                    if tetangga:
                        print(f'  📍 {nid} ({graph.tipe_node[nid]}) → ', end='')
                        print(', '.join([f'{t[0]}({graph.tipe_node[t[0]]})' for t in tetangga[:3]]))
                        if len(tetangga) > 3:
                            print(f'    dan {len(tetangga)-3} node lainnya')
                
                print('\n📊 STATISTIK JARINGAN:')
                total_outgoing = sum(len(graph.tetangga(nid)) for nid in graph.adj)
                print(f'  ├─ Total Edge Keluar : {total_outgoing}')
                print(f'  ├─ Rata-rata per node: {total_outgoing/len(graph.adj):.1f}')
                print(f'  └─ Node PASAR        : {sum(1 for _, t in nodes if t == "PASAR")} (tidak memiliki edge keluar)')
                print('=' * 75)

            # ────────────── KIRIM ──────────────
            elif cmd[0].upper() == 'KIRIM':
                if len(cmd) != 5:
                    print('❌ Format salah! Gunakan: KIRIM <dari> <ke> <kode> <jumlah>')
                    continue

                _, dari, ke, kode, jumlah_str = cmd
                try:
                    jumlah = int(jumlah_str)
                except ValueError:
                    print('❌ Jumlah harus berupa angka!')
                    continue

                if jumlah <= 0:
                    print('❌ Jumlah harus lebih dari 0!')
                    continue

                # Validasi node
                if dari not in graph.adj or ke not in graph.adj:
                    print(f'❌ Node tidak ditemukan! (cek: {dari} atau {ke})')
                    continue

                # Validasi: PASAR tidak bisa mengirim
                if graph.tipe_node.get(dari) == 'PASAR':
                    print(f'❌ DITOLAK! Node {dari} adalah PASAR.')
                    print('   PASAR hanya bisa MENERIMA produk, tidak bisa MENGIRIM!')
                    continue

                # Validasi koneksi (opsional, bisa menggunakan Dijkstra nanti)
                # Cek apakah ada jalur (tidak harus langsung)
                dist, _ = dijkstra_biaya(graph, dari)
                if dist.get(ke, float('inf')) == float('inf'):
                    print(f'⚠️  PERINGATAN: Tidak ada jalur dari {dari} ke {ke}')
                    print(f'   Pengiriman akan tetap ditambahkan, tapi tidak bisa diproses.')
                    konfirmasi = input('   Tetap tambahkan? (y/n): ')
                    if konfirmasi.lower() != 'y':
                        continue

                # Validasi produk
                produk = bst_katalog.search(kode)
                if not produk:
                    print(f'❌ Produk dengan kode {kode} tidak ditemukan!')
                    continue

                if produk.stok < jumlah:
                    print(f'❌ Stok tidak mencukupi! Stok tersedia: {produk.stok}')
                    continue

                # Kurangi stok
                bst_katalog.update_stok(kode, -jumlah)

                prioritas = hitung_prioritas(produk.masa_kadaluarsa_hari)
                prioritas_text = {1: '🔴 MENDESAK', 2: '🟡 NORMAL', 3: '🟢 REGULER'}[prioritas]

                kirim_counter += 1
                pengiriman = Pengiriman(
                    pengiriman_id=kirim_counter,
                    dari_node=dari,
                    ke_node=ke,
                    kode_produk=kode,
                    jumlah=jumlah,
                    prioritas=prioritas,
                    waktu_kirim=time.time()
                )

                pg_kirim.enqueue(pengiriman)

                tipe_dari = graph.tipe_node.get(dari, '')
                tipe_ke = graph.tipe_node.get(ke, '')
                print(f'\n✅ Pengiriman #{kirim_counter} ditambahkan ke antrian')
                print(f'   📍 {dari} ({tipe_dari}) → {ke} ({tipe_ke})')
                print(f'   📦 Produk: {produk.nama} (ID: {kode}) x{jumlah}')
                print(f'   ⚡ Prioritas: {prioritas_text}')

            # ────────────── PROSES_KIRIM ──────────────
            elif cmd[0].upper() == 'PROSES_KIRIM':
                if pg_kirim.is_empty():
                    print('📭 Tidak ada pengiriman dalam antrian')
                    continue

                pengiriman = pg_kirim.dequeue()
                if not pengiriman:
                    print('❌ Gagal memproses pengiriman')
                    continue

                # Cek apakah ada jalur
                dist, parent = dijkstra_biaya(graph, pengiriman.dari_node)
                if dist.get(pengiriman.ke_node, float('inf')) == float('inf'):
                    print(f'❌ Pengiriman #{pengiriman.pengiriman_id} GAGAL!')
                    print(f'   Tidak ada jalur dari {pengiriman.dari_node} ke {pengiriman.ke_node}')
                    # Kembalikan stok
                    bst_katalog.update_stok(pengiriman.kode_produk, pengiriman.jumlah)
                    continue

                # Proses pengiriman
                tipe_tujuan = graph.tipe_node.get(pengiriman.ke_node, '')
                if tipe_tujuan == 'GUDANG':
                    produk = bst_katalog.search(pengiriman.kode_produk)
                    if produk:
                        success = buffer_gudang[pengiriman.ke_node].enqueue(produk)
                        if success:
                            print(f'  📦 → Produk disimpan ke buffer gudang {pengiriman.ke_node}')
                        else:
                            print(f'  ⚠️  → Buffer gudang {pengiriman.ke_node} penuh! Produk tidak tersimpan')
                elif tipe_tujuan == 'PASAR':
                    print(f'  🏪 → Produk diterima oleh PASAR {pengiriman.ke_node}')
                else:
                    print(f'  📍 → Produk diterima oleh {pengiriman.ke_node} ({tipe_tujuan})')

                prioritas_text = {
                    1: 'MENDESAK', 2: 'NORMAL', 3: 'REGULER'
                }[pengiriman.prioritas]

                log_entry = (
                    f'[ID:{pengiriman.pengiriman_id:04d}] '
                    f'{pengiriman.dari_node} → {pengiriman.ke_node} | '
                    f'{pengiriman.kode_produk} x{pengiriman.jumlah} | '
                    f'Prioritas:{prioritas_text}'
                )
                log_transaksi.push(log_entry)

                print(f'\n✅ Pengiriman #{pengiriman.pengiriman_id} berhasil diproses!')

            # ────────────── RUTE_MURAH ──────────────
            elif cmd[0].upper() == 'RUTE_MURAH':
                if len(cmd) != 3:
                    print('❌ Format salah! Gunakan: RUTE_MURAH <dari> <ke>')
                    continue

                _, dari, ke = cmd

                if dari not in graph.adj or ke not in graph.adj:
                    print(f'❌ Node tidak ditemukan! (cek: {dari} atau {ke})')
                    continue

                # Validasi: PASAR tidak bisa menjadi asal
                if graph.tipe_node.get(dari) == 'PASAR':
                    print(f'❌ DITOLAK! Node {dari} adalah PASAR.')
                    print('   PASAR hanya bisa MENERIMA produk, tidak bisa MENGIRIM!')
                    print('   Tidak ada rute keluar dari PASAR.')
                    continue

                dist, parent = dijkstra_biaya(graph, dari)

                if dist.get(ke, float('inf')) == float('inf'):
                    print(f'\n❌ TIDAK ADA JALUR dari {dari} ke {ke}')
                    print('   Kemungkinan penyebab:')
                    print('   • Node tujuan tidak terhubung dalam graf')
                    print('   • Hierarki yang tidak mengizinkan pengiriman langsung')
                    print('   • Coba gunakan perintah CEK_KONEKSI untuk melihat koneksi')
                    continue

                path = get_path(parent, ke)
                
                print(f'\n✨ RUTE TERMURAH dari {dari} ke {ke}:')
                print('=' * 75)
                
                # Tampilkan rute dengan detail
                segments, total_biaya = tampilkan_rute_dengan_biaya(graph, path)
                
                print('\n  📍 RUTE:')
                for i, seg in enumerate(segments, 1):
                    print(f'    {i}. {seg["from"]} → {seg["to"]}')
                    print(f'       📏 Jarak: {seg["jarak"]} km | 💰 Biaya/km: Rp {seg["biaya_km"]:,.0f}')
                    print(f'       💵 Biaya segmen: Rp {seg["biaya"]:,.2f}')
                    if i < len(segments):
                        print(f'       ↓')
                
                print(f'\n  📊 TOTAL BIAYA: Rp {total_biaya:,.2f}')
                print(f'  📍 Total segmen: {len(segments)}')
                print('=' * 75)

            # ────────────── CEK_KONEKSI (perintah baru) ──────────────
            elif cmd[0].upper() == 'CEK_KONEKSI':
                if len(cmd) != 3:
                    print('❌ Format salah! Gunakan: CEK_KONEKSI <dari> <ke>')
                    continue
                
                _, dari, ke = cmd
                
                if dari not in graph.adj or ke not in graph.adj:
                    print(f'❌ Node tidak ditemukan!')
                    continue
                
                print(f'\n🔍 CEK KONEKSI: {dari} → {ke}')
                print('=' * 50)
                
                # Cek koneksi langsung
                tetangga = graph.tetangga(dari)
                langsung = False
                for n, j, b in tetangga:
                    if n == ke:
                        langsung = True
                        print(f'✅ ADA koneksi LANGSUNG!')
                        print(f'   📏 Jarak: {j} km')
                        print(f'   💰 Biaya per km: Rp {b:,.0f}')
                        print(f'   💵 Total biaya langsung: Rp {j * b:,.2f}')
                        break
                
                if not langsung:
                    print(f'❌ TIDAK ADA koneksi langsung dari {dari} ke {ke}')
                
                # Cek apakah ada jalur tidak langsung
                dist, _ = dijkstra_biaya(graph, dari)
                if dist.get(ke, float('inf')) != float('inf'):
                    print(f'\n✅ Tersedia jalur TIDAK LANGSUNG (dapat ditemukan dengan RUTE_MURAH)')
                    print(f'   💰 Estimasi biaya minimal: Rp {dist[ke]:,.2f}')
                else:
                    print(f'\n❌ TIDAK ADA jalur sama sekali dari {dari} ke {ke}')
                    print(f'   Kemungkinan node {ke} tidak terhubung dalam graf')
                
                # Tampilkan tetangga langsung
                if tetangga:
                    print(f'\n📋 Tetangga langsung dari {dari}:')
                    for n, j, b in tetangga[:5]:
                        tipe = graph.tipe_node.get(n, '?')
                        print(f'   • {n} ({tipe}) - Jarak: {j} km')
                
                print('=' * 50)

            # ────────────── CEK_STOK ──────────────
            elif cmd[0].upper() == 'CEK_STOK':
                if len(cmd) != 2:
                    print('❌ Format salah! Gunakan: CEK_STOK <kode>')
                    continue

                _, kode = cmd
                produk = bst_katalog.search(kode)

                if not produk:
                    print(f'❌ Produk dengan kode {kode} tidak ditemukan!')
                else:
                    print(f'\n📦 DETAIL PRODUK:')
                    print('=' * 50)
                    print(f'  Kode          : {produk.kode}')
                    print(f'  Nama          : {produk.nama}')
                    print(f'  Kategori      : {produk.kategori}')
                    print(f'  Harga         : Rp {produk.harga_satuan:,.2f}')
                    print(f'  Stok          : {produk.stok} unit')
                    print(f'  Kadaluarsa    : {produk.masa_kadaluarsa_hari} hari')
                    prioritas = hitung_prioritas(produk.masa_kadaluarsa_hari)
                    ket = {1: '🔴 MENDESAK', 2: '🟡 NORMAL', 3: '🟢 REGULER'}
                    print(f'  Prioritas     : {ket[prioritas]}')
                    print('=' * 50)

            # ────────────── KADALUARSA ──────────────
            elif cmd[0].upper() == 'KADALUARSA':
                if len(cmd) != 2:
                    print('❌ Format salah! Gunakan: KADALUARSA <maks_hari>')
                    continue

                try:
                    maks_hari = int(cmd[1])
                except ValueError:
                    print('❌ Maks hari harus berupa angka!')
                    continue

                produk_kadaluarsa = bst_katalog.filter_kadaluarsa(maks_hari)

                if not produk_kadaluarsa:
                    print(f'✅ Tidak ada produk dengan masa kadaluarsa <= {maks_hari} hari')
                else:
                    print(f'\n⚠️  PRODUK DENGAN KADALUARSA <= {maks_hari} HARI:')
                    print('=' * 75)
                    print(f'  {"Kode":<10} {"Nama":<15} {"Stok":>5} {"Kadaluarsa":>12} {"Status":<15}')
                    print('-' * 75)
                    for p in produk_kadaluarsa:
                        if p.masa_kadaluarsa_hari <= 3:
                            status = '🔴 MENDESAK!'
                        elif p.masa_kadaluarsa_hari <= 7:
                            status = '🟡 Perhatikan'
                        else:
                            status = '🟢 Normal'
                        print(
                            f'  {p.kode:<10} {p.nama:<15} {p.stok:>5}'
                            f' {p.masa_kadaluarsa_hari:>8} hari  {status:<15}'
                        )
                    print('=' * 75)

            # ────────────── LAPORAN_DISTRIBUSI ──────────────
            elif cmd[0].upper() == 'LAPORAN_DISTRIBUSI':
                print('\n' + '=' * 75)
                print('📋 LAPORAN TRANSAKSI DISTRIBUSI')
                print('=' * 75)

                transaksi_list = []
                temp_stack = Stack()
                while not log_transaksi.is_empty():
                    transaksi = log_transaksi.pop()
                    transaksi_list.append(transaksi)
                    temp_stack.push(transaksi)

                # Kembalikan ke stack asli
                while not temp_stack.is_empty():
                    log_transaksi.push(temp_stack.pop())

                if not transaksi_list:
                    print('📭 Belum ada transaksi distribusi')
                else:
                    print(f'\n  Total {len(transaksi_list)} transaksi:\n')
                    for i, transaksi in enumerate(reversed(transaksi_list), 1):
                        print(f'  {i:2}. {transaksi}')
                print('=' * 75)

            # ────────────── BUFFER ──────────────
            elif cmd[0].upper() == 'BUFFER':
                if len(cmd) != 2:
                    print('❌ Format salah! Gunakan: BUFFER <node>')
                    continue

                _, node = cmd

                if node not in buffer_gudang:
                    print(f'❌ Node {node} tidak ditemukan!')
                    continue

                tipe_node = graph.tipe_node.get(node, '')
                buffer = buffer_gudang[node]

                if buffer.is_empty():
                    print(f'📭 Buffer {node} ({tipe_node}) kosong')
                else:
                    print(f'\n📦 ISI BUFFER {node} ({tipe_node}):')
                    print('-' * 60)
                    for i, p in enumerate(buffer.get_all(), 1):
                        print(
                            f'  {i}. {p.kode} | {p.nama:<15} |'
                            f' Kadaluarsa: {p.masa_kadaluarsa_hari} hari'
                        )
                    print(f'\n  📊 Kapasitas: {len(buffer)}/{buffer.kapasitas} ({len(buffer)*100//buffer.kapasitas}%)')
                    print('-' * 60)

            else:
                print(f'❌ Perintah tidak dikenal: {cmd[0]}')
                print('   Ketik BANTUAN untuk melihat daftar perintah yang tersedia')

        except KeyboardInterrupt:
            print('\n\n👋 Keluar dari sistem...')
            break
        except Exception as e:
            print(f'❌ Terjadi kesalahan: {e}')
            print('   Silakan coba lagi atau restart program')


if __name__ == '__main__':
    main()
