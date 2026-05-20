# cli_rantai_pasok.py
# Implementasi CLI untuk sistem rantai pasok
# Perintah: KIRIM, PROSES_KIRIM, RUTE_MURAH, CEK_STOK, KADALUARSA, 
#           LAPORAN_DISTRIBUSI, BUFFER, KELUAR
 
import random
import time
from graph_rantai_pasok import GraphRantaiPasok
from circular_queue_buffer import CircularQueue
from priority_queue_pengiriman import PriorityQueueKirim, Pengiriman, hitung_prioritas, get_prioritas_text
from bst_katalog_produk import BSTKatalog, Produk
from dijkstra_biaya import dijkstra_biaya, get_path, tampilkan_rute_dengan_biaya
 
# Konstanta
KATEGORI_PRODUK = ['SAYUR', 'BUAH', 'DAGING', 'IKAN', 'BAHAN_POKOK']
TIPE_NODE = ['PETANI', 'DISTRIBUTOR', 'PASAR', 'GUDANG']
 
 
class Stack:
    """Stack untuk log transaksi (Linked List)"""
    class LLNode:
        def __init__(self, data=None):
            self.data = data
            self.next = None
 
    def __init__(self):
        self.top = None
        self._size = 0
 
    def push(self, data):
        new_node = self.LLNode(data)
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
 
 
def generate_rantai_pasok(seed=61):
    """Generate rantai pasok dengan struktur hierarki yang jelas"""
    random.seed(seed)
    
    petani = [f'PTN{i:02d}' for i in range(10)]
    distributor = [f'DST{i:02d}' for i in range(5)]
    pasar = [f'PSR{i:02d}' for i in range(8)]
    gudang = [f'GDG{i:02d}' for i in range(3)]
    
    nodes = []
    for p in petani:
        nodes.append((p, 'PETANI'))
    for d in distributor:
        nodes.append((d, 'DISTRIBUTOR'))
    for p in pasar:
        nodes.append((p, 'PASAR'))
    for g in gudang:
        nodes.append((g, 'GUDANG'))
    
    edges = []
    
    # JALUR HIERARKI YANG TERSTRUKTUR
    # 1. PETANI → DISTRIBUTOR
    for p in petani:
        num_connections = random.randint(2, 3)
        distributors_connected = random.sample(distributor, num_connections)
        for d in distributors_connected:
            jarak = random.randint(10, 100)
            biaya = round(random.uniform(500, 2000), 0)
            edges.append((p, d, jarak, biaya))
    
    # 2. DISTRIBUTOR → DISTRIBUTOR
    for i, d1 in enumerate(distributor):
        for d2 in distributor[i+1:]:
            if random.random() < 0.4:
                jarak = random.randint(20, 150)
                biaya = round(random.uniform(800, 2500), 0)
                edges.append((d1, d2, jarak, biaya))
                edges.append((d2, d1, jarak, biaya))
    
    # 3. DISTRIBUTOR → PASAR
    for d in distributor:
        num_connections = random.randint(3, 4)
        markets_connected = random.sample(pasar, min(num_connections, len(pasar)))
        for m in markets_connected:
            jarak = random.randint(5, 80)
            biaya = round(random.uniform(400, 1500), 0)
            edges.append((d, m, jarak, biaya))
    
    # 4. DISTRIBUTOR → GUDANG
    for d in distributor:
        num_connections = random.randint(1, 2)
        warehouses_connected = random.sample(gudang, min(num_connections, len(gudang)))
        for g in warehouses_connected:
            jarak = random.randint(10, 60)
            biaya = round(random.uniform(300, 1200), 0)
            edges.append((d, g, jarak, biaya))
    
    # 5. GUDANG → PASAR
    for g in gudang:
        num_connections = random.randint(2, 3)
        markets_connected = random.sample(pasar, min(num_connections, len(pasar)))
        for m in markets_connected:
            jarak = random.randint(5, 50)
            biaya = round(random.uniform(300, 1000), 0)
            edges.append((g, m, jarak, biaya))
    
    # 6. PETANI → GUDANG (opsional)
    for p in petani:
        if random.random() < 0.3:
            g = random.choice(gudang)
            jarak = random.randint(15, 80)
            biaya = round(random.uniform(600, 1800), 0)
            edges.append((p, g, jarak, biaya))
    
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
 
 
def main():
    graph = GraphRantaiPasok()
    bst_katalog = BSTKatalog()
    pg_kirim = PriorityQueueKirim()
    log_transaksi = Stack()
    buffer_gudang = {}
    kirim_counter = 0
 
    nodes, edges, produk_list = generate_rantai_pasok(seed=61)
 
    # Tambahkan semua node
    for nid, tipe in nodes:
        graph.tambah_node(nid, tipe)
        buffer_gudang[nid] = CircularQueue(kapasitas=50)
 
    # Tambahkan semua edge
    for u, v, j, b in edges:
        graph.tambah_jalur(u, v, j, b)
 
    # Tambahkan produk ke BST
    for p in produk_list:
        bst_katalog.insert(p)
 
    # Tampilkan banner
    print('=' * 75)
    print('  🏭 FOOD SUPPLY CHAIN MANAGEMENT SYSTEM 🏪')
    print('  Sistem Manajemen Rantai Pasok Bahan Makanan')
    print('=' * 75)
    print(f'\n📊 STATISTIK SISTEM:')
    print(f'  ├─ Total Node      : {len(nodes)}')
    print(f'  │  ├─ PETANI       : {sum(1 for _, t in nodes if t == "PETANI")}')
    print(f'  │  ├─ DISTRIBUTOR  : {sum(1 for _, t in nodes if t == "DISTRIBUTOR")}')
    print(f'  │  ├─ PASAR        : {sum(1 for _, t in nodes if t == "PASAR")} (sink only)')
    print(f'  │  └─ GUDANG       : {sum(1 for _, t in nodes if t == "GUDANG")}')
    print(f'  ├─ Total Produk    : {len(produk_list)}')
    print(f'  ├─ Total Jalur     : {len(edges)}')
    print(f'  └─ Struktur        : Hierarkis dengan PASAR sebagai sink node')
    
    print('\n' + '=' * 75)
    print('📝 DAFTAR PERINTAH:')
    print('  KIRIM <dari> <ke> <kode> <jumlah>')
    print('  PROSES_KIRIM')
    print('  RUTE_MURAH <dari> <ke>')
    print('  CEK_STOK <kode>')
    print('  KADALUARSA <maks_hari>')
    print('  LAPORAN_DISTRIBUSI')
    print('  BUFFER <node>')
    print('  INFO_JARINGAN')
    print('  CEK_KONEKSI <dari> <ke>')
    print('  BANTUAN')
    print('  KELUAR')
    print('=' * 75)
 
    while True:
        try:
            cmd = input('\n🍽️  [SCM] > ').strip().split()
            if not cmd:
                continue
 
            if cmd[0].upper() == 'KELUAR':
                print('\n👋 Terima kasih telah menggunakan sistem manajemen rantai pasok!')
                print('   Total transaksi diproses:', len(log_transaksi))
                break
 
            elif cmd[0].upper() == 'BANTUAN':
                print('\n' + '=' * 75)
                print('📖 DAFTAR PERINTAH LENGKAP:')
                print('=' * 75)
                print('  KIRIM <dari> <ke> <kode> <jumlah>')
                print('      → Tambah pengiriman ke antrian (prioritas: MENDESAK/NORMAL/REGULER)')
                print('  PROSES_KIRIM')
                print('      → Proses pengiriman prioritas tertinggi')
                print('  RUTE_MURAH <dari> <ke>')
                print('      → Cari rute dengan biaya terendah')
                print('  CEK_STOK <kode>')
                print('      → Cek stok dan info produk')
                print('  KADALUARSA <maks_hari>')
                print('      → Filter produk berdasarkan kadaluarsa')
                print('  LAPORAN_DISTRIBUSI')
                print('      → Lihat histori transaksi')
                print('  BUFFER <node>')
                print('      → Lihat buffer gudang')
                print('  INFO_JARINGAN')
                print('      → Informasi struktur jaringan')
                print('  CEK_KONEKSI <dari> <ke>')
                print('      → Cek koneksi langsung antar node')
                print('  BANTUAN')
                print('      → Tampilkan bantuan ini')
                print('  KELUAR')
                print('      → Keluar dari aplikasi')
                print('=' * 75)
 
            elif cmd[0].upper() == 'INFO_JARINGAN':
                print('\n' + '=' * 75)
                print('🌐 INFORMASI JARINGAN RANTAI PASOK')
                print('=' * 75)
                print('\n📋 DAFTAR NODE:')
                print(f'  {"ID":<10} {"TIPE":<14} {"Status":<15} {"Outgoing Edges":>15}')
                print('  ' + '-' * 60)
                for nid, tipe in nodes:
                    status = '✅ Bisa Kirim' if tipe != 'PASAR' else '⛔ Sink Only'
                    jml = len(graph.tetangga(nid))
                    print(f'  {nid:<10} {tipe:<14} {status:<15} {jml:>15}')
                print('=' * 75)
 
            elif cmd[0].upper() == 'KIRIM':
                if len(cmd) != 5:
                    print('❌ Format salah! Gunakan: KIRIM <dari> <ke> <kode> <jumlah>')
                    continue
 
                _, dari, ke, kode, jumlah_str = cmd
                try:
                    jumlah = int(jumlah_str)
                except ValueError:
                    print('❌ Jumlah harus berupa angka!')
                    continue
 
                if jumlah <= 0:
                    print('❌ Jumlah harus lebih dari 0!')
                    continue
 
                if dari not in graph.adj or ke not in graph.adj:
                    print(f'❌ Node tidak ditemukan! (cek: {dari} atau {ke})')
                    continue
 
                if graph.tipe_node.get(dari) == 'PASAR':
                    print(f'❌ DITOLAK! Node {dari} adalah PASAR.')
                    print('   PASAR hanya bisa MENERIMA produk, tidak bisa MENGIRIM!')
                    continue
 
                produk = bst_katalog.search(kode)
                if not produk:
                    print(f'❌ Produk dengan kode {kode} tidak ditemukan!')
                    continue
 
                if produk.stok < jumlah:
                    print(f'❌ Stok tidak mencukupi! Stok tersedia: {produk.stok}')
                    continue
 
                bst_katalog.update_stok(kode, -jumlah)
 
                prioritas = hitung_prioritas(produk.masa_kadaluarsa_hari)
                prioritas_text = get_prioritas_text(prioritas)
 
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
 
                print(f'\n✅ Pengiriman #{kirim_counter} ditambahkan ke antrian')
                print(f'   📦 Produk: {produk.nama} (ID: {kode}) x{jumlah}')
                print(f'   ⚡ Prioritas: {prioritas_text}')
 
            elif cmd[0].upper() == 'PROSES_KIRIM':
                if pg_kirim.is_empty():
                    print('📭 Tidak ada pengiriman dalam antrian')
                    continue
 
                pengiriman = pg_kirim.dequeue()
                if not pengiriman:
                    print('❌ Gagal memproses pengiriman')
                    continue
 
                dist, parent = dijkstra_biaya(graph, pengiriman.dari_node)
                if dist.get(pengiriman.ke_node, float('inf')) == float('inf'):
                    print(f'❌ Pengiriman #{pengiriman.pengiriman_id} GAGAL!')
                    print(f'   Tidak ada jalur dari {pengiriman.dari_node} ke {pengiriman.ke_node}')
                    bst_katalog.update_stok(pengiriman.kode_produk, pengiriman.jumlah)
                    continue
 
                tipe_tujuan = graph.tipe_node.get(pengiriman.ke_node, '')
                if tipe_tujuan == 'GUDANG':
                    produk = bst_katalog.search(pengiriman.kode_produk)
                    if produk:
                        success = buffer_gudang[pengiriman.ke_node].enqueue(produk)
                        if success:
                            print(f'  📦 → Produk disimpan ke buffer gudang {pengiriman.ke_node}')
                        else:
                            print(f'  ⚠️  → Buffer gudang {pengiriman.ke_node} penuh!')
                elif tipe_tujuan == 'PASAR':
                    print(f'  🏪 → Produk diterima oleh PASAR {pengiriman.ke_node}')
                else:
                    print(f'  📍 → Produk diterima oleh {pengiriman.ke_node} ({tipe_tujuan})')
 
                log_entry = (f'[ID:{pengiriman.pengiriman_id:04d}] '
                            f'{pengiriman.dari_node} → {pengiriman.ke_node} | '
                            f'{pengiriman.kode_produk} x{pengiriman.jumlah} | '
                            f'Prioritas:{get_prioritas_text(pengiriman.prioritas)}')
                log_transaksi.push(log_entry)
 
                print(f'\n✅ Pengiriman #{pengiriman.pengiriman_id} berhasil diproses!')
 
            elif cmd[0].upper() == 'RUTE_MURAH':
                if len(cmd) != 3:
                    print('❌ Format salah! Gunakan: RUTE_MURAH <dari> <ke>')
                    continue
 
                _, dari, ke = cmd
 
                if dari not in graph.adj or ke not in graph.adj:
                    print(f'❌ Node tidak ditemukan!')
                    continue
 
                if graph.tipe_node.get(dari) == 'PASAR':
                    print(f'❌ DITOLAK! Node {dari} adalah PASAR.')
                    continue
 
                dist, parent = dijkstra_biaya(graph, dari)
 
                if dist.get(ke, float('inf')) == float('inf'):
                    print(f'\n❌ TIDAK ADA JALUR dari {dari} ke {ke}')
                    continue
 
                path = get_path(parent, ke)
                segments, total_biaya = tampilkan_rute_dengan_biaya(graph, path)
                
                print(f'\n✨ RUTE TERMURAH dari {dari} ke {ke}:')
                print('=' * 75)
                for i, seg in enumerate(segments, 1):
                    print(f'    {i}. {seg["from"]} → {seg["to"]}')
                    print(f'       📏 Jarak: {seg["jarak"]} km | 💰 Biaya/km: Rp {seg["biaya_km"]:,.0f}')
                    print(f'       💵 Biaya segmen: Rp {seg["biaya"]:,.2f}')
                print(f'\n  📊 TOTAL BIAYA: Rp {total_biaya:,.2f}')
                print('=' * 75)
 
            elif cmd[0].upper() == 'CEK_KONEKSI':
                if len(cmd) != 3:
                    print('❌ Format salah! Gunakan: CEK_KONEKSI <dari> <ke>')
                    continue
                
                _, dari, ke = cmd
                
                if dari not in graph.adj or ke not in graph.adj:
                    print(f'❌ Node tidak ditemukan!')
                    continue
                
                print(f'\n🔍 CEK KONEKSI: {dari} → {ke}')
                print('=' * 50)
                
                tetangga = graph.tetangga(dari)
                langsung = False
                for n, j, b in tetangga:
                    if n == ke:
                        langsung = True
                        print(f'✅ ADA koneksi LANGSUNG!')
                        print(f'   📏 Jarak: {j} km')
                        print(f'   💰 Biaya per km: Rp {b:,.0f}')
                        break
                
                if not langsung:
                    print(f'❌ TIDAK ADA koneksi langsung dari {dari} ke {ke}')
                
                dist, _ = dijkstra_biaya(graph, dari)
                if dist.get(ke, float('inf')) != float('inf'):
                    print(f'\n✅ Tersedia jalur TIDAK LANGSUNG')
                    print(f'   💰 Estimasi biaya minimal: Rp {dist[ke]:,.2f}')
                else:
                    print(f'\n❌ TIDAK ADA jalur sama sekali')
                print('=' * 50)
 
            elif cmd[0].upper() == 'CEK_STOK':
                if len(cmd) != 2:
                    print('❌ Format salah! Gunakan: CEK_STOK <kode>')
                    continue
 
                _, kode = cmd
                produk = bst_katalog.search(kode)
 
                if not produk:
                    print(f'❌ Produk dengan kode {kode} tidak ditemukan!')
                else:
                    print(f'\n📦 DETAIL PRODUK:')
                    print('=' * 50)
                    print(f'  Kode          : {produk.kode}')
                    print(f'  Nama          : {produk.nama}')
                    print(f'  Kategori      : {produk.kategori}')
                    print(f'  Harga         : Rp {produk.harga_satuan:,.2f}')
                    print(f'  Stok          : {produk.stok} unit')
                    print(f'  Kadaluarsa    : {produk.masa_kadaluarsa_hari} hari')
                    print(f'  Prioritas     : {get_prioritas_text(hitung_prioritas(produk.masa_kadaluarsa_hari))}')
                    print('=' * 50)
 
            elif cmd[0].upper() == 'KADALUARSA':
                if len(cmd) != 2:
                    print('❌ Format salah! Gunakan: KADALUARSA <maks_hari>')
                    continue
 
                try:
                    maks_hari = int(cmd[1])
                except ValueError:
                    print('❌ Maks hari harus berupa angka!')
                    continue
 
                produk_kadaluarsa = bst_katalog.filter_kadaluarsa(maks_hari)
 
                if not produk_kadaluarsa:
                    print(f'✅ Tidak ada produk dengan masa kadaluarsa <= {maks_hari} hari')
                else:
                    print(f'\n⚠️  PRODUK DENGAN KADALUARSA <= {maks_hari} HARI:')
                    print('=' * 75)
                    print(f'  {"Kode":<10} {"Nama":<15} {"Stok":>5} {"Kadaluarsa":>12} {"Status":<15}')
                    print('-' * 75)
                    for p in produk_kadaluarsa:
                        if p.masa_kadaluarsa_hari <= 3:
                            status = '🔴 MENDESAK!'
                        elif p.masa_kadaluarsa_hari <= 7:
                            status = '🟡 Perhatikan'
                        else:
                            status = '🟢 Normal'
                        print(f'  {p.kode:<10} {p.nama:<15} {p.stok:>5} {p.masa_kadaluarsa_hari:>8} hari  {status:<15}')
                    print('=' * 75)
 
            elif cmd[0].upper() == 'LAPORAN_DISTRIBUSI':
                print('\n' + '=' * 75)
                print('📋 LAPORAN TRANSAKSI DISTRIBUSI')
                print('=' * 75)
 
                transaksi_list = []
                temp_stack = Stack()
                while not log_transaksi.is_empty():
                    transaksi = log_transaksi.pop()
                    transaksi_list.append(transaksi)
                    temp_stack.push(transaksi)
 
                while not temp_stack.is_empty():
                    log_transaksi.push(temp_stack.pop())
 
                if not transaksi_list:
                    print('📭 Belum ada transaksi distribusi')
                else:
                    print(f'\n  Total {len(transaksi_list)} transaksi:\n')
                    for i, transaksi in enumerate(reversed(transaksi_list), 1):
                        print(f'  {i:2}. {transaksi}')
                print('=' * 75)
 
            elif cmd[0].upper() == 'BUFFER':
                if len(cmd) != 2:
                    print('❌ Format salah! Gunakan: BUFFER <node>')
                    continue
 
                _, node = cmd
 
                if node not in buffer_gudang:
                    print(f'❌ Node {node} tidak ditemukan!')
                    continue
 
                tipe_node = graph.tipe_node.get(node, '')
                buffer = buffer_gudang[node]
 
                if buffer.is_empty():
                    print(f'📭 Buffer {node} ({tipe_node}) kosong')
                else:
                    print(f'\n📦 ISI BUFFER {node} ({tipe_node}):')
                    print('-' * 60)
                    for i, p in enumerate(buffer.get_all(), 1):
                        print(f'  {i}. {p.kode} | {p.nama:<15} | Kadaluarsa: {p.masa_kadaluarsa_hari} hari')
                    print(f'\n  📊 Kapasitas: {len(buffer)}/{buffer.kapasitas} ({len(buffer)*100//buffer.kapasitas}%)')
                    print('-' * 60)
 
            else:
                print(f'❌ Perintah tidak dikenal: {cmd[0]}')
                print('   Ketik BANTUAN untuk melihat daftar perintah yang tersedia')
 
        except KeyboardInterrupt:
            print('\n\n👋 Keluar dari sistem...')
            break
        except Exception as e:
            print(f'❌ Terjadi kesalahan: {e}')
 
 
if __name__ == '__main__':
    main()
