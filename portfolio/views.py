from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import InvestmentInstrument, UserAsset
from .services import fetch_current_price, fetch_historical_prices, fetch_instrument_info
from decimal import Decimal
from django.http import JsonResponse

@login_required
def instrument_lookup_api(request, ticker):

    instrument = InvestmentInstrument.objects.filter(
        ticker_symbol__istartswith=ticker.upper()
    ).first()

    if not instrument:

        data = fetch_instrument_info(ticker)

        if not data:
            return JsonResponse({
                "success": False,
                "message": "Instrumen tidak ditemukan"
            }, status=404)

        instrument = InvestmentInstrument.objects.create(
            ticker_symbol=data["ticker"],
            name=data["name"],
            instrument_type=data["instrument_type"],
            current_price=data["current_price"]
        )

    return JsonResponse({
        "success": True,
        "ticker": instrument.ticker_symbol,
        "name": instrument.name,
        "instrument_type": instrument.instrument_type,
        "current_price": float(instrument.current_price),
    })

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    email = forms.EmailField(required=False, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Konfirmasi Password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        username = cleaned_data.get("username")

        if username and User.objects.filter(username=username).exists():
            self.add_error('username', 'Username sudah terdaftar.')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Konfirmasi password tidak cocok.')
        
        return cleaned_data

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            messages.success(request, 'Registrasi berhasil! Selamat datang.')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Selamat datang kembali, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Username atau password salah.')
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Anda telah keluar dari akun.')
    return redirect('login')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Ambil semua aset yang dimiliki oleh user
    user_assets = UserAsset.objects.filter(user=request.user).select_related('instrument')
    
    # Caching cerdas: perbarui harga pasar jika harga terakhir diperbarui > 5 menit yang lalu
    five_minutes_ago = timezone.now() - timedelta(minutes=5)
    
    # Kumpulkan instrumen unik dari portfolio user yang perlu diperbarui
    instruments_to_update = InvestmentInstrument.objects.filter(
        user_assets__user=request.user,
        last_updated__lt=five_minutes_ago
    ).distinct()
    
    for instrument in instruments_to_update:
        new_price = fetch_current_price(instrument.ticker_symbol)
        if new_price is not None:
            instrument.current_price = Decimal(new_price)
            instrument.save()
            
    # Ambil ulang aset setelah pembaruan harga agar data terhitung akurat
    user_assets = UserAsset.objects.filter(user=request.user).select_related('instrument')
    
    # Hitung metrik ringkasan portofolio
    total_value = Decimal(0.0)
    total_cost = Decimal(0.0)
    
    for asset in user_assets:
        total_value += asset.current_value
        total_cost += asset.total_cost
        
    total_pnl = total_value - total_cost
    total_pnl_percentage = Decimal(0.0)
    if total_cost > 0:
        total_pnl_percentage = (total_pnl / total_cost) * 100

    # Hitung data alokasi untuk grafik
    allocation_data = []

    for asset in user_assets:
        allocation_data.append({
            "symbol": asset.instrument.ticker_symbol,
            "value": float(asset.current_value)
        })
        
    context = {
        'user_assets': user_assets,
        'total_value': total_value,
        'total_cost': total_cost,
        'total_pnl': total_pnl,
        'total_pnl_percentage': total_pnl_percentage,
        'allocation_data': allocation_data,
    }
    return render(request, 'dashboard.html', context)

def add_asset_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':

        ticker_symbol = request.POST.get(
            'ticker_symbol'
        ).strip().upper()

        quantity_str = request.POST.get('quantity')

        average_buy_price_str = request.POST.get(
            'average_buy_price'
        )

        instrument = InvestmentInstrument.objects.filter(
            ticker_symbol__istartswith=ticker_symbol.upper()
        ).first()

        if not instrument:

            data = fetch_instrument_info(ticker_symbol)

            if not data:
                return render(
                    request,
                    'asset_form.html',
                    {
                        'form_type': 'add',
                        'error_message': 'Instrumen tidak ditemukan'
                    }
                )

            instrument = InvestmentInstrument.objects.create(
                ticker_symbol=data["ticker"],
                name=data["name"],
                instrument_type=data["instrument_type"],
                current_price=data["current_price"]
            )

        # gunakan data dari database
        ticker_symbol = instrument.ticker_symbol
        name = instrument.name
        instrument_type = instrument.instrument_type

        try:
            quantity = Decimal(quantity_str)
            average_buy_price = Decimal(average_buy_price_str)

            if instrument_type == "Saham":
                quantity *= 100

            if quantity <= 0 or average_buy_price <= 0:
                raise ValueError(
                    "Jumlah dan harga beli harus lebih dari 0."
                )
            
            # Pancing harga live saat pendaftaran pertama kali
            live_price = fetch_current_price(ticker_symbol)
            default_price = Decimal(live_price) if live_price is not None else average_buy_price
            
            # Jika instrumen sudah ada, kita perbarui datanya
            if not created:
                instrument.name = name
                instrument.instrument_type = instrument_type
                if live_price is not None:
                    instrument.current_price = Decimal(live_price)
                instrument.save()
                
            # Dapatkan atau buat UserAsset
            user_asset, asset_created = UserAsset.objects.get_or_create(
                user=request.user,
                instrument=instrument,
                defaults={
                    'quantity': quantity,
                    'average_buy_price': average_buy_price,
                }
            )
            
            # Jika user sudah punya aset ini, gabungkan kepemilikannya (hitung rata-rata baru)
            if not asset_created:
                new_qty = user_asset.quantity + quantity
                new_cost = (user_asset.quantity * user_asset.average_buy_price) + (quantity * average_buy_price)
                user_asset.average_buy_price = new_cost / new_qty
                user_asset.quantity = new_qty
                user_asset.save()
                
            messages.success(request, f"Aset {ticker_symbol} berhasil disimpan!")
            return redirect('dashboard')
            
        except (ValueError, Exception) as e:
            return render(request, 'asset_form.html', {
                'form_type': 'add',
                'error_message': f"Gagal menyimpan aset: {str(e)}",
                'ticker_symbol': ticker_symbol,
                'name': name,
                'instrument_type': instrument_type,
                'quantity': quantity_str,
                'average_buy_price': average_buy_price_str,
            })
            
    return render(request, 'asset_form.html', {'form_type': 'add'})

def edit_asset_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
        
    asset = get_object_or_404(UserAsset, pk=pk, user=request.user)
    
    if request.method == 'POST':
        quantity_str = request.POST.get('quantity')
        average_buy_price_str = request.POST.get('average_buy_price')
        
        try:
            quantity = Decimal(quantity_str)
            average_buy_price = Decimal(average_buy_price_str)
            
            if quantity <= 0 or average_buy_price <= 0:
                raise ValueError("Jumlah dan harga beli harus lebih dari 0.")
                
            asset.quantity = quantity
            asset.average_buy_price = average_buy_price
            asset.save()
            
            messages.success(request, f"Aset {asset.instrument.ticker_symbol} berhasil diperbarui!")
            return redirect('dashboard')
            
        except (ValueError, Exception) as e:
            return render(request, 'asset_form.html', {
                'form_type': 'edit',
                'asset': asset,
                'error_message': f"Gagal memperbarui aset: {str(e)}",
            })
            
    return render(request, 'asset_form.html', {'form_type': 'edit', 'asset': asset})

def delete_asset_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
        
    asset = get_object_or_404(UserAsset, pk=pk, user=request.user)
    ticker = asset.instrument.ticker_symbol
    
    if request.method == 'POST':
        asset.delete()
        messages.success(request, f"Aset {ticker} berhasil dihapus dari portofolio.")
        return redirect('dashboard')
        
    return render(request, 'asset_confirm_delete.html', {'asset': asset})

def chart_data_api(request, ticker_symbol):
    """
    Menyediakan data grafik historis instrumen dalam format JSON untuk ApexCharts.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    period = request.GET.get('period', '1mo')
    data = fetch_historical_prices(ticker_symbol, period=period)
    
    if not data:
        return JsonResponse({'error': 'Data historis tidak ditemukan untuk ticker ini.'}, status=404)
        
    dates = [item['date'] for item in data]
    prices = [item['price'] for item in data]
    
    return JsonResponse({
        'ticker': ticker_symbol,
        'dates': dates,
        'prices': prices
    })
