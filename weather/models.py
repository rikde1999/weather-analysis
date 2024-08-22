from django.db import models


class WeatherLocation(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    localtime = models.DateTimeField()

    def __str__(self):
        return f"{self.name}, {self.region}, {self.country}"


class WeatherCondition(models.Model):
    text = models.CharField(max_length=100)
    icon = models.URLField(max_length=200)
    code = models.IntegerField()

    def __str__(self):
        return f"{self.text}, {self.code}"


class WeatherData(models.Model):
    location = models.ForeignKey(WeatherLocation, on_delete=models.CASCADE)
    condition = models.ForeignKey(WeatherCondition, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(null=True, blank=True)
    temp_c = models.FloatField(null=True, blank=True)
    temp_f = models.FloatField(null=True, blank=True)
    is_day = models.BooleanField(null=True, blank=True)
    wind_mph = models.FloatField(null=True, blank=True)
    wind_kph = models.FloatField(null=True, blank=True)
    wind_degree = models.IntegerField(null=True, blank=True)
    humidity = models.IntegerField()
    cloud = models.IntegerField()
    feelslike_c = models.FloatField()
    feelslike_f = models.FloatField()

    def __str__(self) -> str:
        return f" {self.location.country}, {self.humidity}, {self.last_updated}"
