# graph_rantai_pasok.py
# Graf berbobot tidak berarah dengan dua atribut edge: jarak_km dan biaya_per_km
# Dijkstra menggunakan total_biaya = jarak * biaya_km sebagai bobot
# Mendukung: tambah_node, tambah_jalur, tetangga
# DFS/BFS untuk audit konektivitas
# Big-O: add O(1), BFS/DFS O(V+E)
 
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
        if tipe_u == 'PETANI' and tipe_v not in ['DISTRIBUTOR', 'GUDANG', 'PASAR']:
            return
        
        if tipe_u == 'DISTRIBUTOR' and tipe_v not in ['DISTRIBUTOR', 'GUDANG', 'PASAR']:
            return
        
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
 
    def bfs(self, start):
        """BFS untuk audit konektivitas"""
        visited = set()
        queue = [start]
        visited.add(start)
        
        while queue:
            u = queue.pop(0)
            for v, _, _ in self.tetangga(u):
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        return visited
 
    def dfs(self, start, visited=None):
        """DFS untuk audit konektivitas"""
        if visited is None:
            visited = set()
        visited.add(start)
        for v, _, _ in self.tetangga(start):
            if v not in visited:
                self.dfs(v, visited)
        return visited
 
    def bisa_mengirim(self, node_id):
        return self.tipe_node.get(node_id, '') != 'PASAR'
    
    def bisa_menerima(self, node_id):
        return True
 
    def info_node(self, node_id):
        return self.tipe_node.get(node_id, 'TIDAK DIKENAL')
    
    def get_all_nodes(self):
        return list(self.adj.keys())
 
Modul 2: circular_queue_buffer.py
# circular_queue_buffer.py
# Setiap node memiliki Circular Queue berbasis array (fixed capacity=50)
# untuk menyimpan produk secara FIFO
# Big-O: enqueue O(1), dequeue O(1), is_full O(1)
 
class CircularQueue:
    def __init__(self, kapasitas=50):
        self.kapasitas = kapasitas
        self.buffer = [None] * kapasitas
        self.front = 0
        self.rear = 0
        self._size = 0
 
    def enqueue(self, produk):
        """Memasukkan produk ke buffer (FIFO)"""
        if self.is_full():
            return False
        self.buffer[self.rear] = produk
        self.rear = (self.rear + 1) % self.kapasitas
        self._size += 1
        return True
 
    def dequeue(self):
        """Mengeluarkan produk dari buffer (FIFO)"""
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
    
    def clear(self):
        """Mengosongkan buffer"""
        self.buffer = [None] * self.kapasitas
        self.front = 0
        self.rear = 0
        self._size = 0
