# circular_queue_buffer.py
# Setiap node memiliki Circular Queue berbasis array (fixed capacity=50)
# untuk menyimpan produk secara FIFO
# Big-O: enqueue O(1), dequeue O(1), is_full O(1)
 
class CircularQueue:
    def __init__(self, kapasitas=50):
        self.kapasitas = kapasitas
        self.buffer = [None] * kapasitas
        self.front = 0
        self.rear = 0
        self._size = 0
 
    def enqueue(self, produk):
        """Memasukkan produk ke buffer (FIFO)"""
        if self.is_full():
            return False
        self.buffer[self.rear] = produk
        self.rear = (self.rear + 1) % self.kapasitas
        self._size += 1
        return True
 
    def dequeue(self):
        """Mengeluarkan produk dari buffer (FIFO)"""
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
    
    def clear(self):
        """Mengosongkan buffer"""
        self.buffer = [None] * self.kapasitas
        self.front = 0
        self.rear = 0
        self._size = 0
