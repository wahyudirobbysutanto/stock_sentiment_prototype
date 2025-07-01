from scraper import scrape_google_news
from sentiment import analyze_sentiment, generate_summary
from db import insert_batch
from utils import save_to_json
from collections import Counter

def main(stock):
    news_list = scrape_google_news(stock, max_articles=3)

    if not news_list:
        print("Tidak ada berita ditemukan.")
        return

    for item in news_list:
        item['Sentiment'] = analyze_sentiment(item['Content'])

    sentiments = [item['Sentiment'] for item in news_list if item['Sentiment']]
    
    if not sentiments:
        print("Tidak ada sentimen yang bisa dianalisis.")
        return

    # Hitung sentimen dominan
    summary_sentiment = Counter(sentiments).most_common(1)[0][0]

    # Buat ringkasan seluruh konten
    contents = [item['Content'] for item in news_list]
    summary_result = generate_summary(contents)

    # Ambil bagian ringkasan dan sentimen dari hasil Gemini
    summary_lines = summary_result.splitlines()
    summary_text = next((line.replace("Ringkasan:", "").strip() for line in summary_lines if "Ringkasan:" in line), "")
    summary_sentiment_ai = next((line.replace("Sentimen:", "").strip().capitalize() for line in summary_lines if "Sentimen:" in line), summary_sentiment)
    
    caller_id = insert_batch(news_list, summary_sentiment_ai, summary_text, stock)
    save_to_json(news_list, caller_id, stock)
    print(f"Berhasil disimpan dengan CallerID #{caller_id}. Summary sentiment: {summary_sentiment_ai}")


if __name__ == "__main__":
    stock = input("Masukkan kode saham (contoh: BBRI): ")
    main(stock)
