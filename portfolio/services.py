import yfinance as yf
from datetime import datetime

def fetch_current_price(ticker):
    """
    Menarik harga terkini dari Yahoo Finance untuk simbol tertentu.
    Mendukung saham, reksadana, dan cryptocurrency.
    """
    try:
        ticker_data = yf.Ticker(ticker)
        # Metode teraman: ambil data historis 1 hari terakhir
        history = ticker_data.history(period="1d")
        if not history.empty:
            price = history['Close'].iloc[-1]
            return float(price)
        
        # Fallback ke info dict jika data historis kosong
        info = ticker_data.info
        if 'regularMarketPrice' in info and info['regularMarketPrice'] is not None:
            return float(info['regularMarketPrice'])
        if 'currentPrice' in info and info['currentPrice'] is not None:
            return float(info['currentPrice'])
        return None
    except Exception as e:
        print(f"Error fetching current price for {ticker}: {e}")
        return None

def fetch_historical_prices(ticker, period="1mo"):
    """
    Menarik harga penutupan historis untuk membuat grafik pergerakan harga.
    Pilihan period: '1mo', '3mo', '6mo', '1y', 'ytd', 'max'
    """
    try:
        ticker_data = yf.Ticker(ticker)
        history = ticker_data.history(period=period)
        if history.empty:
            return []
        
        data_points = []
        for index, row in history.iterrows():
            date_str = index.strftime('%Y-%m-%d')
            data_points.append({
                'date': date_str,
                'price': float(row['Close'])
            })
        return data_points
    except Exception as e:
        print(f"Error fetching historical data for {ticker}: {e}")
        return []


def fetch_instrument_info(ticker):
    try:
        yf_ticker = (
            ticker if ticker.endswith(".JK")
            else f"{ticker}.JK"
        )

        stock = yf.Ticker(yf_ticker)

        history = stock.history(period="1d")

        if history.empty:
            return None

        info = stock.info

        return {
            "ticker": yf_ticker,
            "name": (
                info.get("longName")
                or info.get("shortName")
                or ticker
            ),
            "instrument_type": "Saham",
            "current_price": float(
                history["Close"].iloc[-1]
            ),
        }

    except Exception as e:
        print("Fetch Instrument Error:", e)
        return None