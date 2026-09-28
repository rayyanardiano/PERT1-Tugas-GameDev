# Simulasi Enemy AI - Dungeon 2D Sederhana

Proyek ini adalah simulasi kecerdasan buatan (AI) musuh dalam game dungeon menggunakan Python. Musuh dirancang untuk bisa mendeteksi pemain, mengejar, mencari jalur untuk menghindari rintangan (tembok), dan menyerang jika sudah dekat.

## Algoritma yang Digunakan

1. **Finite State Machine (FSM)**
   FSM digunakan untuk mengatur perilaku dasar musuh melalui *state* atau fase. Terdapat tiga state utama:
   - **PATROL**: Musuh diam di tempat sambil terus memindai sekeliling.
   - **CHASE**: Musuh mendeteksi player dan akan mulai mencari jalan mendekati posisi player menggunakan algoritma pathfinding.
   - **REACHED**: Musuh telah mencapai posisi player dan game berakhir (Game Over).

2. **A* Pathfinding (A-Star)**
   Algoritma pencarian rute yang sangat optimal untuk mencari jalur terpendek dari posisi musuh menuju posisi player dengan menghindari tembok. 
   **Alasan Memilih A*:**
   A* menggabungkan keunggulan algoritma Dijkstra (menjamin rute terpendek) dan Greedy Best-First-Search (cepat karena dipandu oleh heuristik). Ini membuatnya sangat efisien, cepat, dan pintar dalam memandu musuh menyusuri labirin tanpa perlu mengecek semua jalur yang tak perlu.

3. **Pengecekan Jarak (Distance Checks)**
   Proyek ini menggunakan dua rumus pencarian jarak untuk keperluan berbeda:
   - **Jarak Euclidean**: Digunakan sebagai sensor radius berbentuk lingkaran (`detection_range`). Sesuai untuk mensimulasikan batas penglihatan sesungguhnya di dunia nyata.
   - **Jarak Manhattan**: Digunakan sebagai heuristik pada A* dan jarak serangan. Karena gerakan hanya terbatas pada 4 arah (atas, bawah, kiri, kanan), jarak langkah grid dihitung dengan Manhattan (tanpa diagonal).

---

## Flowchart Game Loop FSM

Berikut adalah cara kerja alur sistem dan state musuh (FSM) dalam setiap giliran / *tick*:

```mermaid
graph TD
    Start([GAME START]) --> Init[Inisialisasi Map, Player, Enemy]
    Init --> Loop{Game Loop<br/>Setiap Tick}
    
    Loop --> Calc["Hitung Euclidean<br/>Distance<br/>d = √(dx² + dy²)"]
    Calc --> CheckDist{d ≤ Detection Radius R?}
    
    CheckDist -->|Tidak| Patrol["State: PATROL<br/>Enemy diam / berpatroli"]
    Patrol --> Render[Tampilkan peta dungeon]
    
    CheckDist -->|Ya| Chase["State: CHASE<br/>Player Terdeteksi!"]
    Chase --> RunAStar["Jalankan A*<br/>Pathfinding<br/>Dari posisi Enemy ke posisi Player"]
    RunAStar --> CheckPath{"Jalur<br/>ditemukan?"}
    
    CheckPath -->|Tidak| NoPath["❌ Tidak ada jalur<br/>Enemy tidak bisa bergerak"]
    NoPath --> Render
    
    CheckPath -->|Ya| GetWaypoint["Ambil waypoint<br/>berikutnya dari jalur A*"]
    GetWaypoint --> Move["Geser posisi Enemy<br/>1 langkah ke waypoint"]
    Move --> CheckPos{"pos Enemy ==<br/>pos Player?"}
    
    CheckPos -->|Tidak| Render
    CheckPos -->|Ya| Reached["State: REACHED<br/>⚔️ Enemy mencapai Player!"]
    Reached --> GameOver([GAME OVER])
    
    Render --> Loop
```

---

## Flowchart Pathfinding A*

Berikut adalah logika algoritma A* saat mencari jalan dari musuh menuju titik target:

```mermaid
graph TD
    A[Mulai Pathfinding] --> B[Masukkan Node Start ke Open List]
    B --> C{Open List Kosong?}
    C -->|Ya| D[Jalur Tidak Ditemukan]
    C -->|Tidak| E[Ambil Node dengan nilai f-cost Terendah]
    E --> F{Node = Posisi Player?}
    F -->|Ya| G[Kembalikan List Jalur dari Target ke Awal]
    F -->|Tidak| H[Pindahkan Node ke Closed List]
    H --> I[Cek 4 Node Tetangga]
    I --> J{Evaluasi Setiap Tetangga}
    J --> K{Tetangga adalah Tembok / ada di Closed List?}
    K -->|Ya| L[Abaikan]
    K -->|Tidak| M[Hitung g-cost & h-cost]
    M --> N{Jalur Lebih Baik / Tetangga Baru?}
    N -->|Ya| O[Perbarui Cost & Masukkan ke Open List]
    N -->|Tidak| L
    O --> C
    L --> C
```

---

## Cara Menjalankan Program

Program ini ditulis dengan standar library bawaan Python tanpa dependensi pihak ketiga, sehingga mudah langsung dijalankan di PC / Laptop.

1. Buka Terminal (Command Prompt / PowerShell / Bash).
2. Arahkan *directory* ke folder tempat Anda mengekstrak proyek ini.
3. Jalankan perintah berikut:

```bash
python enemy_ai.py
```
*(Catatan: pastikan Anda sudah menginstal Python)*
