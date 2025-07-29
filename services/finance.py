from yahooquery import Ticker
from datetime import datetime
from config import get_connection  # pastikan sudah ada koneksi SQL Server
import pyodbc

def get_fundamentals(stock_code):
    stock_key = f"{stock_code}.JK"
    ticker = Ticker(stock_key)
    try:
        summary = ticker.summary_detail.get(stock_key, {})
        stats = ticker.key_stats.get(stock_key, {})
        financial = ticker.financial_data.get(stock_key, {})
        price_data = ticker.price.get(stock_key, {})

        data = {
            "Stock": stock_code,
            "Price": price_data.get("regularMarketPrice") or summary.get("regularMarketPrice"),
            "EPS": stats.get("trailingEps"),
            "BookValue": stats.get("bookValue"),
            "PE_Ratio": summary.get("trailingPE"),
            "PB_Ratio": stats.get("priceToBook"),
            "ROE": stats.get("returnOnEquity") or financial.get("returnOnEquity"),
            "Forward_PE": summary.get("forwardPE"),
            "DividendYield": (summary.get("dividendYield", 0) or 0) * 100,
            "DebtEquity": stats.get("debtToEquity"),
            "MarketCap": stats.get("marketCap"),
            "Currency": summary.get("currency")
        }
        # print(data);
        save_to_database(data)
        return data
        
    except Exception as e:
        print(f"[ERROR] Gagal mengambil data untuk {stock_code}: {e}")
        return None


def save_to_database(data):
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Simpan ke archive
    cursor.execute("""
        SELECT [Stock],[Price],[EPS],[BookValue],[PE_Ratio],[PB_Ratio],[ROE],[Forward_PE],
            [DividendYield],[DebtEquity],[MarketCap], [Currency], [LastUpdated]
        FROM StockFundamentals
        WHERE Stock = ?
    """, (data['Stock'],))
    old_data = cursor.fetchone()

    if old_data:
        cursor.execute("""
            INSERT INTO StockFundamentalsArchive 
            ([Stock],[Price],[EPS],[BookValue],[PE_Ratio],[PB_Ratio],[ROE],[Forward_PE],
            [DividendYield],[DebtEquity],[MarketCap], [Currency], [LastUpdated])
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (*old_data,))

    # 2. Simpan ke StockFundamentals (UPSERT)
    cursor.execute("""
        MERGE StockFundamentals AS target
        USING (SELECT ? AS Stock) AS source
        ON target.Stock = source.Stock
        WHEN MATCHED THEN 
            UPDATE SET Price = ?, EPS = ?, BookValue = ?, PE_Ratio = ?, PB_Ratio = ?, ROE = ?, 
                Forward_PE = ?, DividendYield = ?, DebtEquity = ?, MarketCap = ?, Currency = ?, LastUpdated = GETDATE()
        WHEN NOT MATCHED THEN
            INSERT ([Stock],[Price],[EPS],[BookValue],[PE_Ratio],[PB_Ratio],[ROE],[Forward_PE],[DividendYield],[DebtEquity],[MarketCap],[Currency])
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (data["Stock"],  # For match
          data["Price"], data["EPS"], data["BookValue"], data["PE_Ratio"], data["PB_Ratio"],
          data["ROE"], data["Forward_PE"], data["DividendYield"], data["DebtEquity"],
          data["MarketCap"], data["Currency"],  # For update
          data["Stock"], data["Price"], data["EPS"], data["BookValue"], data["PE_Ratio"],
          data["PB_Ratio"], data["ROE"], data["Forward_PE"], data["DividendYield"],
          data["DebtEquity"], data["MarketCap"], data["Currency"]))  # For insert

    conn.commit()
    conn.close()
    print(f"[INFO] Data untuk {data['Stock']} berhasil disimpan.")

# if __name__ == "__main__":
#     kode_saham = input("Masukkan kode saham (contoh: BBRI): ").upper()
#     hasil = get_fundamentals(kode_saham)
#     print(hasil)
#     if hasil:
#         save_to_database(hasil)
