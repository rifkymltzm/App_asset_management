from django.contrib import admin
from .models import InvestmentInstrument

# Register your models here.
@admin.register(InvestmentInstrument)
class InvestmentInstrumentAdmin(admin.ModelAdmin):
    list_display = (
        "ticker_symbol",
        "name",
        "instrument_type",
        "provider",
        "current_price",
    )