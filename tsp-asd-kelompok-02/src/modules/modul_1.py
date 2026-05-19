# modul1_graph.py
from typing import List, Tuple, Dict, Optional
 
class Edge:
    def __init__(self, dest, jarak_km, biaya_per_km):
        self.dest = dest
        self.jarak_km = jarak_km
        self.biaya_per_km = biaya_per_km
        self.next = None
 
 
class GraphRantaiPasok:
    """
    Graf berbobot tidak berarah dengan dua atribut edge: jarak_km dan biaya_per_km.
    Dijkstra menggunakan total_biaya = jarak * biaya_km sebagai bobot.
    Mendukung: tambah_node, tambah_jalur, tetangga.
    DFS/BFS untuk audit konektivitas.
    Big-O: add O(1), BFS/DFS O(V+E).
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
 
    def bfs_audit(self, start):
        """BFS untuk audit konektivitas - O(V+E)"""
        visited = set()
        queue = [start]
        visited.add(start)
        
        while queue:
            node = queue.pop(0)
            for neighbor, _, _ in self.tetangga(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return visited
 
    def dfs_audit(self, start):
        """DFS untuk audit konektivitas - O(V+E)"""
        visited = set()
        
        def dfs_rec(node):
            visited.add(node)
            for neighbor, _, _ in self.tetangga(node):
                if neighbor not in visited:
                    dfs_rec(neighbor)
        
        dfs_rec(start)
        return visited
 
