#examples.py - Contoh penggunaan advanced Indo Scraper

from indo_scraper import IndoScraper
from indo_scraper.utils import validate_indonesian_domain, format_scraped_data
import json
import time
import pandas as pd
from datetime import datetime

class AdvancedScraper:
    """Advanced wrapper untuk Indo Scraper dengan fitur tambahan"""
    
    def __init__(self):
        self.scraper = IndoScraper(delay=2.0, timeout=60)
        self.results = []
    
    def scrape_with_retry(self, url, max_retries=3):
        """Scraping dengan retry mechanism"""
        for attempt in range(max_retries):
            try:
                print(f"🔄 Attempt {attempt + 1}/{max_retries} for {url}")
                result = self.scraper.scrape(url)
                
                if result['status'] == 'success':
                    print(f"✅ Success on attempt {attempt + 1}")
                    return result
                else:
                    print(f"❌ Failed attempt {attempt + 1}: {result.get('error')}")
                    
            except Exception as e:
                print(f"💥 Exception on attempt {attempt + 1}: {str(e)}")
                
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2  # Exponential backoff
                print(f"⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
        
        return {"status": "failed", "error": "Max retries exceeded"}
    
    def scrape_school_directory(self):
        """Scraping direktori sekolah Indonesia"""
        print("🏫 SCRAPING DIREKTORI SEKOLAH INDONESIA")
        print("=" * 50)
        
        school_urls = [
            "https://www.smkn1jakarta.sch.id/",
            "https://www.smkn5bandung.sch.id/", 
            "https://www.sman1yogya.sch.id/",
            "https://www.smkn2surabaya.sch.id/",
            # Tambah URL sekolah lainnya
        ]
        
        school_data = []
        
        for i, url in enumerate(school_urls, 1):
            print(f"\n📚 Scraping sekolah {i}/{len(school_urls)}: {url}")
            
            result = self.scrape_with_retry(url)
            
            if result['status'] == 'success':
                school_info = {
                    'nama_sekolah': result['title'],
                    'website': url,
                    'deskripsi': result['description'],
                    'email': result['contact_info']['emails'],
                    'telepon': result['contact_info']['phones'],
                    'alamat': result['contact_info']['addresses'],
                    'jumlah_halaman': result['scraped_pages'],
                    'waktu_scraping': result['timestamp']
                }
                school_data.append(school_info)
                print(f"   ✅ {school_info['nama_sekolah']}")
                print(f"   📧 Email: {len(school_info['email'])}")
                print(f"   📞 Telepon: {len(school_info['telepon'])}")
            else:
                print(f"   ❌ Gagal scraping {url}")
        
        # Simpan ke JSON dan CSV
        with open('sekolah_indonesia.json', 'w', encoding='utf-8') as f:
            json.dump(school_data, f, ensure_ascii=False, indent=2)
        
        # Convert ke DataFrame untuk analisis
        if school_data:
            df = pd.DataFrame(school_data)
            df.to_csv('sekolah_indonesia.csv', index=False, encoding='utf-8')
            
            print(f"\n📊 RINGKASAN SCRAPING SEKOLAH:")
            print(f"   Total sekolah berhasil: {len(school_data)}")
            print(f"   Total email ditemukan: {sum(len(s['email']) for s in school_data)}")
            print(f"   Total telepon ditemukan: {sum(len(s['telepon']) for s in school_data)}")
            print(f"   📁 Data disimpan: sekolah_indonesia.json & sekolah_indonesia.csv")
        
        return school_data
    
    def scrape_government_portals(self):
        """Scraping portal pemerintah Indonesia"""
        print("\n🏛️ SCRAPING PORTAL PEMERINTAH")
        print("=" * 50)
        
        gov_urls = [
            "https://www.kemendikbud.go.id/",
            "https://www.kemkes.go.id/",
            "https://www.kemenag.go.id/",
            "https://www.kemenhub.go.id/",
            # Tambah URL pemerintah lainnya
        ]
        
        gov_data = []
        
        for url in gov_urls:
            print(f"\n🏛️ Scraping: {url}")
            
            result = self.scrape_with_retry(url, max_retries=2)
            
            if result['status'] == 'success':
                # Ekstrak informasi khusus pemerintah
                gov_info = {
                    'kementerian': result['title'],
                    'website': url,
                    'domain': result['domain'],
                    'deskripsi': result['description'],
                    'kontak': result['contact_info'],
                    'metadata': result['metadata'],
                    'total_links': len(result['links']),
                    'waktu_scraping': result['timestamp']
                }
                gov_data.append(gov_info)
                
                print(f"   ✅ {gov_info['kementerian']}")
                print(f"   🔗 Total link: {gov_info['total_links']}")
                
                # Analisis khusus untuk situs pemerintah
                content = result['content'].lower()
                keywords = ['pelayanan', 'informasi', 'berita', 'pengumuman', 'regulasi']
                keyword_count = {kw: content.count(kw) for kw in keywords}
                gov_info['keyword_analysis'] = keyword_count
                
                print(f"   📊 Keyword analysis: {keyword_count}")
            else:
                print(f"   ❌ Gagal scraping {url}")
        
        # Simpan hasil
        with open('pemerintah_indonesia.json', 'w', encoding='utf-8') as f:
            json.dump(gov_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 Data pemerintah disimpan: pemerintah_indonesia.json")
        return gov_data
    
    def scrape_news_analysis(self):
        """Scraping dan analisis situs berita Indonesia"""
        print("\n📰 SCRAPING & ANALISIS SITUS BERITA")
        print("=" * 50)
        
        news_urls = [
            "https://www.detik.com/",
            "https://www.kompas.com/",
            "https://www.liputan6.com/",
            "https://www.tempo.co/",
        ]
        
        news_data = []
        
        for url in news_urls:
            print(f"\n📰 Scraping berita: {url}")
            
            result = self.scraper.scrape(url, max_pages=2)
            
            if result['status'] == 'success':
                # Analisis khusus untuk situs berita
                content = result['content']
                
                # Hitung statistik konten
                word_count = len(content.split())
                char_count = len(content)
                
                # Cari kata kunci berita populer
                news_keywords = ['politik', 'ekonomi', 'olahraga', 'teknologi', 'kesehatan']
                keyword_freq = {}
                for keyword in news_keywords:
                    keyword_freq[keyword] = content.lower().count(keyword)
                
                news_info = {
                    'media': result['title'],
                    'website': url,
                    'word_count': word_count,
                    'char_count': char_count,
                    'link_count': len(result['links']),
                    'image_count': len(result['images']),
                    'keyword_frequency': keyword_freq,
                    'contact_info': result['contact_info'],
                    'scraped_at': result['timestamp']
                }
                
                news_data.append(news_info)
                
                print(f"   ✅ {news_info['media']}")
                print(f"   📝 Words: {word_count:,}")
                print(f"   🔗 Links: {news_info['link_count']}")
                print(f"   🖼️ Images: {news_info['image_count']}")
                print(f"   🔍 Top keyword: {max(keyword_freq, key=keyword_freq.get)}")
        
        # Simpan dan analisis
        with open('analisis_berita.json', 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        
        # Summary analysis
        if news_data:
            total_words = sum(n['word_count'] for n in news_data)
            total_links = sum(n['link_count'] for n in news_data)
            
            print(f"\n📊 RINGKASAN ANALISIS BERITA:")
            print(f"   Total media: {len(news_data)}")
            print(f"   Total kata: {total_words:,}")
            print(f"   Total link: {total_links:,}")
            print(f"   Rata-rata kata per media: {total_words//len(news_data):,}")
        
        return news_data
    
    def generate_report(self, data_list, report_type):
        """Generate laporan HTML dari hasil scraping"""
        print(f"\n📋 GENERATING {report_type.upper()} REPORT")
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Laporan {report_type.title()} - Indo Scraper</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
                .item {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
                .success {{ border-left: 5px solid #27ae60; }}
                .failed {{ border-left: 5px solid #e74c3c; }}
                .stats {{ background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 10px 0; }}
                .contact {{ background: #e8f4f8; padding: 10px; margin: 5px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🇮🇩 Laporan Scraping {report_type.title()}</h1>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Total item: {len(data_list)}</p>
            </div>
        """
        
        for i, item in enumerate(data_list, 1):
            html_content += f"""
            <div class="item success">
                <h3>{i}. {item.get('nama_sekolah', item.get('kementerian', item.get('media', 'Unknown')))}</h3>
                <p><strong>Website:</strong> <a href="{item.get('website', '#')}">{item.get('website', 'N/A')}</a></p>
                <p><strong>Deskripsi:</strong> {item.get('deskripsi', 'N/A')[:200]}...</p>
                
                <div class="contact">
                    <strong>Kontak:</strong><br>
                    📧 Email: {', '.join(item.get('email', item.get('kontak', {}).get('emails', [])))}<br>
                    📞 Telepon: {', '.join(item.get('telepon', item.get('kontak', {}).get('phones', [])))}<br>
                </div>
                
                <div class="stats">
                    <strong>Statistik:</strong><br>
                    🔗 Link: {item.get('total_links', item.get('link_count', 'N/A'))}<br>
                    📄 Halaman: {item.get('jumlah_halaman', 1)}<br>
                    ⏰ Scraping: {item.get('waktu_scraping', item.get('scraped_at', 'N/A'))}
                </div>
            </div>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        filename = f"laporan_{report_type}_{datetime.now().strftime('%Y%m%d')}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"   📄 Laporan HTML disimpan: {filename}")
        return filename

def main():
    """Jalankan semua contoh advanced"""
    print("🚀 INDO SCRAPER - ADVANCED EXAMPLES")
    print("=" * 60)
    
    advanced = AdvancedScraper()
    
    try:
        # 1. Scraping direktori sekolah
        school_data = advanced.scrape_school_directory()
        if school_data:
            advanced.generate_report(school_data, 'sekolah')
        
        # 2. Scraping portal pemerintah  
        gov_data = advanced.scrape_government_portals()
        if gov_data:
            advanced.generate_report(gov_data, 'pemerintah')
        
        # 3. Analisis situs berita
        news_data = advanced.scrape_news_analysis()
        if news_data:
            advanced.generate_report(news_data, 'berita')
        
        print("\n" + "=" * 60)
        print("✅ SEMUA ADVANCED EXAMPLES SELESAI!")
        print("📁 Check file JSON, CSV, dan HTML yang telah dibuat")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n⏹️ Program dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()