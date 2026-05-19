from test_linked_list import LLNode
 
class Stack:
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
 

