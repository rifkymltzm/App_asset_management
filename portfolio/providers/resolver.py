class AssetResolver:

    @staticmethod
    def resolve(symbol):

        symbol = symbol.strip().upper()

        # Crypto
        if symbol in [
            "BTC",
            "ETH",
            "SOL",
            "BNB",
            "ADA",
            "XRP",
        ]:
            return {
                "instrument_type": "Crypto",
                "provider": "COINGECKO",
            }

        # Emas
        if symbol in [
            "ANTAM",
            "UBS",
        ]:
            return {
                "instrument_type": "Emas",
                "provider": "SCRAPER",
            }

        # Default
        return {
            "instrument_type": "Saham",
            "provider": "YAHOO",
        }