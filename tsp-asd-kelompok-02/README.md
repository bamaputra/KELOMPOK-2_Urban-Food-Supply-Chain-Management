# KELOMPOK-2_Urban-Food-Supply-Chain-Management
topik 10 Urban Food Supply Chain Management

## Team
1. MUHAMMAD SURYA ALDO 25051030046 
2. FARHAN FAJARI FADHULURRAHMAN 25051030043
3. AHMAD NIRO YOGARA 25051030051
4. DECO ARDIANDRA 25051030069
   
---

## Mata Kuliah
Algoritma dan Struktur Data  
S1 Teknik Elektro  
Universitas Negeri Yogyakarta

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
