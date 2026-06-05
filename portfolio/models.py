from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User

class InvestmentInstrument(models.Model):
    INSTRUMENT_TYPES = [
        ('Saham', 'Saham'),
        ('Crypto', 'Crypto'),
        ('Emas', 'Emas'),
        ('Reksadana', 'Reksadana'),
        ('Obligasi', 'Obligasi'),
    ]
 
    DATA_PROVIDERS = [
        ('YAHOO', 'Yahoo Finance'),
        ('COINGECKO', 'CoinGecko'),
        ('SCRAPER', 'Web Scraper'),
        ('MANUAL', 'Manual'),
    ]
    
    ticker_symbol = models.CharField(max_length=20, unique=True, verbose_name="Ticker Symbol")
    name = models.CharField(max_length=100, verbose_name="Nama Instrumen")
    instrument_type = models.CharField(max_length=20, choices=INSTRUMENT_TYPES, default='Saham', verbose_name="Tipe Instrumen")
    provider = models.CharField(
        max_length=20,
        choices=DATA_PROVIDERS,
        default='YAHOO',
        verbose_name="Data Provider"
    )
    current_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.0, verbose_name="Harga Terkini")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Terakhir Diperbarui")

    def __str__(self):
        return f"{self.name} ({self.ticker_symbol})"


    def save(self, *args, **kwargs):

        self.ticker_symbol = (
            self.ticker_symbol.upper()
        )

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Instrumen Investasi"
        verbose_name_plural = "Instrumen Investasi"

    @property
    def display_ticker(self):
        if self.ticker_symbol.endswith(".JK"):
            return self.ticker_symbol[:-3]

        return self.ticker_symbol


    # Label satuan berdasarkan tipe instrumen
    @property
    def unit_label(self):

        units = {
            "Saham": "Lot",
            "Crypto": "Coin",
            "Emas": "Gram",
            "Reksadana": "Unit",
            "Obligasi": "Nominal",
        }

        return units.get(
            self.instrument_type,
            "Unit"
        )


class UserAsset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assets", verbose_name="Pengguna")
    instrument = models.ForeignKey(InvestmentInstrument, on_delete=models.CASCADE, related_name="user_assets", verbose_name="Instrumen")
    quantity = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="Jumlah")
    average_buy_price = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Harga Beli Rata-rata")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Dibuat")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Tanggal Diperbarui")

    @property
    def total_cost(self):
        return self.quantity * self.average_buy_price

    @property
    def current_value(self):
        return self.quantity * self.instrument.current_price

    @property
    def profit_loss(self):
        return self.current_value - self.total_cost

    @property
    def profit_loss_percentage(self):
        cost = self.total_cost
        if cost == 0:
            return 0
        return (self.profit_loss / cost) * 100

    # Quantity yang ditampilkan ke user
    @property
    def display_quantity(self):

        value = self.quantity

        # Saham disimpan dalam lembar, tampilkan dalam lot
        if self.instrument.instrument_type == "Saham":
            value = value / Decimal("100")

        # Hilangkan nol di belakang desimal
        return format(value, "f").rstrip("0").rstrip(".")


    def __str__(self):
        return f"{self.user.username} - {self.instrument.ticker_symbol} ({self.quantity})"

    class Meta:
        verbose_name = "Aset Pengguna"
        verbose_name_plural = "Aset Pengguna"
        unique_together = ('user', 'instrument')
