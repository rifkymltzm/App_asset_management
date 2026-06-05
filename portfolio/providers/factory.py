from .yahoo_provider import YahooProvider
from .coingecko_provider import CoinGeckoProvider
from .gold_provider import GoldProvider
from .manual_provider import ManualProvider


class ProviderFactory:

    @staticmethod
    def get_provider(provider_name):

        providers = {
            "YAHOO": YahooProvider,
            "COINGECKO": CoinGeckoProvider,
            "SCRAPER": GoldProvider,
            "MANUAL": ManualProvider,
        }

        return providers.get(provider_name)