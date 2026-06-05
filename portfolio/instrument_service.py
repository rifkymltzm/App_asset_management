from .models import InvestmentInstrument
from .providers.resolver import AssetResolver
from .providers.factory import ProviderFactory


class InstrumentService:

    @staticmethod
    def get_or_create_instrument(symbol):

        symbol = symbol.strip().upper()

        # Cari berdasarkan input user
        instrument = (
            InvestmentInstrument.objects
            .filter(
                ticker_symbol__istartswith=symbol
            )
            .first()
        )

        if instrument:
            return instrument

        asset_info = AssetResolver.resolve(
            symbol
        )

        provider_class = (
            ProviderFactory.get_provider(
                asset_info["provider"]
            )
        )

        data = (
            provider_class
            .get_instrument_info(symbol)
        )

        if not data:
            return None

        # Cek lagi menggunakan ticker final dari provider
        instrument = (
            InvestmentInstrument.objects
            .filter(
                ticker_symbol=data["ticker"]
            )
            .first()
        )

        if instrument:
            return instrument

        return (
            InvestmentInstrument.objects
            .create(
                ticker_symbol=data["ticker"],
                name=data["name"],
                instrument_type=data["instrument_type"],
                provider=data["provider"],
                current_price=data["current_price"],
            )
        )