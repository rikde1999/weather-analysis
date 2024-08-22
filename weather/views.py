from django.shortcuts import render
from .forms import CityForm
from .models import WeatherData, WeatherLocation
from weather.utils import (
    calculate_average_humidity,
    calculate_average_temperature,
    fetch_weather_data,
    is_extreme_weather,
)
from django.utils import timezone
from datetime import timedelta


def get_weather_view(request):
    form = CityForm()
    weather_data = None
    alert_message = None
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data.get("city")

            if city:
                data = fetch_weather_data(city)
                if isinstance(data, dict) and "error" in data:
                    error_message = data["error"]
                else:

                    location_data = data.get("location", {})
                    location = WeatherLocation.objects.filter(
                        name__iexact=location_data.get("name")
                    ).last()

                    if location:
                        weather_data = (
                            WeatherData.objects.filter(location=location)
                            .order_by("-last_updated")
                            .first()
                        )

                        if weather_data and is_extreme_weather(weather_data):
                            alert_message = "Extreme weather conditions detected!"

    return render(
        request,
        "weather_display.html",
        {
            "form": form,
            "weather_data": weather_data,
            "alert_message": alert_message,
        },
    )


def trends_view(request):
    form = CityForm()
    average_temp = None
    average_humidity = None
    city_name = None
    error = None

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data.get("city")

            location = WeatherLocation.objects.filter(name__iexact=city_name).last()

            if location:
                now = timezone.now()
                twenty_four_hours_ago = now - timedelta(hours=24)

                weather_data = WeatherData.objects.filter(
                    location=location, last_updated__gte=twenty_four_hours_ago
                )

                average_temp = calculate_average_temperature(weather_data)
                average_humidity = calculate_average_humidity(weather_data)
            else:
                error = "No city found in the database."
        else:
            error = "Invalid form submission."

    context = {
        "form": form,
        "city_name": city_name,
        "average_temp": average_temp,
        "average_humidity": average_humidity,
        "error": error,
    }

    return render(request, "trends.html", context)
