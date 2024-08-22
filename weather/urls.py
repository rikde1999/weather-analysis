# weather/urls.py
from django.urls import path
from .views import get_weather_view, trends_view

urlpatterns = [
    path("", get_weather_view, name="get_weather"),
    path("trends/", trends_view, name="trends"),
]
