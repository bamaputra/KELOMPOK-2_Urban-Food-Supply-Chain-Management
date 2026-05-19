from test_linked_list import LLNode
 
class CircularQueue:
    def __init__(self, kapasitas):
        self.kapasitas = kapasitas
        self.buffer = [None] * kapasitas
        self.front = 0
        self.rear = 0
        self._size = 0
 
    def enqueue(self, produk):
        if self.is_full():
            return False
        self.buffer[self.rear] = produk
        self.rear = (self.rear + 1) % self.kapasitas
        self._size += 1
        return True
 
    def dequeue(self):
        if self.is_empty():
            return None
        produk = self.buffer[self.front]
        self.buffer[self.front] = None
        self.front = (self.front + 1) % self.kapasitas
        self._size -= 1
        return produk
 
    def is_full(self):
        return self._size == self.kapasitas
 
    def is_empty(self):
        return self._size == 0
 
    def __len__(self):
        return self._size
 
    def get_all(self):
        result = []
        if self.is_empty():
            return result
        idx = self.front
        for _ in range(self._size):
            if self.buffer[idx] is not None:
                result.append(self.buffer[idx])
            idx = (idx + 1) % self.kapasitas
        return result
 
 
class PriorityQueueKirim:
    def __init__(self):
        self.head = None
        self._size = 0
 
    def enqueue(self, pengiriman):
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
 

