import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import MagicMock, patch
from commands.weather_command import WeatherCommand


def make_mock(chat_id=12345):
    bot = MagicMock()
    message = MagicMock()
    message.chat.id = chat_id
    return bot, message


class TestWeatherCommand(unittest.TestCase):

    def test_format_returns_string(self):
        bot, message = make_mock()
        cmd = WeatherCommand(bot, message, "Astana")

        fake_data = {
            "current_condition": [{
                "temp_C": "20",
                "FeelsLikeC": "18",
                "humidity": "45",
                "windspeedKmph": "15",
                "weatherDesc": [{"value": "Sunny"}],
                "visibility": "10",
                "pressure": "1013"
            }],
            "nearest_area": [{
                "areaName": [{"value": "Astana"}],
                "country": [{"value": "Kazakhstan"}]
            }]
        }

        result = cmd._format(fake_data)
        self.assertIsInstance(result, str)
        self.assertIn("Astana", result)
        self.assertIn("20°C", result)
        self.assertIn("Sunny", result)

    def test_execute_sends_error_on_connection_failure(self):
        import requests
        bot, message = make_mock()
        cmd = WeatherCommand(bot, message, "Astana")
        cmd._fetch = MagicMock(side_effect=requests.exceptions.ConnectionError)
        cmd.execute()

        bot.send_message.assert_called()
        args = bot.send_message.call_args[0]
        self.assertIn("❌", args[1])

    def test_execute_sends_error_on_timeout(self):
        import requests
        bot, message = make_mock()
        cmd = WeatherCommand(bot, message, "Astana")
        cmd._fetch = MagicMock(side_effect=requests.exceptions.Timeout)
        cmd.execute()

        bot.send_message.assert_called()
        args = bot.send_message.call_args[0]
        self.assertIn("❌", args[1])

    @patch("commands.weather_command.requests.get")
    def test_fetch_calls_correct_url(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {}
        bot, message = make_mock()
        cmd = WeatherCommand(bot, message, "London")

        try:
            cmd._fetch("London")
        except Exception:
            pass

        mock_get.assert_called_once()
        url = mock_get.call_args[0][0]
        self.assertIn("London", url)
        self.assertIn("wttr.in", url)


if __name__ == "__main__":
    unittest.main()