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
# GENERATOR RANTAI PASOK
# ================================================================
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
# GRAPH — Rantai Pasok (Directed: PASAR hanya menerima)
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
    ATURAN: PASAR hanya memiliki edge masuk (tidak bisa mengirim).
    Semua edge yang melibatkan PASAR hanya satu arah menuju PASAR.
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
        - Jika u adalah PASAR → tidak menambah edge u→v (PASAR tidak bisa mengirim)
        - Jika v adalah PASAR → tidak menambah edge v→u (PASAR tidak bisa mengirim)
        - Jika keduanya PASAR → tidak menambah edge sama sekali
        - Jika keduanya bukan PASAR → menambahkan edge dua arah seperti biasa
        """
        tipe_u = self.tipe_node.get(u, '')
        tipe_v = self.tipe_node.get(v, '')
 
        # u → v : hanya jika u BUKAN PASAR
        if tipe_u != 'PASAR':
            new_edge = Edge(v, jarak, biaya_km)
            new_edge.next = self.adj[u]
            self.adj[u] = new_edge
 
        # v → u : hanya jika v BUKAN PASAR
        if tipe_v != 'PASAR':
            new_edge = Edge(u, jarak, biaya_km)
            new_edge.next = self.adj[v]
            self.adj[v] = new_edge
 
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
 
    def info_node(self, node_id):
        """Mengembalikan informasi tipe node"""
        return self.tipe_node.get(node_id, 'TIDAK DIKENAL')
 
 
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
 
            # ────────────── KELUAR ──────────────
            if cmd[0].upper() == 'KELUAR':
                print('Terima kasih telah menggunakan sistem manajemen rantai pasok!')
                break
 
            # ────────────── BANTUAN ──────────────
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
 
            # ────────────── INFO_JARINGAN ──────────────
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
 
            # ────────────── KIRIM ──────────────
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
 
                # Cek node ada
                if dari not in graph.adj or ke not in graph.adj:
                    print('Node tidak ditemukan!')
                    continue
 
                # ★ VALIDASI UTAMA: PASAR tidak bisa mengirim
                if graph.tipe_node.get(dari) == 'PASAR':
                    print(f'✗ DITOLAK! Node {dari} adalah PASAR.')
                    print('  PASAR hanya bisa MENERIMA produk, tidak bisa MENGIRIM!')
                    continue
 
                # Cek produk
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
                prioritas_text = {1: 'MENDESAK', 2: 'NORMAL', 3: 'REGULER'}[prioritas]
 
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
                print(f'✓ Pengiriman #{kirim_counter} ditambahkan ke antrian')
                print(f'  {dari} ({tipe_dari}) ──► {ke} ({tipe_ke})')
                print(f'  Produk: {produk.nama} x{jumlah}')
                print(f'  Prioritas: {prioritas_text}')
 
            # ────────────── PROSES_KIRIM ──────────────
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
                        success = buffer_gudang[pengiriman.ke_node].enqueue(produk)
                        if success:
                            print(f'  → Produk disimpan ke buffer gudang {pengiriman.ke_node}')
                        else:
                            print(f'  → Buffer gudang {pengiriman.ke_node} penuh! Produk tidak tersimpan')
                elif tipe_tujuan == 'PASAR':
                    print(f'  → Produk diterima oleh PASAR {pengiriman.ke_node}')
 
                prioritas_text = {
                    1: 'MENDESAK', 2: 'NORMAL', 3: 'REGULER'
                }[pengiriman.prioritas]
 
                log_entry = (
                    f'[ID:{pengiriman.pengiriman_id}] '
                    f'{pengiriman.dari_node} → {pengiriman.ke_node} | '
                    f'{pengiriman.kode_produk} x{pengiriman.jumlah} | '
                    f'Prioritas:{prioritas_text}'
                )
                log_transaksi.push(log_entry)
 
                print(f'✓ Pengiriman #{pengiriman.pengiriman_id} diproses')
 
            # ────────────── RUTE_MURAH ──────────────
            elif cmd[0].upper() == 'RUTE_MURAH':
                if len(cmd) != 3:
                    print('Format: RUTE_MURAH <dari> <ke>')
                    continue
 
                _, dari, ke = cmd
 
                if dari not in graph.adj or ke not in graph.adj:
                    print('Node tidak ditemukan!')
                    continue
 
                # ★ VALIDASI: PASAR tidak bisa menjadi asal pengiriman
                if graph.tipe_node.get(dari) == 'PASAR':
                    print(f'✗ DITOLAK! Node {dari} adalah PASAR.')
                    print('  PASAR hanya bisa MENERIMA produk, tidak bisa MENGIRIM!')
                    print('  Tidak ada rute keluar dari PASAR.')
                    continue
 
                dist, parent = dijkstra_biaya(graph, dari)
 
                if dist[ke] == float('inf'):
                    print(f'Tidak ada jalur dari {dari} ke {ke}')
                    continue
 
                path = get_path(parent, ke)
                print(f'\nJalur termurah dari {dari} ke {ke}:')
                # Tampilkan dengan keterangan tipe node
                path_labeled = []
                for node_id in path:
                    tipe = graph.tipe_node.get(node_id, '?')
                    path_labeled.append(f'{node_id}({tipe})')
                print(' → '.join(path_labeled))
                print(f'Total biaya: Rp {dist[ke]:,.2f}')
 
            # ────────────── CEK_STOK ──────────────
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
                    print(f'  Kode          : {produk.kode}')
                    print(f'  Nama          : {produk.nama}')
                    print(f'  Kategori      : {produk.kategori}')
                    print(f'  Harga         : Rp {produk.harga_satuan:,.2f}')
                    print(f'  Stok          : {produk.stok}')
                    print(f'  Kadaluarsa    : {produk.masa_kadaluarsa_hari} hari')
                    prioritas = hitung_prioritas(produk.masa_kadaluarsa_hari)
                    ket = {1: 'MENDESAK', 2: 'NORMAL', 3: 'REGULER'}
                    print(f'  Prioritas     : {ket[prioritas]}')
 
            # ────────────── KADALUARSA ──────────────
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
                    print('-' * 70)
                    print(f'  {"Kode":<10} {"Nama":<12} {"Stok":>5} {"Kadaluarsa":>12} {"Status"}')
                    print('-' * 70)
                    for p in produk_kadaluarsa:
                        if p.masa_kadaluarsa_hari <= 3:
                            status = '⚠ MENDESAK!'
                        elif p.masa_kadaluarsa_hari <= 7:
                            status = '⚡ Perhatikan'
                        else:
                            status = '✓ Normal'
                        print(
                            f'  {p.kode:<10} {p.nama:<12} {p.stok:>5}'
                            f' {p.masa_kadaluarsa_hari:>8} hari  {status}'
                        )
 
            # ────────────── LAPORAN_DISTRIBUSI ──────────────
            elif cmd[0].upper() == 'LAPORAN_DISTRIBUSI':
                print('\n' + '=' * 65)
                print('LAPORAN TRANSAKSI DISTRIBUSI')
                print('=' * 65)
 
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
                    print('Belum ada transaksi distribusi')
                else:
                    for i, transaksi in enumerate(reversed(transaksi_list), 1):
                        print(f'{i}. {transaksi}')
                print('=' * 65)
 
            # ────────────── BUFFER ──────────────
            elif cmd[0].upper() == 'BUFFER':
                if len(cmd) != 2:
                    print('Format: BUFFER <node>')
                    continue
 
                _, node = cmd
 
                if node not in buffer_gudang:
                    print(f'Node {node} tidak ditemukan!')
                    continue
 
                tipe_node = graph.tipe_node.get(node, '')
                buffer = buffer_gudang[node]
 
                if buffer.is_empty():
                    print(f'Buffer {node} ({tipe_node}) kosong')
                else:
                    print(f'\nIsi buffer {node} ({tipe_node}):')
                    print('-' * 55)
                    for i, p in enumerate(buffer.get_all(), 1):
                        print(
                            f'  {i}. {p.kode} | {p.nama:<12} |'
                            f' Kadaluarsa: {p.masa_kadaluarsa_hari} hari'
                        )
                    print(f'  Kapasitas: {len(buffer)}/{buffer.kapasitas}')
 
            else:
                print(f'Perintah tidak dikenal: {cmd[0]}. Ketik BANTUAN untuk daftar perintah.')
 
        except KeyboardInterrupt:
            print('\nKeluar dari sistem...')
            break
        except Exception as e:
            print(f'Terjadi kesalahan: {e}')
 
 
if __name__ == '__main__':
    main()
