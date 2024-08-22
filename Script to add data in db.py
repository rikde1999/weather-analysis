from weather.models import WeatherLocation, WeatherCondition, WeatherData
from weather.utils import fetch_weather_data


def fetch_and_store_weather_data(city):
    data = fetch_weather_data(city)

    location_data = data["location"]
    location, _ = WeatherLocation.objects.get_or_create(
        name=location_data["name"],
        region=location_data["region"],
        country=location_data["country"],
        latitude=location_data["lat"],
        longitude=location_data["lon"],
        localtime=location_data["localtime"],
    )

    condition_data = data["current"]["condition"]
    condition, _ = WeatherCondition.objects.get_or_create(
        text=condition_data["text"],
        icon=condition_data["icon"],
        code=condition_data["code"],
    )

    current_data = data["current"]
    WeatherData.objects.create(
        location=location,
        condition=condition,
        last_updated=current_data["last_updated"],
        temp_c=current_data["temp_c"],
        temp_f=current_data["temp_f"],
        is_day=current_data["is_day"],
        wind_mph=current_data["wind_mph"],
        wind_kph=current_data["wind_kph"],
    )
