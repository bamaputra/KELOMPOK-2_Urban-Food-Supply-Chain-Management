# dijkstra_biaya.py
# Dijkstra dari setiap node sumber menggunakan bobot = jarak * biaya_km
# untuk mencari jalur distribusi termurah
# Rekonstruksi jalur dan tampilkan total biaya perjalanan
# Audit biaya: urutkan jalur berdasarkan biaya menggunakan Merge Sort
# Big-O: O(V^2 + E)
 
def dijkstra_biaya(graph, asal):
    """
    Mencari jalur terpendek (termurah) dari asal ke semua node
    Menggunakan bobot = jarak_km * biaya_per_km
    """
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
    """Merekontruksi jalur dari source ke target"""
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = parent.get(current, None)
    return list(reversed(path))
 
 
def tampilkan_rute_dengan_biaya(graph, path):
    """Menampilkan rute dengan biaya per segmen"""
    total_biaya = 0
    segments = []
    
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
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
        if left[i]['total_biaya'] <= right[j]['total_biaya']:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result
 
 
def audit_semua_rute(graph, sumber_list):
    """
    Melakukan audit biaya untuk semua rute dari sumber tertentu
    """
    all_routes = []
    
    for sumber in sumber_list:
        dist, parent = dijkstra_biaya(graph, sumber)
        for tujuan in graph.get_all_nodes():
            if tujuan != sumber and dist.get(tujuan, float('inf')) != float('inf'):
                path = get_path(parent, tujuan)
                segments, total_biaya = tampilkan_rute_dengan_biaya(graph, path)
                all_routes.append({
                    'sumber': sumber,
                    'tujuan': tujuan,
                    'total_biaya': total_biaya,
                    'jalur': path,
                    'segments': segments
                })
    
    return merge_sort_jalur(all_routes)
