from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('asset/add/', views.add_asset_view, name='add_asset'),
    path('asset/<int:pk>/edit/', views.edit_asset_view, name='edit_asset'),
    path('asset/<int:pk>/delete/', views.delete_asset_view, name='delete_asset'),
    path('api/chart-data/<str:ticker_symbol>/', views.chart_data_api, name='chart_data_api'),
    path('api/instrument/<str:ticker>/', views.instrument_lookup_api, name='instrument_lookup_api'),
]
