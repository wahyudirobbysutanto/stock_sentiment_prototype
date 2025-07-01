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
        return response.text.strip()
    except Exception as e:
        print(f"[WARN] Gagal generate summary: {e}")
        return "Ringkasan: Tidak tersedia\nSentimen: Neutral"
