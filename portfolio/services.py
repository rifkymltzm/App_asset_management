from .providers.factory import (
    ProviderFactory
)


def fetch_current_price(
    ticker,
    provider="YAHOO"
):

    provider_class = (
        ProviderFactory.get_provider(
            provider
        )
    )

    return provider_class.get_current_price(
        ticker
    )


def fetch_historical_prices(
    ticker,
    period="1mo",
    provider="YAHOO"
):

    provider_class = (
        ProviderFactory.get_provider(
            provider
        )
    )

    return provider_class.get_historical_prices(
        ticker,
        period
    )


def fetch_instrument_info(
    ticker,
    provider="YAHOO"
):

    provider_class = (
        ProviderFactory.get_provider(
            provider
        )
    )

    return provider_class.get_instrument_info(
        ticker
    )