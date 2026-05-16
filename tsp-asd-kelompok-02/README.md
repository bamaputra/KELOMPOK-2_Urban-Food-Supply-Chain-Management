# KELOMPOK-2_Urban-Food-Supply-Chain-Management
topik 10 Urban Food Supply Chain Management

## Deskripsi Project
Project ini merupakan implementasi sistem manajemen rantai pasok pangan perkotaan menggunakan bahasa Python dan konsep Algoritma Struktur Data.

Sistem dirancang untuk membantu pengelolaan distribusi produk pangan mulai dari petani, distributor, gudang, hingga pasar dengan mempertimbangkan:
- stok produk
- prioritas pengiriman
- masa kadaluarsa
- jalur distribusi termurah

---

## Struktur Data yang Digunakan
Project ini menggunakan beberapa struktur data utama, yaitu:

- Binary Search Tree (BST)
  - Mengelola katalog produk dan pencarian stok.
- Priority Queue
  - Mengatur prioritas pengiriman berdasarkan masa kadaluarsa.
- Stack
  - Menyimpan log transaksi distribusi.
- Circular Queue
  - Buffer penyimpanan produk pada gudang.
- Graph
  - Merepresentasikan jaringan rantai pasok.
- Algoritma Dijkstra
  - Menentukan jalur distribusi dengan biaya termurah.
    
---

## Fitur Program
- Pengiriman produk antar node
- Pencarian jalur termurah
- Pemeriksaan stok produk
- Filter produk mendekati kadaluarsa
- Buffer gudang
- Laporan distribusi

---

## Struktur Folder
```bash
docs/          -> laporan dan slide presentasi
src/           -> source code utama
tests/         -> pengujian program
experiments/   -> eksperimen dan analisis
