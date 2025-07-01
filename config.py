import pyodbc
import os

from dotenv import load_dotenv

load_dotenv()

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
USE_WINDOWS_AUTH = os.getenv("USE_WINDOWS_AUTH", "false").lower() == "true"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DRIVER = os.getenv("DRIVER")

def get_connection():
    if USE_WINDOWS_AUTH:
        conn_str = f'DRIVER={{{DRIVER}}};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};Trusted_Connection=yes;'
    else:
        # Tambahkan USERNAME & PASSWORD di .env jika pakai SQL Auth
        USERNAME = os.getenv("SQL_USERNAME")
        PASSWORD = os.getenv("SQL_PASSWORD")
        conn_str = f'DRIVER={{{DRIVER}}};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};UID={USERNAME};PWD={PASSWORD}'
    return pyodbc.connect(conn_str)