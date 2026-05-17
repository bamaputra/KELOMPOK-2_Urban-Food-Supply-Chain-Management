"""
Module 3: Priority Queue Pengiriman
Prioritas pengiriman: MENDESAK (masa kadaluarsa <= 3 hari), 
NORMAL (4-7 hari), REGULER (>7 hari)
Mendukung: KIRIM (enqueue), PROSES_KIRIM (dequeue & eksekusi)
Big-O: enqueue O(n), dequeue O(1)
"""

class LLNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class PriorityQueueKirim:
    def __init__(self):
        self.head = None
        self._size = 0

    def enqueue(self, pengiriman):
        """
        Memasukkan pengiriman ke antrian prioritas - Big-O: O(n)
        Prioritas: 1 (MENDESAK) > 2 (NORMAL) > 3 (REGULER)
        """
        new_node = LLNode(pengiriman)
        if self.head is None or pengiriman.prioritas < self.head.data.prioritas:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next is not None and current.next.data.prioritas <= pengiriman.prioritas:
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self._size += 1

    def dequeue(self):
        """Mengeluarkan pengiriman prioritas tertinggi - Big-O: O(1)"""
        if self.head is None:
            return None
        pengiriman = self.head.data
        self.head = self.head.next
        self._size -= 1
        return pengiriman

    def __len__(self):
        return self._size

    def is_empty(self):
        return self.head is None

    def peek(self):
        """Melihat pengiriman dengan prioritas tertinggi tanpa menghapus"""
        return self.head.data if self.head else None

    def get_all(self):
        """Mendapatkan semua pengiriman dalam antrian"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result


class Stack:
    """Stack untuk menyimpan log transaksi"""
    
    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, data):
        new_node = LLNode(data)
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

    def get_all(self):
        """Mendapatkan semua data dalam stack (dari oldest ke newest)"""
        result = []
        temp_stack = Stack()
        while not self.is_empty():
            temp_stack.push(self.pop())
        while not temp_stack.is_empty():
            data = temp_stack.pop()
            result.append(data)
            self.push(data)
        return result

    
