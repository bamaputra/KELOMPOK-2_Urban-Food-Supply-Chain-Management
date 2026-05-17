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
            while (current.next is not None
                   and current.next.data.prioritas <= pengiriman.prioritas):
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

