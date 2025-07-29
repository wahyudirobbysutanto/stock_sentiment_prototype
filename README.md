# 📰 Stock News Sentiment Analyzer

A web-based tool to analyze stock news sentiment automatically using Google Gemini AI.  
This project is designed for research, education, or news-based stock monitoring.

## 🔧 Key Features

- Input any stock ticker (e.g., `BBRI`, `TLKM`, `BMRI`)
- Scrape recent stock-related news from Google News and popular news websites
- Extract article titles, links, and content using `readability`
- Sentiment analysis on each article with **Google Gemini 2.0 Flash**
- Automatic batch news summarization using AI
- Save results into:
  - **SQL Server** (`WebsiteData` and `HistorySummary` tables)
  - **JSON files** (one file per batch as backup)
- **Flask Web Interface**:
  - Stock input form
  - Analysis history with date filter & pagination
  - Detail page to inspect every batch

## 📦 Project Structure

```
project/
│
├── core/
│   ├── scraper.py          # News scraper and content extraction
│   ├── sentiment.py        # Gemini AI integration
│   └── utils.py            # JSON helpers, text cleaning utilities
│
├── output/                 # JSON files (one per batch)
│
├── data/                   
│   └── database.sql        # SQL schema for the database
│
├── services/
│   ├── db.py               # Database operations (SQL Server)
│   └── finance.py          # Get fundamental data and save to DB
│
├── templates/
│   ├── index.html          # Home page (form + history)
│   └── detail.html         # Batch detail page
│
├── app.py                  # Flask entry point
├── main.py                 # Scraping + sentiment pipeline (CLI)
├── config.py               # SQL Server connection using .env
│
├── .env                    # Secrets and configuration (ignored by git)
└── requirements.txt
```

## ⚙️ Example .env file

```env
SQL_SERVER=LAPTOP-XXXX
SQL_DATABASE=StockSentiment
USE_WINDOWS_AUTH=true
GEMINI_API_KEY=your_api_key_here
```

## ▶️ How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/wahyudirobbysutanto/stock_sentiment_prototype.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run Flask:
   ```bash
   python app.py
   ```

4. Open in your browser:
   ```
   http://localhost:5000
   ```

## 💡 Tech Stack

- Python (Flask, requests, BeautifulSoup, readability-lxml, pyodbc)
- SQL Server
- Google Gemini AI
- Bootstrap 5

## 🧪 Current Status

✅ Scraping and AI sentiment analysis implemented  
✅ Basic UI ready (input form, history, and detail view)  
🚧 Future improvements:
- Auto-scheduler for daily scraping
- Multi-stock batch processing
- Sentiment trend visualization

## 📜 License

MIT License — free to use and modify.
