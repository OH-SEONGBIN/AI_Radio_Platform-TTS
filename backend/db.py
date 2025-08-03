import pymysql
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        db=os.getenv("DB_NAME", "myradio"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )