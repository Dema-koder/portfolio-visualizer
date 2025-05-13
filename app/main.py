from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from app.db import Database
from app.plotting import create_portfolio_plot
import os

app = FastAPI()
db = Database(os.getenv("DB_URL", "postgresql://app_user:secretpass@localhost:5433/app_db"))

@app.get("/plot", response_class=HTMLResponse)
async def get_plot(period: str = "month"):
    periods = {
        "15min": ("График за 15 минут", None, 15),
        "30min": ("График за 30 минут", None, 30),
        "1h": ("График за 1 час", None, 60),
        "3h": ("График за 3 часа", None, 180),
        "6h": ("График за 6 часов", None, 360),
        "12h": ("График за 12 часов", None, 720),
        "day": ("Дневной график", 1, None),
        "week": ("Недельный график", 7, None),
        "month": ("Месячный график", 30, None),
        "year": ("Годовой график", 365, None)
    }

    if period not in periods:
        raise HTTPException(status_code=400, detail="Invalid period")

    title, days, minutes = periods[period]
    df = db.get_portfolio_data(period_minutes=minutes, period_days=days)

    if df.empty:
        raise HTTPException(status_code=404, detail="No data available")

    img = create_portfolio_plot(df, title)
    return f"""
    <html>
        <body>
            <img src="data:image/png;base64,{img}" />
        </body>
    </html>
    """