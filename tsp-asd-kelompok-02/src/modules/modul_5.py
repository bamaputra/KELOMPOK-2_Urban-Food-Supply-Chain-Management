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
     while len(visited) < len(graph.adj):
        # Cari node dengan jarak minimum yang belum dikunjungi
        min_dist = INF
        u = None
        for v in graph.adj:
            if v not in visited and dist[v] < min_dist:
                min_dist = dist[v]
                u = v

        if u is None:
            break

        visited.add(u)

        # Update jarak ke tetangga
        current = graph.adj[u]
        while current:
            v = current.dest
            if v not in visited:
                # Bobot = jarak * biaya_per_km
                weight = current.jarak_km * current.biaya_per_km
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    parent[v] = u
            current = current.next

    return dist, parent

