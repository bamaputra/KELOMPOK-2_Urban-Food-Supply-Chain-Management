class BSTNodeProd:
    def __init__(self, produk):
        self.produk = produk
        self.left = None
        self.right = None
 
 
class BSTKatalog:
    def __init__(self):
        self.root = None
 
    def insert(self, produk):
        self.root = self._insert_rec(self.root, produk)
 
    def _insert_rec(self, node, produk):
        if node is None:
            return BSTNodeProd(produk)
        if produk.kode < node.produk.kode:
            node.left = self._insert_rec(node.left, produk)
        elif produk.kode > node.produk.kode:
            node.right = self._insert_rec(node.right, produk)
        return node
 
    def search(self, kode):
        return self._search_rec(self.root, kode)
 
    def _search_rec(self, node, kode):
        if node is None or node.produk.kode == kode:
            return node.produk if node else None
        if kode < node.produk.kode:
            return self._search_rec(node.left, kode)
        return self._search_rec(node.right, kode)
 
    def update_stok(self, kode, delta):
        produk = self.search(kode)
        if produk:
            produk.stok += delta
            if produk.stok < 0:
                produk.stok = 0
            return True
        return False
 
    def filter_kadaluarsa(self, maks_hari):
        result = []
        self._filter_rec(self.root, maks_hari, result)
        return result
 
    def _filter_rec(self, node, maks_hari, result):
        if node is None:
            return
        self._filter_rec(node.left, maks_hari, result)
        if node.produk.masa_kadaluarsa_hari <= maks_hari:
            result.append(node.produk)
        self._filter_rec(node.right, maks_hari, result)
 
    def inorder(self):
        result = []
        self._inorder_rec(self.root, result)
        return result
 
    def _inorder_rec(self, node, result):
        if node is None:
            return
        self._inorder_rec(node.left, result)
        result.append(node.produk)
        self._inorder_rec(node.right, result)
