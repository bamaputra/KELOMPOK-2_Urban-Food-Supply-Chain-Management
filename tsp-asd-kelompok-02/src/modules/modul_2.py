# modul2_circular_queue.py
 
class CircularQueue:
    """
    Setiap node memiliki Circular Queue berbasis array (fixed capacity=50)
    untuk menyimpan produk secara FIFO.
    Produk masuk (enqueue) dari supplier, keluar (dequeue) ke tujuan berikutnya.
    Prinsip FIFO mencegah penumpukan produk lama.
    Big-O: enqueue O(1), dequeue O(1), is_full O(1).
    """
    
    def __init__(self, kapasitas=50):
        self.kapasitas = kapasitas
        self.buffer = [None] * kapasitas
        self.front = 0
        self.rear = 0
        self._size = 0
 
    def enqueue(self, produk):
        """Memasukkan produk ke buffer - O(1)"""
        if self.is_full():
            return False
        self.buffer[self.rear] = produk
        self.rear = (self.rear + 1) % self.kapasitas
        self._size += 1
        return True
 
    def dequeue(self):
        """Mengeluarkan produk dari buffer - O(1)"""
        if self.is_empty():
            return None
        produk = self.buffer[self.front]
        self.buffer[self.front] = None
        self.front = (self.front + 1) % self.kapasitas
        self._size -= 1
        return produk
 
    def is_full(self):
        """Cek apakah buffer penuh - O(1)"""
        return self._size == self.kapasitas
 
    def is_empty(self):
        """Cek apakah buffer kosong - O(1)"""
        return self._size == 0
 
    def __len__(self):
        return self._size
 
    def get_all(self):
        """Mendapatkan semua isi buffer (untuk display)"""
        result = []
        if self.is_empty():
            return result
        idx = self.front
        for _ in range(self._size):
            if self.buffer[idx] is not None:
                result.append(self.buffer[idx])
            idx = (idx + 1) % self.kapasitas
        return result
 
    def peek(self):
        """Melihat produk terdepan tanpa menghapus"""
        if self.is_empty():
            return None
        return self.buffer[self.front]
