import requests


class CoinGeckoProvider:

    BASE_URL = (
        "https://api.coingecko.com/api/v3"
    )

    SYMBOL_MAP = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana",
        "BNB": "binancecoin",
        "ADA": "cardano",
        "XRP": "ripple",
    }

    @classmethod
    def get_instrument_info(
        cls,
        symbol
    ):

        symbol = symbol.upper()

        coin_id = cls.SYMBOL_MAP.get(
            symbol
        )

        if not coin_id:
            return None

        response = requests.get(
            f"{cls.BASE_URL}/coins/{coin_id}"
        )

        if response.status_code != 200:
            return None

        data = response.json()

        return {
            "ticker": symbol,
            "name": data["name"],
            "instrument_type": "Crypto",
            "provider": "COINGECKO",
            "current_price": data[
                "market_data"
            ][
                "current_price"
            ][
                "idr"
            ]
        }


    @classmethod
    def get_current_price(
        cls,
        symbol
    ):

        symbol = symbol.upper()

        coin_id = cls.SYMBOL_MAP.get(
            symbol
        )

        if not coin_id:
            return None

        try:

            response = requests.get(
                f"{cls.BASE_URL}/simple/price",
                params={
                    "ids": coin_id,
                    "vs_currencies": "idr"
                }
            )

            if response.status_code != 200:
                return None

            data = response.json()

            return data[
                coin_id
            ][
                "idr"
            ]

        except Exception as e:

            print(
                f"CoinGecko error: {e}"
            )

            return None


    @classmethod
    def get_historical_prices(
        cls,
        symbol,
        period="1mo"
    ):
        return []