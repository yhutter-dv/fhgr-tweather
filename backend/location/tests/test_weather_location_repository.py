import unittest

from location.weather_location import WeatherLocation
from location.weather_location_repository import WeatherLocationRepository


class TestWeatherLocationRepository(unittest.TestCase):
    def test_find_location_by_name(self):
        repository = WeatherLocationRepository()
        result = repository.find_location_by_name("Chur")

        self.assertIsNotNone(result)
        self.assertEqual("Chur", result.name)
        self.assertEqual(7000, result.postal_code)

        result = repository.find_location_by_name("Does not exist")
        self.assertIsNone(result)

    def test_find_locations_by_name(self):
        repository = WeatherLocationRepository()
        results = repository.find_locations_by_name("Aeug")
        self.assertEqual(2, len(results))
        self.assertEqual("Aeugst am Albis", results[0].name)
        self.assertEqual("Aeugstertal", results[1].name)
