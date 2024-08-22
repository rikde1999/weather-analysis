import requests
from weather.models import WeatherCondition, WeatherData, WeatherLocation
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


def fetch_weather_data(city):
    """Call the weather API and save the data in our db

    Args:
        city (_type_): "Kolkata"

    Returns:
        _type_: None
    """
    api_key = settings.WEATHER_API_KEY
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    try:
        response = requests.get(url, timeout=10)
        try:
            data = response.json()

            if "error" in data:
                error_code = data["error"].get("code")
                error_message = data["error"].get(
                    "message", "Unknown error from the API"
                )
                return {"error": f" Error : {error_message}"}

            location_data = data.get("location")
            if location_data:
                location, _ = WeatherLocation.objects.get_or_create(
                    name=location_data.get("name"),
                    region=location_data.get("region"),
                    country=location_data.get("country"),
                    latitude=location_data.get("lat"),
                    longitude=location_data.get("lon"),
                    localtime=location_data.get("localtime"),
                )
            else:
                return {"error": "Location data is missing from the API response."}

            current_data = data.get("current")
            if current_data:
                condition_data = current_data.get("condition")
                if condition_data:
                    condition, _ = WeatherCondition.objects.get_or_create(
                        text=condition_data.get("text"),
                        icon=condition_data.get("icon"),
                        code=condition_data.get("code"),
                    )
                else:
                    return {"error": "Condition data is missing from the API response."}

                WeatherData.objects.create(
                    location=location,
                    condition=condition,
                    last_updated=current_data.get("last_updated"),
                    temp_c=current_data.get("temp_c"),
                    temp_f=current_data.get("temp_f"),
                    is_day=current_data.get("is_day"),
                    wind_mph=current_data.get("wind_mph"),
                    wind_kph=current_data.get("wind_kph"),
                    humidity=current_data.get("humidity"),
                    cloud=current_data.get("cloud"),
                    feelslike_c=current_data.get("feelslike_c"),
                    feelslike_f=current_data.get("feelslike_f"),
                )
            else:
                return {
                    "error": "Current weather data is missing from the API response."
                }

            return data

        except ValueError:
            return {"error": "Invalid JSON response from the API"}

    except Exception as e:

        return {"error": str(e)}


def get_weather_data_last_24_hours():
    """Getting 24 hours data

    Returns:
        _type_: queryset
    """
    now = timezone.now()
    twenty_four_hours_ago = now - timedelta(hours=24)
    return WeatherData.objects.filter(last_updated__gte=twenty_four_hours_ago)


def calculate_average_temperature(data):
    """Calculate average temprature

    Returns:
        _type_: temperature
    """
    temperatures = [entry.temp_c for entry in data if entry.temp_c is not None]
    if temperatures:
        return sum(temperatures) / len(temperatures)
    return None


def calculate_average_humidity(data):
    """Calculate average humidity

    Returns:
        _type_: int
    """
    humidities = [entry.humidity for entry in data if entry.humidity is not None]
    if humidities:
        return sum(humidities) / len(humidities)
    return None


def is_extreme_weather(weather_data):
    """checking if the weather is extreme.

    Returns:
        _type_: Boolean
    """
    extreme_temp_threshold = 34
    extreme_wind_speed_threshold = 10

    if (
        weather_data.temp_c > extreme_temp_threshold
        or weather_data.wind_kph > extreme_wind_speed_threshold
    ):

        return True
    return False
