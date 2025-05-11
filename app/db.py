import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
import pandas as pd

class Database:
    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url)

    def get_portfolio_data(self, period_days: int = 30):
        query = sql.SQL("""
            SELECT time, value 
            FROM stoncks 
            WHERE time >= %s
            ORDER BY time
        """)
        date_from = datetime.now() - timedelta(days=period_days)

        with self.conn.cursor() as cursor:
            cursor.execute(query, (date_from,))
            data = cursor.fetchall()

        df = pd.DataFrame(data, columns=['time', 'value'])
        df['time'] = pd.to_datetime(df['time'])
        return df