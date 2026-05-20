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
