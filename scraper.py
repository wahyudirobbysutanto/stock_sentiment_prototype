import requests
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime
from readability import Document

# Ambil isi artikel dari URL menggunakan readability
def extract_article_content(url, headers=None):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        doc = Document(response.text)
        content_html = doc.summary()
        soup = BeautifulSoup(content_html, 'html.parser')
        return soup.get_text(separator='\n').strip()
    except Exception as e:
        print(f"[WARN] Gagal ambil isi dari {url}: {e}")
        return None

# Fungsi scraping utama
def scrape_google_news(stock_name, max_articles=3):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }

    query = f"{stock_name} berita"
    url = f"https://www.google.com/search?q={query}&hl=id&gl=id&tbm=nws"

    print(f"[INFO] Mencari berita untuk: {stock_name}")
    response = requests.get(url, headers=headers)
    time.sleep(random.uniform(2, 4))

    if response.status_code != 200:
        print("[ERROR] Gagal mengambil hasil dari Google. Status code:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Ambil semua <a> dan filter yang berasal dari media berita populer
    all_links = soup.select('a')
    berita_links = [
        a for a in all_links
        if a.get('href') and any(domain in a['href'] for domain in [
            'detik.com', 'cnbcindonesia.com', 'kontan.co.id',
            'kompas.com', 'bisnis.com', 'republika.co.id', 'cnnindonesia.com'
        ])
    ]

    print(f"[INFO] Ditemukan {len(berita_links)} link berita")

    results = []
    seen_links = set()

    for a in berita_links:
        if len(results) >= max_articles:
            break

        # href = a.get('href')
        href_raw = a.get('href')
        href = None
        if href_raw.startswith("/url?q="):
            href = href_raw.split("/url?q=")[-1].split("&")[0]
        elif href_raw.startswith("http"):
            href = href_raw
        else:
            href = None

        if not href or href in seen_links:
            continue

        title = a.get_text(strip=True)

        if not href or not title or href in seen_links:
            continue

        seen_links.add(href)
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Ambil isi artikel
        content = extract_article_content(href, headers)
        if not content:
            print(f"[WARN] Gagal ambil isi artikel dari {href}")
            content = title  # fallback

        results.append({
            "Stock": stock_name,
            "Title": title,
            "Link": href,
            "Content": content,
            "Date": date_now
        })

        time.sleep(random.uniform(1, 2))  # jeda agar tidak dianggap bot

    return results
