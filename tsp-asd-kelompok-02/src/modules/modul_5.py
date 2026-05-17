"""
Module 5: Dijkstra Biaya Minimum
Dijkstra dari setiap node sumber menggunakan bobot = jarak * biaya_km
untuk mencari jalur distribusi termurah
Rekonstruksi jalur dan tampilkan total biaya perjalanan
Audit biaya: urutkan jalur berdasarkan biaya menggunakan Merge Sort
Big-O: O(V^2 + E)
"""

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


def get_path(parent, target):
    """Rekonstruksi jalur dari parent array"""
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = parent.get(current, None)
    return list(reversed(path))


def hitung_prioritas(masa_kadaluarsa):
    """
    Hitung prioritas pengiriman berdasarkan masa kadaluarsa
    MENDESAK: <= 3 hari -> prioritas 1
    NORMAL: 4-7 hari -> prioritas 2
    REGULER: > 7 hari -> prioritas 3
    """
    if masa_kadaluarsa <= 3:
        return 1  # MENDESAK
    elif masa_kadaluarsa <= 7:
        return 2  # NORMAL
    else:
        return 3  # REGULER


def prioritas_to_text(prioritas):
    """Konversi nilai prioritas ke teks"""
    return {1: 'MENDESAK', 2: 'NORMAL', 3: 'REGULER'}.get(prioritas, 'UNKNOWN')


def merge_sort_jalur(jalur_list):
    """
    Merge Sort untuk mengurutkan jalur berdasarkan biaya
    Digunakan untuk audit biaya
    """
    if len(jalur_list) <= 1:
        return jalur_list
    
    mid = len(jalur_list) // 2
    left = merge_sort_jalur(jalur_list[:mid])
    right = merge_sort_jalur(jalur_list[mid:])
    
    return _merge(left, right)


def _merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i][1] <= right[j][1]:  # bandingkan biaya
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def hitung_semua_rute_biaya(graph):
    """
    Menghitung semua rute termurah antar node
    untuk audit biaya
    """
    nodes = graph.get_all_nodes()
    semua_rute = []
    
    for asal in nodes:
        dist, _ = dijkstra_biaya(graph, asal)
        for tujuan in nodes:
            if asal != tujuan and dist[tujuan] != float('inf'):
                semua_rute.append((f"{asal}->{tujuan}", dist[tujuan]))
    
    return merge_sort_jalur(semua_rute)

