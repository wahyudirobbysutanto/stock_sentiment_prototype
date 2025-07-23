import google.generativeai as genai

import os

from dotenv import load_dotenv
    
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(os.getenv("GEMINI_MODEL"))


def analyze_sentiment(text: str) -> str:
    prompt = f"""
    Tugas kamu adalah melakukan analisis sentimen terhadap artikel berita saham berikut ini.
    
    Artikel:
    \"\"\"
    {text}
    \"\"\"

    Jawab hanya dengan salah satu dari tiga label ini (tanpa penjelasan): 
    Positive, Negative, atau Neutral.
    """
    try:
        response = model.generate_content(prompt)
        sentiment = response.text.strip().capitalize()

        if sentiment not in ["Positive", "Negative", "Neutral"]:
            return "Neutral"  # fallback aman
        return sentiment
    except Exception as e:
        print(f"[WARN] Gagal analisis sentimen: {e}")
        return "Neutral"


def generate_summary(articles: list[str]) -> str:
    text = "\n\n".join(articles[:3])  # batasi agar tidak terlalu panjang
    prompt = f"""
Berikut adalah beberapa artikel berita tentang saham:

\"\"\"
{text}
\"\"\"

Tolong:
1. Buat ringkasan isi secara singkat dalam 2-3 kalimat
2. Nilai sentimen keseluruhan (Positive, Neutral, atau Negative)

Format jawaban:
Ringkasan: ...
Sentimen: ...
"""

    try:
        response = model.generate_content(prompt)
        # print("----------------")
        # print(response)
        return response.text.strip()
    except Exception as e:
        print(f"[WARN] Gagal generate summary: {e}")
        return "Ringkasan: Tidak tersedia\nSentimen: Neutral"

def analyze_sentiment_final(articles: list[str], financial_data) -> str:
        text = "\n\n".join(articles[:3])  # batasi agar tidak terlalu panjang
        prompt = f"""
    Berikut adalah beberapa artikel berita tentang saham:

    \"\"\"
    {text}
    \"\"\"

    Dan ini adalah data keuangan saham {financial_data['Stock']}:
    - Harga: {financial_data['Price']}
    - PER: {financial_data['PE_Ratio']}
    - PBV: {financial_data['PB_Ratio']}
    - ROE: {financial_data['ROE']}
    - Dividend Yield: {financial_data['DividendYield']}%

    Berdasarkan data diatas, apakah saham ini tergolong Positif, Netral, atau Negatif dari berita dan data keuangan diatas. Balas hanya seperti ini:

    Sentimen: <Positive/Neutral/Negative>
    Penjelasan: <alasan singkat>
    """

        try:
            response = model.generate_content(prompt)
            sentiment = response.text.strip().capitalize()
            print("----------------")
            print(response)
            print("----------------")
            
            print("----------------")
            print(sentiment)
            print("----------------")

            return sentiment
        except Exception as e:
            print(f"[WARN] Gagal generate summary: {e}")
            return "Ringkasan: Tidak tersedia\nSentimen: Neutral"

def analyze_sentiment_text(text):
    # print(text)
    # print(text["PE_Ratio"])

    prompt = f"""
    Berikut adalah data keuangan saham {text['Stock']}:
    - Harga: {text['Price']}
    - PER: {text['PE_Ratio']}
    - PBV: {text['PB_Ratio']}
    - ROE: {text['ROE']}
    - Dividend Yield: {text['DividendYield']}%

    Berdasarkan data ini, apakah saham ini tergolong Positif, Netral, atau Negatif dari sisi fundamental? Balas hanya seperti ini:

    Sentimen: <Positive/Neutral/Negative>
    Penjelasan: <alasan singkat>
    """

    # prompt = f"Berikan sentimen (Positive, Negative, atau Neutral) berdasarkan data keuangan berikut:\n{text}\n\nSentimen:"
    # print(prompt)
    try:
        response = model.generate_content(prompt)
        sentiment = response.text.strip().capitalize()
        # print("----------------")
        # print(response)
        # print("----------------")
        
        # print("----------------")
        # print(sentiment)
        # print("----------------")
        
        # if sentiment not in ["Positive", "Negative", "Neutral"]:
        #     return "Neutral"  # fallback aman
        return sentiment
    except Exception as e:
        print(f"[WARN] Gagal analisis sentimen: {e}")
        return "Neutral"

