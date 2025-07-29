import json
import os
import re
from datetime import datetime

def clean_gemini_formatting(text):
    # Hapus triple asterisk ***bold***
    text = re.sub(r'\*{3}([^*]+)\*{3}', r'\1', text)
    # Hapus double asterisk **bold**
    text = re.sub(r'\*{2}([^*]+)\*{2}', r'\1', text)
    return text

import re

def clean_gemini_fundamental_formatting(text):
    sentiment = ""
    explanation = ""

    # Cari sentimen (case-insensitive)
    match_sentiment = re.search(r"sentimen:\s*(\w+)", text, re.IGNORECASE)
    if match_sentiment:
        sentiment = match_sentiment.group(1).capitalize()

    # Cari penjelasan (hingga akhir)
    match_explanation = re.search(r"penjelasan:\s*(.+)", text, re.IGNORECASE)
    if match_explanation:
        explanation = match_explanation.group(1).strip()

    return sentiment, explanation


def save_to_json(data, caller_id, stock_name):
    os.makedirs("output", exist_ok=True)

    # Format nama file: yyyyMMdd_STOCK_CALLERID.json
    today_str = datetime.now().strftime("%Y%m%d")
    filename = f"{today_str}_{stock_name.upper()}_{str(caller_id).zfill(3)}.json"

    filepath = os.path.join("output", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[INFO] Hasil disimpan ke {filepath}")
