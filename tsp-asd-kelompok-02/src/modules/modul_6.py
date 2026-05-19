# modul6_cli.py
import random
import time
from typing import List, Tuple
 
# Import dari modul lain
from modul1_graph import GraphRantaiPasok
from modul2_circular_queue import CircularQueue
from modul3_priority_queue import PriorityQueueKirim, hitung_prioritas, get_prioritas_text
from modul4_bst_katalog import BSTKatalog, Produk
from modul5_dijkstra import dijkstra_biaya, get_path
 
 
# Data kelas tambahan
@dataclass
class Pengiriman:
    pengiriman_id: int
    dari_node: str
    ke_node: str
    kode_produk: str
    jumlah: int
    prioritas: int
    waktu_kirim: float
 
 
# Stack untuk log transaksi (menggunakan linked list sederhana)
class LLNodeLog:
    def __init__(self, data=None):
        self.data = data
        self.next = None
 
 
class Stack:
    def __init__(self):
        self.top = None
        self._size = 0
 
    def push(self, data):
        new_node = LLNodeLog(data)
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
 
    def is_empty(self):
        return self.top is None
 
 
# Generator Rantai Pasok
KATEGORI_PRODUK = ['SAYUR', 'BUAH', 'DAGING', 'IKAN', 'BAHAN_POKOK']
TIPE_NODE = ['PETANI', 'DISTRIBUTOR', 'PASAR', 'GUDANG']
 
 
def generate_rantai_pasok(seed=61):
    """Generate rantai pasok tanpa numpy"""
    random.seed(seed)
 
    nodes = []
    # 10 petani
    for i in range(10):
