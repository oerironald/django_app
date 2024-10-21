from django.urls import path
from .views import fetch_counties

urlpatterns = [
    path('', fetch_counties, name='fetch_counties'),
]