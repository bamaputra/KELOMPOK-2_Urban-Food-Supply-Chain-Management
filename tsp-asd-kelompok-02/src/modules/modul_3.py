# modul3_priority_queue.py
 
class LLNode:
    """Linked list node untuk priority queue"""
    def __init__(self, data=None):
        self.data = data
        self.next = None
 
 
class PriorityQueueKirim:
    """
    Prioritas pengiriman: 
    MENDESAK (masa kadaluarsa <= 3 hari), 
    NORMAL (4-7 hari), 
    REGULER (>7 hari).
    Mendukung: KIRIM (enqueue), PROSES_KIRIM (dequeue & eksekusi).
    Produk MENDESAK selalu dikirim lebih dulu.
    Big-O: enqueue O(n), dequeue O(1).
    """
    
    def __init__(self):
        self.head = None
        self._size = 0
 
    def enqueue(self, pengiriman):
        """
        Memasukkan pengiriman ke antrian prioritas - O(n)
        Prioritas: 1 (MENDESAK) > 2 (NORMAL) > 3 (REGULER)
        """
        new_node = LLNode(pengiriman)
        if self.head is None or pengiriman.prioritas < self.head.data.prioritas:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while (current.next is not None
                   and current.next.data.prioritas <= pengiriman.prioritas):
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self._size += 1
 
    def dequeue(self):
        """Mengeluarkan pengiriman prioritas tertinggi - O(1)"""
        if self.head is None:
            return None
        pengiriman = self.head.data
        self.head = self.head.next
        self._size -= 1
        return pengiriman
 
    def peek(self):
        """Melihat pengiriman prioritas tertinggi tanpa menghapus"""
        if self.head is None:
            return None
        return self.head.data
 
    def __len__(self):
        return self._size
 
    def is_empty(self):
        return self.head is None
 
    def get_all(self):
        """Mendapatkan semua pengiriman dalam antrian (untuk display)"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
 
 
def hitung_prioritas(masa_kadaluarsa):
    """Helper function untuk menghitung prioritas berdasarkan masa kadaluarsa"""
    if masa_kadaluarsa <= 3:
        return 1  # MENDESAK
    elif masa_kadaluarsa <= 7:
        return 2  # NORMAL
    else:
        return 3  # REGULER
 
 
def get_prioritas_text(prioritas):
    """Mendapatkan teks prioritas"""
    return {1: 'MENDESAK', 2: 'NORMAL', 3: 'REGULER'}.get(prioritas, 'UNKNOWN')

    
