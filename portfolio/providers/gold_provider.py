class GoldProvider:

    GOLD_PRODUCTS = {
        "ANTAM": {
            "ticker": "ANTAM",
            "name": "Emas Antam",
        },
        "UBS": {
            "ticker": "UBS",
            "name": "Emas UBS",
        },
    }

    @classmethod
    def get_instrument_info(cls, symbol):

        symbol = symbol.upper()

        if symbol not in cls.GOLD_PRODUCTS:
            return None

        product = cls.GOLD_PRODUCTS[symbol]

        return {
            "ticker": product["ticker"],
            "name": product["name"],
            "instrument_type": "Emas",
            "provider": "SCRAPER",
            "current_price": 0,
        }

    
    @classmethod
    def get_current_price(
        cls,
        symbol
    ):
        """
        Harga emas sementara.
        Nanti akan diganti dengan scraper Antam/UBS.
        """

        data = cls.get_instrument_info(
            symbol
        )

        if not data:
            return None

        return data["current_price"]