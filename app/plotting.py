import matplotlib.pyplot as plt
from io import BytesIO
import base64

def create_portfolio_plot(df, title):
    plt.figure(figsize=(12, 6))
    plt.plot(df['time'], df['value'], marker='o', linestyle='-', color='b')

    plt.title(title)
    plt.xlabel('Дата')
    plt.ylabel('Стоимость портфеля')
    plt.grid(True)
    plt.xticks(rotation=45)

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')