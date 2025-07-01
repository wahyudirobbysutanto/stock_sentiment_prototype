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
