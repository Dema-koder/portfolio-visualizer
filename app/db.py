import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
import pandas as pd

class Database:
    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url)

    def get_portfolio_data(self, period_minutes: int = None, period_days: int = None):
        query = sql.SQL("""
            SELECT time, value 
            FROM stoncks 
            WHERE time >= %s
            ORDER BY time
        """)

        if period_minutes is not None:
            date_from = datetime.now() - timedelta(minutes=period_minutes)
        elif period_days is not None:
            date_from = datetime.now() - timedelta(days=period_days)
        else:
            date_from = datetime.now() - timedelta(days=30)

        with self.conn.cursor() as cursor:
            cursor.execute(query, (date_from,))
            data = cursor.fetchall()

        df = pd.DataFrame(data, columns=['time', 'value'])
        df['time'] = pd.to_datetime(df['time'])

        df['time'] = df['time'] + pd.Timedelta(hours=3)

        return df