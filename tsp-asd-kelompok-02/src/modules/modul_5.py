def dijkstra_biaya(graph, asal):
    """
    Dijkstra dari node sumber menggunakan bobot = jarak * biaya_km
    Big-O: O(V^2 + E)
    """
    INF = float('inf')
    dist = {v: INF for v in graph.adj}
    parent = {v: None for v in graph.adj}
    dist[asal] = 0.0
    visited = set()
