import unittest

from data.weather_data_request import WeatherDataRequest

class TestWeatherDataRequest(unittest.TestCase):
    def setUp(self):
        self.weather_data_request = WeatherDataRequest()

    def test_is_valid(self):
        """Test if a weather data request is valid"""
        self.assertTrue(self.weather_data_request.is_valid())


if __name__ == "__main__":
    unittest.main(verbosity=2)
