import requests
from commands.base_command import Command
from utils.decorators import log_execution, retry


class WeatherCommand(Command):

    BASE_URL = "https://wttr.in/{city}?format=j1"

    def __init__(self, bot, message, city: str):
        super().__init__(bot, message)
        self.city = city

    @log_execution
    def execute(self):
        try:
            self.send(f"🌍 Getting weather for {self.city}...")
            data = self._fetch(self.city)
            self.send(self._format(data))
        except requests.exceptions.ConnectionError:
            self.send("❌ No internet connection.")
        except requests.exceptions.Timeout:
            self.send("❌ Request timed out.")
        except Exception as e:
            self.send(f"❌ ERROR WEATHER: {e}")

    @retry(times=3, delay=2)
    def _fetch(self, city: str) -> dict:
        """Запрос к wttr.in API."""
        url = self.BASE_URL.format(city=city)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def _format(self, data: dict) -> str:
        """Форматирует ответ API в читаемый текст."""
        current = data["current_condition"][0]
        area = data["nearest_area"][0]

        city_name = area["areaName"][0]["value"]
        country = area["country"][0]["value"]

        temp_c = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]
        wind_kmph = current["windspeedKmph"]
        description = current["weatherDesc"][0]["value"]
        visibility = current["visibility"]
        pressure = current["pressure"]

        return (
            f"🌤 Weather in {city_name}, {country}\n"
            f"{'─' * 25}\n"
            f"🌡 Temperature:  {temp_c}°C\n"
            f"🤔 Feels like:   {feels_like}°C\n"
            f"☁️  Condition:    {description}\n"
            f"💧 Humidity:     {humidity}%\n"
            f"💨 Wind:         {wind_kmph} km/h\n"
            f"👁 Visibility:   {visibility} km\n"
            f"🔵 Pressure:     {pressure} hPa"
        )