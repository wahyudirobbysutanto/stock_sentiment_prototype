import json
import os
from datetime import datetime

def save_to_json(data, caller_id, stock_name):
    os.makedirs("output", exist_ok=True)

    # Format nama file: yyyyMMdd_STOCK_CALLERID.json
    today_str = datetime.now().strftime("%Y%m%d")
    filename = f"{today_str}_{stock_name.upper()}_{str(caller_id).zfill(3)}.json"

    filepath = os.path.join("output", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[INFO] Hasil disimpan ke {filepath}")
