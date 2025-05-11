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
        "day": ("Дневной график", 1),
        "week": ("Недельный график", 7),
        "month": ("Месячный график", 30),
        "year": ("Годовой график", 365)
    }

    if period not in periods:
        raise HTTPException(status_code=400, detail="Invalid period")

    title, days = periods[period]
    df = db.get_portfolio_data(days)

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