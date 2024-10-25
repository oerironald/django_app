from django.urls import path
from .views import fetch_counties, health_check, get_countries, get_counties, get_wards, get_postal_stations, country_info

urlpatterns = [
    path('', fetch_counties, name='fetch_counties'),
    path('health/', health_check, name='health_check'),
    path('country/', get_countries, name='get_countries'),
    path('county/', get_counties, name='get_counties'),
    path('wards/', get_wards, name='get_wards'),
    path('postal_stations/', get_postal_stations, name='get_postal_stations'),
    path('home/', country_info, name='country_info'),
]