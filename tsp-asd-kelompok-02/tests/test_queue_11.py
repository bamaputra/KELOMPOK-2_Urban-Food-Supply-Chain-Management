# PRIORITY QUEUE PENGIRIMAN
# Urban Food Supply Chain Management
# Struktur Data: Priority Queue menggunakan Linked List

# =========================================================
# DATA PENGIRIMAN
# =========================================================
class Pengiriman:
    def __init__(self, pengiriman_id, nama_produk, jumlah, prioritas):
        self.pengiriman_id = pengiriman_id
        self.nama_produk = nama_produk
        self.jumlah = jumlah
        self.prioritas = prioritas

    def __str__(self):
        status = {
            1: "MENDESAK",
            2: "NORMAL",
            3: "REGULER"
        }

        return (f"[ID:{self.pengiriman_id}] "
                f"{self.nama_produk} x{self.jumlah} "
                f"| Prioritas: {status[self.prioritas]}")


# =========================================================
# LINKED LIST NODE
# =========================================================
class LLNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None


# =========================================================
# PRIORITY QUEUE
# =========================================================
class PriorityQueueKirim:
    def __init__(self):
        self.head = None
        self._size = 0

    # =====================================================
    # MENAMBAHKAN DATA BERDASARKAN PRIORITAS
    # =====================================================
    def enqueue(self, pengiriman):

        new_node = LLNode(pengiriman)

        # Jika queue kosong
        # atau prioritas lebih tinggi
        if (self.head is None or
                pengiriman.prioritas < self.head.data.prioritas):

            new_node.next = self.head
            self.head = new_node

        else:
            current = self.head

            # Cari posisi yang sesuai
            while (current.next is not None and
                   current.next.data.prioritas <= pengiriman.prioritas):

                current = current.next

            # Sisipkan node
            new_node.next = current.next
            current.next = new_node

        self._size += 1

    # =====================================================
    # MENGAMBIL DATA PRIORITAS TERTINGGI
    # =====================================================
    def dequeue(self):

        if self.head is None:
            return None

        pengiriman = self.head.data

        self.head = self.head.next

        self._size -= 1

        return pengiriman

    # =====================================================
    # CEK KOSONG
    # =====================================================
    def is_empty(self):
        return self.head is None

    # =====================================================
    # JUMLAH DATA
    # =====================================================
    def __len__(self):
        return self._size

    # =====================================================
    # TAMPILKAN ISI QUEUE
    # =====================================================
    def tampilkan(self):

        if self.is_empty():
            print("Queue kosong")
            return

        current = self.head

        print("\nIsi Priority Queue:")
        print("-" * 50)

        while current:
            print(current.data)
            current = current.next

        print("-" * 50)


# =========================================================
# MAIN PROGRAM
# =========================================================
def main():

    queue = PriorityQueueKirim()

    # Tambah data pengiriman
    p1 = Pengiriman(1, "Cabai", 20, 2)
    p2 = Pengiriman(2, "Tomat", 15, 1)
    p3 = Pengiriman(3, "Beras", 50, 3)
    p4 = Pengiriman(4, "Ayam", 10, 1)

    queue.enqueue(p1)
    queue.enqueue(p2)
    queue.enqueue(p3)
    queue.enqueue(p4)

    # Tampilkan queue
    queue.tampilkan()

    print("\nProses Pengiriman")
    print("=" * 50)

    # Proses queue
    while not queue.is_empty():

        proses = queue.dequeue()

        print(f"Memproses -> {proses}")

    print("\nSemua pengiriman selesai")


# =========================================================
# JALANKAN PROGRAM
# =========================================================
if __name__ == "__main__":
    main()
