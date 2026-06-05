import yfinance as yf


class YahooProvider:

    @staticmethod
    def get_instrument_info(ticker):

        ticker = ticker.strip().upper()
        yf_ticker = (
            ticker
            if ticker.endswith(".JK")
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
            "provider": "YAHOO",
            "current_price": float(
                history["Close"].iloc[-1]
            ),
        }

    @staticmethod
    def get_current_price(ticker):

        ticker = ticker.strip().upper()

        stock = yf.Ticker(ticker)

        history = stock.history(period="1d")

        if history.empty:
            return None

        return float(
            history["Close"].iloc[-1]
        )

    @staticmethod
    def get_historical_prices(
        ticker,
        period="1mo"
    ):

        ticker = ticker.strip().upper()

        try:

            stock = yf.Ticker(ticker)

            history = stock.history(
                period=period
            )

            if history.empty:
                return []

            data_points = []

            for index, row in history.iterrows():

                data_points.append({
                    "date": index.strftime(
                        "%Y-%m-%d"
                    ),
                    "price": float(
                        row["Close"]
                    )
                })

            return data_points

        except Exception as e:

            print(
                f"Yahoo historical error: {e}"
            )

            return []