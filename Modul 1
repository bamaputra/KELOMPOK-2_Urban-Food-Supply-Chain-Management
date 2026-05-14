"""
Module 1: Graph Rantai Pasok
Graf berbobot tidak berarah dengan dua atribut edge: jarak_km dan biaya_per_km
Mendukung: tambah_node, tambah_jalur, tetangga
DFS/BFS untuk audit konektivitas
Big-O: add O(1), BFS/DFS O(V+E)
"""

class Edge:
    def __init__(self, dest, jarak_km, biaya_per_km):
        self.dest = dest
        self.jarak_km = jarak_km
        self.biaya_per_km = biaya_per_km
        self.next = None


class GraphRantaiPasok:
    def __init__(self):
        self.adj = {}
        self.tipe_node = {}

    def tambah_node(self, node_id, tipe):
        """Menambah node ke graph - Big-O: O(1)"""
        if node_id not in self.adj:
            self.adj[node_id] = None
            self.tipe_node[node_id] = tipe

    def tambah_jalur(self, u, v, jarak, biaya_km):
        """Menambah jalur edge antara dua node"""
        new_edge = Edge(v, jarak, biaya_km)
        new_edge.next = self.adj[u]
        self.adj[u] = new_edge

        new_edge = Edge(u, jarak, biaya_km)
        new_edge.next = self.adj[v]
        self.adj[v] = new_edge

    def tetangga(self, u):
        """Mendapatkan semua tetangga dari node u"""
        neighbors = []
        current = self.adj.get(u, None)
        while current:
            neighbors.append((current.dest, current.jarak_km, current.biaya_per_km))
            current = current.next
        return neighbors

    def bfs_audit(self, start):
        """BFS untuk audit konektivitas - Big-O: O(V+E)"""
        visited = set()
        from collections import deque
        queue = deque([start])
        visited.add(start)
        
        while queue:
            node = queue.popleft()
            current = self.adj.get(node, None)
            while current:
                if current.dest not in visited:
                    visited.add(current.dest)
                    queue.append(current.dest)
                current = current.next
        return visited

    def dfs_audit(self, start):
        """DFS untuk audit konektivitas - Big-O: O(V+E)"""
        visited = set()
        stack = [start]
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                current = self.adj.get(node, None)
                while current:
                    if current.dest not in visited:
                        stack.append(current.dest)
                    current = current.next
        return visited

    def get_all_nodes(self):
        return list(self.adj.keys())
