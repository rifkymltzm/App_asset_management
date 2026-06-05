from .gold_api_provider import (
    GoldApiProvider
)

from .gold_scraper import (
    GoldScraper
)

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

        symbol = symbol.upper()

        # Primary source:
        # Indogold API (ANTAM & UBS)
        price = (
            GoldApiProvider
            .get_current_price(
                symbol
            )
        )

        if price:
            return price

        # Fallback source : Scraper Logam Mulia resmi (Jika Primary tidak tersedia)
        # ToDo:
        # Tambahkan UBS scraper dari ubslifestyle.com
        # sebagai fallback jika API Indogold gagal.
        if symbol == "ANTAM":

            return (
                GoldScraper
                .get_antam_price()
            )

        return None