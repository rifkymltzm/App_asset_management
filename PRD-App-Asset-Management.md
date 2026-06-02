# Product Requirements Document (PRD): Manajemen Asset Investasi

## 1. Pendahuluan
**Nama Proyek:** Aplikasi Manajemen Asset Investasi
**Tujuan Proyek:** Membangun platform web yang memungkinkan pengguna untuk mencatat, mengelola, dan memantau portofolio investasi mereka di berbagai instrumen (seperti saham, reksadana, crypto, emas, dll) secara terpusat dengan harga yang selalu *up-to-date*.
**Filosofi Pengembangan:** Sistem dirancang sesederhana dan seefisien mungkin agar mudah dipahami, dikembangkan, dan dipelihara oleh *junior programmer* maupun dengan bantuan *AI (AI-assisted coding)*, namun tetap berpegang pada standar profesional (keamanan, performa, dan struktur kode yang bersih).

## 2. Technology Stack
*   **Backend & Framework Utama:** Django (Python)
*   **Frontend Interaktivitas:** Vanilla JavaScript
*   **Frontend Styling:** Tailwind CSS 
*   **Database:** PostgreSQL

## 3. Fitur Utama
Aplikasi ini memiliki beberapa fitur inti sebagai berikut:

### A. Autentikasi Pengguna (User Auth)
*   **Sign Up:** Pengguna dapat mendaftarkan akun baru.
*   **Login & Logout:** Akses masuk dan keluar sistem dengan aman menggunakan *session/token based authentication* standar Django.

### B. Manajemen Portofolio Asset
*   **Tambah Asset (Buy/Add):** Pengguna dapat memasukkan data instrumen investasi yang mereka miliki (misal: kode saham perusahaan, jumlah lot/unit, harga beli rata-rata).
*   **Integrasi Harga Real-time (API):** Sistem akan menarik harga pasar terbaru dari instrumen yang dimasukkan pengguna menggunakan layanan pihak ketiga (misal: Yahoo Finance API, Alpha Vantage, atau API keuangan publik lainnya).
*   **Pantau P&L (Profit & Loss):** Sistem secara otomatis menghitung dan menampilkan *Unrealized Profit/Loss* berdasarkan selisih antara harga beli rata-rata dengan harga pasar saat ini.

### C. Dashboard & Visualisasi Data
*   **Ringkasan Portofolio:** Menampilkan total nilai seluruh asset (Total Asset Value) pengguna dan ringkasan persentase keuntungan/kerugian secara keseluruhan.
*   **Grafik Harga (Chart):** Menyediakan grafik interaktif (menggunakan library JS ringan seperti Chart.js atau ApexCharts) untuk melihat pergerakan harga historis dari suatu instrumen investasi yang dipilih.

## 4. Desain Struktur Data (Model Django)
Untuk memudahkan pengembangan ke depannya, struktur *database* dibuat *normalized* namun tidak berlebihan (menghindari kompleksitas yang tidak perlu). Berikut rancangan Model Django yang disarankan:

### 4.1. `User` (Django Built-in Auth)
Menggunakan model `User` bawaan Django untuk menangani sistem login, password hashing, dan autentikasi dasar.

### 4.2. `InvestmentInstrument` (Master Data Instrumen)
Menyimpan daftar instrumen yang dikenali oleh sistem agar lebih rapi dan mengurangi *request* API yang sama secara berulang.
*   `ticker_symbol` (CharField, Unik) - Kode instrumen, contoh: "BBCA.JK", "BTC-USD".
*   `name` (CharField) - Nama panjang instrumen, contoh: "Bank Central Asia Tbk".
*   `instrument_type` (CharField) - Kategori, contoh: "Saham", "Crypto", "Reksadana".
*   `current_price` (DecimalField) - Harga pasar terakhir yang di-fetch dari API (berfungsi sebagai *cache* sementara).
*   `last_updated` (DateTimeField) - Waktu terakhir harga diperbarui dari API.

### 4.3. `UserAsset` (Portofolio Pengguna)
Menyimpan data spesifik mengenai investasi yang dimiliki oleh setiap *User*.
*   `user` (ForeignKey -> `User`) - Pemilik asset.
*   `instrument` (ForeignKey -> `InvestmentInstrument`) - Jenis instrumen yang dimiliki.
*   `quantity` (DecimalField) - Jumlah lembar saham/unit/koin.
*   `average_buy_price` (DecimalField) - Harga modal / harga beli rata-rata.
*   `created_at` (DateTimeField) - Waktu pencatatan.
*   `updated_at` (DateTimeField) - Waktu perubahan pencatatan terakhir.

> **Catatan Teknis Penting:** Perhitungan metrik seperti nilai *P&L* dan *Total Portofolio* sebaiknya tidak disimpan secara permanen di database, melainkan dihitung secara dinamis pada level `Model Property` atau diserahkan ke *Frontend/Views* setiap kali halaman dimuat, demi akurasi data.

## 5. Arsitektur & Pedoman Pengembangan Kode
*   **Pola Desain (MVT):** Menggunakan pendekatan MVT (Model-View-Template) standar dari Django untuk merender halaman HTML.
*   **Logika API Terpusat:** Integrasi dengan penyedia layanan harga (API eksternal) harus dipisahkan ke dalam modul atau *Service Class* tersendiri (misal: file `services.py` di dalam app), agar `views.py` tetap ringkas dan *clean*.
*   **Interaktivitas UI:** Penggunaan Vanilla JavaScript (Fetch API/AJAX) difokuskan pada bagian yang butuh pembaruan data tanpa *reload* seluruh halaman, seperti filter grafik interaktif atau memperbarui tabel harga.
*   **Tailwind CSS Integration:** Hindari *inline-styling* khusus. Manfaatkan sepenuhnya kelas utilitas Tailwind CSS untuk mencapai tampilan yang modern dan profesional. Strukturkan file template HTML (seperti `base.html`, `navbar.html`, `card.html`) dengan prinsip *DRY (Don't Repeat Yourself)* menggunakan mekanisme *include* pada Django template.

## 6. Rencana Fase Pengembangan (Milestones)
Untuk tim/developer (atau AI), pengerjaan aplikasi dapat dipecah secara sistematis:
1.  **Fase 1: Setup Lingkungan & Autentikasi Dasar.** Inisialisasi proyek Django, setup struktur PostgreSQL, konfigurasi *pipeline* Tailwind CSS, dan pembangunan sistem Sign-Up & Login yang aman.
2.  **Fase 2: Core Models & Manajemen CRUD.** Pembuatan struktur tabel (`InvestmentInstrument` & `UserAsset`). Pengembangan form/halaman agar *user* bisa menginput, mengedit, dan menghapus data pembelian instrumen.
3.  **Fase 3: Integrasi API Harga & Kalkulasi P&L.** Membuat layanan penarik harga (API *fetcher*) dan mengimplementasikan perhitungan profit/loss pada dashboard berdasarkan data langsung.
4.  **Fase 4: Visualisasi Grafik & Finalisasi UI.** Penambahan library grafik historis untuk tiap instrumen, perapian UI/UX dengan standar Tailwind agar estetis (*professional look*), dan pengujian menyeluruh terhadap fitur yang sudah dibangun.
