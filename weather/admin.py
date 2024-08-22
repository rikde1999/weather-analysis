from django.contrib import admin
from .models import WeatherLocation, WeatherCondition, WeatherData


@admin.register(WeatherLocation)
class WeatherLocationAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "country", "latitude", "longitude", "localtime")
    search_fields = ("name", "region", "country")
    list_filter = ("country", "region")


@admin.register(WeatherCondition)
class WeatherConditionAdmin(admin.ModelAdmin):
    list_display = ("text", "icon", "code")
    search_fields = ("text",)
    list_filter = ("code",)


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = (
        "location",
        "condition",
        "last_updated",
        "temp_c",
        "temp_f",
        "is_day",
        "wind_mph",
        "wind_kph",
        "wind_degree",
        "humidity",
        "cloud",
        "feelslike_c",
        "feelslike_f",
    )
    search_fields = ("location__name", "condition__text")
    list_filter = ("location", "condition", "last_updated")
    date_hierarchy = "last_updated"
