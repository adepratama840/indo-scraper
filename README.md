<<<<<<< HEAD
# Indo Scraper 🇮🇩

Library Python untuk scraping website Indonesia dengan mudah dan aman. Dirancang khusus untuk domain Indonesia seperti `.id`, `.co.id`, `.go.id`, `.sch.id`, dan domain Indonesia lainnya.

## 🚀 Fitur Utama

- ✅ **Mudah digunakan** - Cukup satu baris kode untuk scraping
- ✅ **Domain Indonesia** - Dioptimalkan untuk website Indonesia
- ✅ **Ekstraksi otomatis** - Email, telepon, alamat, dan kontak lainnya
- ✅ **Multiple pages** - Scraping beberapa halaman sekaligus
- ✅ **Export JSON** - Simpan hasil ke file JSON
- ✅ **Command Line** - Bisa digunakan dari terminal
- ✅ **Rate limiting** - Menghormati server dengan delay otomatis

## 📦 Instalasi

```bash
pip install indo-scraper
```

## 🔧 Cara Penggunaan

### 1. Penggunaan Dasar

```python
from indo_scraper import IndoScraper

# Buat instance scraper
scraper = IndoScraper()

# Scraping website
hasil = scraper.scrape("https://www.smkn5bandung.sch.id/")

# Lihat hasil
print(f"Judul: {hasil['title']}")
print(f"Email ditemukan: {hasil['contact_info']['emails']}")
print(f"Telepon: {hasil['contact_info']['phones']}")
```

### 2. Scraping dengan Opsi Lengkap

```python
from indo_scraper import IndoScraper

scraper = IndoScraper(delay=2.0, timeout=60)

hasil = scraper.scrape(
    url="https://www.kemendikbud.go.id/",
    extract_links=True,      # Ekstrak semua link
    extract_images=True,     # Ekstrak semua gambar
    extract_contact=True,    # Ekstrak informasi kontak
    max_pages=3             # Scraping maksimal 3 halaman
)

# Simpan hasil ke JSON
scraper.save_to_json(hasil, "hasil_scraping.json")
```

### 3. Scraping Multiple Websites

```python
from indo_scraper import IndoScraper

scraper = IndoScraper()

urls = [
    "https://www.smkn5bandung.sch.id/",
    "https://www.ui.ac.id/",
    "https://www.detik.com/"
]

semua_hasil = scraper.scrape_multiple(urls, max_pages=2)

for hasil in semua_hasil:
    print(f"Website: {hasil['domain']}")
    print(f"Status: {hasil['status']}")
    print("-" * 40)
```

### 4. Menggunakan dari Command Line

```bash
# Scraping basic
indo-scraper https://www.smkn5bandung.sch.id/

# Scraping dengan opsi
indo-scraper https://www.kemendikbud.go.id/ --max-pages 3 --output hasil.json --delay 2

# Lihat bantuan
indo-scraper --help
```

## 📋 Format Hasil Scraping

```python
{
    "url": "https://www.smkn5bandung.sch.id/",
    "domain": "www.smkn5bandung.sch.id",
    "title": "SMK Negeri 5 Bandung",
    "description": "Website resmi SMK Negeri 5 Bandung",
    "content": "Konten lengkap website...",
    "links": ["https://...", "https://..."],
    "images": ["https://img1.jpg", "https://img2.png"],
    "contact_info": {
        "emails": ["info@smkn5bandung.sch.id"],
        "phones": ["(022) 1234567", "0812-3456-7890"],
        "addresses": ["Jl. Veteran No. 1, Bandung"]
    },
    "metadata": {
        "author": "...",
        "keywords": "...",
        "og:title": "..."
    },
    "status": "success",
    "scraped_pages": 1,
    "timestamp": "2024-12-07 10:30:00"
}
```

## 🛠️ Opsi Konfigurasi

### Inisialisasi Scraper

```python
scraper = IndoScraper(
    delay=1.0,      # Jeda antar request (detik)
    timeout=30      # Timeout request (detik)
)
```

### Parameter Scraping

```python
scraper.scrape(
    url="https://website.co.id/",
    extract_links=True,     # Ekstrak link (default: True)
    extract_images=True,    # Ekstrak gambar (default: True)
    extract_contact=True,   # Ekstrak kontak (default: True)
    max_pages=1            # Maks halaman (default: 1)
)
```

## 🎯 Domain yang Didukung

Library ini dioptimalkan untuk domain Indonesia:

- `.id` - Domain Indonesia
- `.co.id` - Komersial Indonesia
- `.or.id` - Organisasi Indonesia
- `.ac.id` - Akademik Indonesia
- `.sch.id` - Sekolah Indonesia
- `.net.id` - Network Indonesia
- `.web.id` - Web Indonesia
- `.my.id` - Personal Indonesia
- `.go.id` - Pemerintah Indonesia
- `.mil.id` - Militer Indonesia
- `.desa.id` - Desa Indonesia
- `.ponpes.id` - Pondok Pesantren

## 🔍 Contoh Penggunaan Lengkap

### Scraping Website Sekolah

```python
from indo_scraper import IndoScraper
from indo_scraper.utils import format_scraped_data

# Buat scraper dengan delay 2 detik
scraper = IndoScraper(delay=2.0)

# Scraping website sekolah
print("🔄 Memulai scraping...")
hasil = scraper.scrape(
    url="https://www.smkn5bandung.sch.id/",
    max_pages=2
)

# Format dan tampilkan hasil
print(format_scraped_data(hasil))

# Simpan ke file
scraper.save_to_json(hasil, "data_sekolah.json")
print("✅ Data berhasil disimpan!")
```

### Scraping Website Pemerintah

```python
from indo_scraper import IndoScraper

scraper = IndoScraper()

# Scraping website kemendikbud
hasil = scraper.scrape("https://www.kemendikbud.go.id/")

if hasil['status'] == 'success':
    print(f"📊 Berhasil scraping {hasil['domain']}")
    print(f"📧 Email ditemukan: {len(hasil['contact_info']['emails'])}")
    print(f"📞 Telepon ditemukan: {len(hasil['contact_info']['phones'])}")
    print(f"🔗 Link ditemukan: {len(hasil['links'])}")
else:
    print(f"❌ Gagal scraping: {hasil.get('error', 'Unknown error')}")
```

### Batch Scraping Multiple Websites

```python
from indo_scraper import IndoScraper
import time

scraper = IndoScraper(delay=3.0)  # Delay 3 detik untuk menghormati server

# Daftar website Indonesia
websites = [
    "https://www.ui.ac.id/",
    "https://www.itb.ac.id/",
    "https://www.ugm.ac.id/",
    "https://www.unpad.ac.id/"
]

print("🚀 Memulai batch scraping...")
start_time = time.time()

all_results = []
for i, url in enumerate(websites, 1):
    print(f"📥 Scraping {i}/{len(websites)}: {url}")
    
    hasil = scraper.scrape(url, max_pages=1)
    all_results.append(hasil)
    
    # Progress info
    if hasil['status'] == 'success':
        print(f"  ✅ Berhasil - {hasil['title'][:50]}...")
    else:
        print(f"  ❌ Gagal - {hasil.get('error', 'Unknown')}")

# Summary
elapsed = time.time() - start_time
success_count = sum(1 for r in all_results if r['status'] == 'success')

print(f"\n📊 RINGKASAN BATCH SCRAPING")
print(f"Total website: {len(websites)}")
print(f"Berhasil: {success_count}")
print(f"Gagal: {len(websites) - success_count}")
print(f"Waktu total: {elapsed:.2f} detik")

# Simpan semua hasil
scraper.save_to_json(all_results, "batch_scraping_results.json")
```

## 🚨 Tips Penggunaan yang Baik

### 1. Menghormati Server

```python
# Gunakan delay yang wajar (minimal 1 detik)
scraper = IndoScraper(delay=2.0)

# Jangan scraping terlalu banyak halaman sekaligus
hasil = scraper.scrape(url, max_pages=5)  # Maksimal 5 halaman
```

### 2. Error Handling

```python
from indo_scraper import IndoScraper

scraper = IndoScraper()

try:
    hasil = scraper.scrape("https://website.co.id/")
    
    if hasil['status'] == 'success':
        print("✅ Scraping berhasil!")
        # Proses data...
    else:
        print(f"❌ Scraping gagal: {hasil.get('error')}")
        
except Exception as e:
    print(f"💥 Error tak terduga: {str(e)}")
```

### 3. Validasi Domain

```python
from indo_scraper.utils import validate_indonesian_domain

url = "https://www.example.com/"

if validate_indonesian_domain(url):
    print("✅ Domain Indonesia terdeteksi")
    hasil = scraper.scrape(url)
else:
    print("⚠️ Bukan domain Indonesia")
    # Tetap bisa scraping, tapi tidak dioptimalkan untuk Indonesia
    hasil = scraper.scrape(url)
```

## 📝 Command Line Interface

### Perintah Dasar

```bash
# Scraping sederhana
indo-scraper https://www.smkn5bandung.sch.id/

# Dengan output file
indo-scraper https://www.ui.ac.id/ --output universitas.json

# Multiple pages dengan delay
indo-scraper https://www.detik.com/ --max-pages 3 --delay 2.5

# Tanpa ekstrak gambar dan link
indo-scraper https://www.kemendikbud.go.id/ --no-images --no-links
```

### Opsi Command Line Lengkap

```bash
indo-scraper [URL] [OPTIONS]

Opsi:
  --max-pages N     Maksimal halaman yang di-scrape (default: 1)
  --delay N         Jeda antar request dalam detik (default: 1.0)
  --timeout N       Timeout request dalam detik (default: 30)
  --output FILE     File output JSON (opsional)
  --no-links        Jangan ekstrak link
  --no-images       Jangan ekstrak gambar
  --no-contact      Jangan ekstrak informasi kontak
  --version         Tampilkan versi
  --help           Tampilkan bantuan
```

## 🛡️ Keamanan dan Etika

### Pedoman Penggunaan

1. **Hormati robots.txt** - Selalu cek file robots.txt website
2. **Gunakan delay yang wajar** - Minimal 1-2 detik antar request
3. **Jangan overload server** - Batasi jumlah halaman yang di-scrape
4. **Patuhi Terms of Service** - Baca dan patuhi TOS website
5. **Data pribadi** - Hati-hati dengan data pribadi yang di-scrape

### Contoh Penggunaan yang Bertanggung Jawab

```python
from indo_scraper import IndoScraper

# Konfigurasi yang menghormati server
scraper = IndoScraper(
    delay=2.0,      # Delay 2 detik
    timeout=30      # Timeout wajar
)

# Scraping dengan batasan
hasil = scraper.scrape(
    url="https://website.co.id/",
    max_pages=3     # Maksimal 3 halaman saja
)

# Cek apakah ada informasi sensitif
if hasil['contact_info']['emails']:
    print("⚠️ Ditemukan email - gunakan dengan bijak")
```

## 🐛 Troubleshooting

### Masalah Umum

**1. Error "Connection timeout"**
```python
# Tingkatkan timeout
scraper = IndoScraper(timeout=60)
```

**2. Error "Too many requests"**
```python
# Tingkatkan delay
scraper = IndoScraper(delay=5.0)
```

**3. Website tidak bisa diakses**
```python
# Cek status error
hasil = scraper.scrape(url)
if hasil['status'] == 'error':
    print(f"Error: {hasil['error']}")
```

**4. Data tidak lengkap**
```python
# Scraping dengan opsi lengkap
hasil = scraper.scrape(
    url=url,
    extract_links=True,
    extract_images=True,
    extract_contact=True,
    max_pages=2
)
```

## 📄 Lisensi

MIT License - Bebas untuk digunakan dan dimodifikasi.

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository ini
2. Buat branch untuk fitur baru
3. Commit perubahan Anda
4. Push ke branch
5. Buat Pull Request

## 📞 Dukungan

- 🐛 **Bug reports**: [GitHub Issues](https://github.com/adepratama840/indo-scraper/issues)
- 💡 **Feature requests**: [GitHub Issues](https://github.com/adepratama840/indo-scraper/issues)
- 📚 **Dokumentasi**: [GitHub Wiki](https://github.com/adepratama840/indo-scraper/wiki)
- 📧 **Email**: adepratama20071907@gmail.com

## 🔄 Changelog

### v1.0.0
- ✨ Rilis pertama
- 🚀 Scraping dasar untuk website Indonesia
- 📧 Ekstraksi otomatis email, telepon, alamat
- 💾 Export ke JSON
- 🖥️ Command line interface
- 📱 Support untuk semua domain Indonesia

---

**Dibuat dengan ❤️ untuk komunitas developer Indonesia**
=======
# indo-scraper
>>>>>>> 0cbe3a032a07d478c1b1a462705172de0d426e4e
