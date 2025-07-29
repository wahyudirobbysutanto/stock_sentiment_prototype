from core.scraper import get_cached_or_fresh_news  
from core.sentiment import analyze_sentiment, generate_summary, analyze_sentiment_final, analyze_sentiment_text
from services.db import insert_batch
from core.utils import save_to_json, clean_gemini_formatting, clean_gemini_fundamental_formatting
from services.finance import get_fundamentals
from collections import Counter


def main(stock, return_result=False):
    news_list = get_cached_or_fresh_news(stock, max_articles=5)

    if not news_list:
        print("Tidak ada berita ditemukan.")
        return

    for item in news_list:
        item['Sentiment'] = analyze_sentiment(item['Content'])

    sentiments = [item['Sentiment'] for item in news_list if item['Sentiment']]
    if not sentiments:
        print("Tidak ada sentimen yang bisa dianalisis.")
        return

    summary_sentiment = Counter(sentiments).most_common(1)[0][0]

    contents = [item['Content'] for item in news_list]
    summary_result = generate_summary(contents)

    summary_lines = summary_result.splitlines()
    summary_lines = [clean_gemini_formatting(line) for line in summary_lines]

    summary_text = next((line.replace("Ringkasan:", "").strip() for line in summary_lines if "Ringkasan:" in line), "")
    summary_sentiment_ai = next((line.replace("Sentimen:", "").strip().capitalize() for line in summary_lines if "Sentimen:" in line), summary_sentiment)

    summary_text = clean_gemini_formatting(summary_text)
    summary_sentiment_ai = clean_gemini_formatting(summary_sentiment_ai)
    
    # Ambil data fundamental
    financial_data = get_fundamentals(stock)
    if financial_data:
        financial_text = f"Stock: {stock}. PE Ratio: {financial_data.get('PE_Ratio')}, PB Ratio: {financial_data.get('PB_Ratio')}, ROE: {financial_data.get('ROE')}, EPS: {financial_data.get('EPS')}, Book Value: {financial_data.get('BookValue')}, Debt/Equity: {financial_data.get('DebtEquity')}"
        fundamental_sentiment_result = analyze_sentiment_text(financial_data)
        fundamental_sentiment, fundamental_sentiment_summary = clean_gemini_fundamental_formatting(fundamental_sentiment_result)
    else:
        fundamental_sentiment = ''
        fundamental_sentiment_summary = ''


    # print(fundamental_sentiment)
    # print(fundamental_sentiment_summary)
    # final_summary = f"{summary_text}\n\nData Keuangan: {financial_text}"
    # final_summary = f"asdqwe\n\nData Keuangan: {financial_text}"
    final_sentiment_result = analyze_sentiment_final(contents, financial_data)
    final_sentiment, final_sentiment_summary = clean_gemini_fundamental_formatting(fundamental_sentiment_result)
    # print(final_sentiment)

    # exit()

    # print("summary_sentiment_ai:", summary_sentiment_ai)
    # print("summary_text:", summary_text)
    # print("final_summary:", final_summary)
    # print("fundamental_sentiment:", fundamental_sentiment)


    caller_id = insert_batch(
        news_list, stock,
        summary_sentiment_ai, summary_text,
        fundamental_sentiment, fundamental_sentiment_summary,
        final_sentiment, final_sentiment_summary
    )

    save_to_json(news_list, caller_id, stock)

    if return_result:
        return {
            "caller_id": caller_id,
            "stock": stock,
            "summary": summary_text,
            "sentiment": summary_sentiment_ai,
            "articles": news_list
        }


if __name__ == "__main__":
    stock = input("Masukkan kode saham (contoh: BBRI): ")
    main(stock.upper())
