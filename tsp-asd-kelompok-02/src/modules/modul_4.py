# bst_katalog.py
from models import product 
class bst node 

if (  def init unit  self. root

def _search_rec(self, node, kode):
        if node is None or node.produk.kode == kode:
            return node.produk if node else None
        if kode < node.produk.kode:
            return self._search_rec(node.left, kode)
        return self._search_rec(node.right, kode)
 
    def update_stok(self, kode, delta):
        produk = self.search(kode)
        if produk:

