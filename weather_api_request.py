import requests


def fetch_weather_data(city):
    api_key = "6e3951e8b00e4fcd861141119242108"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url)
    return response.json()


print(fetch_weather_data("durgapur"))
