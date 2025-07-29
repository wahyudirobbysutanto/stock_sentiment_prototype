
# 📰 Stock News Sentiment Analyzer

Web-based tool untuk menganalisis sentimen berita saham dari berbagai sumber secara otomatis, dibantu AI Gemini. Proyek ini cocok untuk keperluan riset, edukasi, atau monitoring saham berbasis berita.

## 🔧 Fitur Utama

- Input kode saham (misalnya: `BBRI`, `TLKM`, `BMRI`)
- Scraping berita dari hasil pencarian Google (Google News & situs berita populer)
- Ekstraksi judul, tautan, dan isi artikel dengan `newspaper3k`
- Analisis sentimen tiap artikel dengan Google Gemini 2.0 Flash
- Ringkasan otomatis batch berita dengan AI
- Penyimpanan hasil ke:
  - **SQL Server** (tabel: `WebsiteData` dan `HistorySummary`)
  - **File JSON** (backup setiap batch)
- Antarmuka **Flask Web**:
  - Form input saham
  - Riwayat analisis dengan filter tanggal & pagination
  - Halaman detail untuk melihat isi setiap batch

## 📦 Struktur Folder

```
project/
│
├── core/
│   ├── scraper.py          # Scraper berita dan konten
│   ├── sentiment.py        # Integrasi Gemini
│   └── utils.py            # Simpan JSON, helper, pembersih teks
│
├── output/                 # Folder JSON hasil scraping
│
├── data/                   # Folder JSON hasil scraping
│   └── database.sql         # SQL script for database
│
├── services/
│   ├── db.py               # Insert dan query data dari SQL Server
│   └── finance.py          # Get fundamental and insert to database for the fundamental
│
├── templates/
│   ├── index.html          # Halaman utama (form + history)
│   └── detail.html         # Halaman detail CallerID
│
├── app.py                  # Entry point Flask
├── main.py                 # Proses scraping + analisis
├── config.py               # Koneksi SQL Server (pakai .env)
│
├── .env                    # Konfigurasi rahasia (.gitignore!)
└── requirements.txt
```

## 🗃️ Struktur Database (SQL Server)

**Tabel: `WebsiteData`**

| Kolom     | Tipe         | Keterangan                     |
|-----------|--------------|--------------------------------|
| Stock     | VARCHAR      | Kode saham (ex: BBRI)          |
| Title     | VARCHAR      | Judul berita                   |
| Link      | VARCHAR      | URL asli                       |
| Content   | TEXT         | Isi artikel                    |
| Sentiment | VARCHAR      | Hasil analisis per artikel     |
| Date      | DATETIME     | Tanggal publikasi/scrape       |
| CallerID  | INT          | ID batch scraping              |

**Tabel: `HistorySummary`**

| Kolom     | Tipe         | Keterangan                     |
|-----------|--------------|--------------------------------|
| CallerID  | INT          | ID unik tiap batch             |
| Stock     | VARCHAR      | Saham                          |
| Sentiment | VARCHAR      | Ringkasan sentimen batch       |
| Summary   | TEXT         | Ringkasan isi batch (dari AI)  |
| Date      | DATETIME     | Tanggal scraping dilakukan     |

## ⚙️ .env (Contoh)

```env
SQL_SERVER=LAPTOP-XXXX
SQL_DATABASE=StockSentiment
USE_WINDOWS_AUTH=true
GEMINI_API_KEY=your_api_key_here
```

## ▶️ Cara Menjalankan

1. Clone repo ini:
   ```
   git clone https://github.com/wahyudirobbysutanto/stock_sentiment_prototype.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Jalankan Flask:
   ```
   python app.py
   ```

4. Buka browser di `http://localhost:5000`

## 💡 Teknologi yang Digunakan

- Python (Flask, requests, BeautifulSoup, newspaper3k, pyodbc)
- SQL Server
- Google Gemini
- Bootstrap 5

## 🧪 Status

✅ Fitur scraping dan analisis AI berjalan  
✅ UI dasar sudah siap (input + history + detail)  
🛠️ Masih bisa dikembangkan:
- Auto-scheduler untuk scraping harian
- Dukungan multi-saham sekaligus
- Grafik tren sentimen

## 📜 Lisensi

MIT License — silakan digunakan dan dikembangkan sesuai kebutuhan.
