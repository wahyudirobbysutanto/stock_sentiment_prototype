from config import get_connection
from datetime import datetime

def insert_batch(news_list, summary_sentiment, summary_text, stock_name):
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
        INSERT INTO HistorySummary (CallerID, Stock, Sentiment, Summary, Date)
        VALUES (?, ?, ?, ?, ?)
    """, (caller_id, stock_name, summary_sentiment, summary_text, datetime.now()))

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
        SELECT CallerID, Stock, Sentiment, Summary, Date
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

    columns = ["CallerID", "Stock", "Sentiment", "Summary", "Date"]
    # data = [dict(zip(columns, row)) for row in rows]
    data = []
    for row in rows:
        row_dict = dict(zip(columns, row))
        row_dict["Sentiment"] = clean_sentiment_label(row_dict["Sentiment"])
        data.append(row_dict)


    has_next = len(data) > limit
    return data[:limit], has_next



def get_history_detail(caller_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Stock, Sentiment, Summary, Date
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
        "summary": dict(zip(["Stock", "Sentiment", "Summary", "Date"], summary)) if summary else None,
        "articles": [dict(zip(["Title", "Link", "Content", "Sentiment"], row)) for row in articles]
    }
