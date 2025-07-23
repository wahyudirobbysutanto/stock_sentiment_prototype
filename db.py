from config import get_connection
from datetime import datetime

def insert_batch(news_list, stock_name, NewsSentiment, NewsSentimentSummary,
                 FundamentalSentiment=None, FundamentalSentimentSummary=None, FinalSentiment=None, FinalSummary=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT ISNULL(MAX(CallerID), 0) FROM WebsiteData")
    caller_id = cursor.fetchone()[0] + 1

    for item in news_list:
        cursor.execute("""
            INSERT INTO WebsiteData (Stock, Title, Link, Content, Sentiment, Date, CallerID)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (item['Stock'], item['Title'], item['Link'], item['Content'],
              item['Sentiment'], item['Date'], caller_id))

    cursor.execute("""
        INSERT INTO HistorySummary (
            CallerID, Stock, 
            NewsSentiment, NewsSentimentSummary, 
            FundamentalSentiment, FundamentalSentimentSummary, 
            FinalSentiment, FinalSummary, 
            Date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            caller_id, stock_name, 
            NewsSentiment, NewsSentimentSummary,
            FundamentalSentiment, FundamentalSentimentSummary,
            FinalSentiment, FinalSummary,
            datetime.now()
        ))




    conn.commit()
    conn.close()
    return caller_id


def clean_sentiment_label(sentiment):
    if sentiment and '(' in sentiment:
        return sentiment.split('(')[0].strip().title()
    return sentiment.title() if sentiment else 'Neutral'


def get_history(limit=5, offset=0, date_filter=None):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT CallerID, Stock, 
            NewsSentiment, NewsSentimentSummary, 
            FundamentalSentiment, FundamentalSentimentSummary, 
            FinalSentiment, FinalSummary, 
            Date
        FROM HistorySummary
    """
    params = []

    if date_filter:
        sql += " WHERE CAST(Date AS DATE) = ?"
        params.append(date_filter)

    sql += " ORDER BY Date DESC OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
    params.extend([offset, limit + 1])  # ambil 1 lebih banyak

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    columns = ["CallerID", "Stock", "NewsSentiment", "NewsSentimentSummary", "FundamentalSentiment", "FundamentalSentimentSummary", "FinalSentiment", "FinalSummary", "Date"]
    # data = [dict(zip(columns, row)) for row in rows]
    data = []
    for row in rows:
        row_dict = dict(zip(columns, row))
        row_dict["NewsSentiment"] = clean_sentiment_label(row_dict["NewsSentiment"])
        data.append(row_dict)


    has_next = len(data) > limit
    return data[:limit], has_next



def get_history_detail(caller_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT CallerID, Stock, 
            NewsSentiment, NewsSentimentSummary, 
            FundamentalSentiment, FundamentalSentimentSummary, 
            FinalSentiment, FinalSummary, 
            Date
        FROM HistorySummary
        WHERE CallerID = ?
    """, (caller_id,))
    summary = cursor.fetchone()

    cursor.execute("""
        SELECT Title, Link, Content, Sentiment
        FROM WebsiteData
        WHERE CallerID = ?
    """, (caller_id,))
    articles = cursor.fetchall()

    conn.close()

    return {
        "summary": dict(zip(["CallerID", "Stock", "NewsSentiment", "NewsSentimentSummary", "FundamentalSentiment", "FundamentalSentimentSummary", "FinalSentiment", "FinalSummary", "Date"], summary)) if summary else None,
        "articles": [dict(zip(["Title", "Link", "Content", "Sentiment"], row)) for row in articles]
    }


# def insert_fundamental_data(data):
#     conn = get_connection()
#     cursor = conn.cursor()

#     # Pindahkan data lama ke archive jika ada
#     cursor.execute("SELECT * FROM StockFundamentals WHERE Stock = ?", (data['Stock'],))
#     old_data = cursor.fetchone()
#     if old_data:
#         cursor.execute("""
#             INSERT INTO StockFundamentalArchive 
#             (Stock, Price, EPS, BookValue, PE_Ratio, PB_Ratio, ROE, DividendYield, DebtToEquity, IntrinsicValue, MOS, Currency, ArchivedAt)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, (*old_data[1:], datetime.now()))

#         cursor.execute("DELETE FROM StockFundamental WHERE Stock = ?", (data['Stock'],))

#     # Simpan data terbaru
#     cursor.execute("""
#         INSERT INTO StockFundamentals
#         (Stock, Price, EPS, BookValue, PE_Ratio, PB_Ratio, ROE, DividendYield, DebtToEquity, IntrinsicValue, MOS, Currency, LastUpdated)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, (
#         data['Stock'], data['Price'], data['EPS'], data['BookValue'], data['PE_Ratio'], data['PB_Ratio'],
#         data['ROE'], data['DividendYield'], data['DebtToEquity'], data['IntrinsicValue'], data['MOS'],
#         data['Currency'], datetime.now()
#     ))

#     conn.commit()
#     conn.close()
