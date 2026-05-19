class Edge: # digunakan untuk menyimpan data jalur antar node.
    def __init__(self, dest, jarak_km, biaya_per_km):
        self.dest = dest
        self.jarak_km = jarak_km
        self.biaya_per_km = biaya_per_km
        self.next = None
 
 
class GraphRantaiPasok: # Class utama untuk membuat dan mengelola graf distribusi pangan.
    def __init__(self):
        self.adj = {}
        self.tipe_node = {}
 
    def tambah_node(self, node_id, tipe):
        if node_id not in self.adj:
            self.adj[node_id] = None
            self.tipe_node[node_id] = tipe
 
    def tambah_jalur(self, u, v, jarak, biaya_km):
        new_edge = Edge(v, jarak, biaya_km)
        new_edge.next = self.adj[u]
        self.adj[u] = new_edge
 
        new_edge = Edge(u, jarak, biaya_km)
        new_edge.next = self.adj[v]
        self.adj[v] = new_edge
 
    def tetangga(self, u):
        neighbors = []
        current = self.adj.get(u, None)
        while current:
            neighbors.append((current.dest, current.jarak_km, current.biaya_per_km))
            current = current.next
        return neighbors
 
 
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
