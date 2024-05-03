import unittest

from analysis_settings.weather_location import WeatherLocation
from analysis_settings.weather_location_repository import WeatherLocationRepository


class TestWeatherLocationRepository(unittest.TestCase):
    def setUp(self) -> None:
        self._repository = WeatherLocationRepository()

    def tearDown(self) -> None:
        self._repository.clear_locations()

    def test_find_location_by_name(self):
        location = WeatherLocation(
            name="Chur", postal_code=7000, longitude=0.0, latitude=0.0
        )
        self._repository.add_location(location)

        result = self._repository.find_location_by_name("Chur")

        self.assertIsNotNone(result)

        if result is None:
            self.fail("Could not find a location")

        self.assertEqual("Chur", result.name)
        self.assertEqual(7000, result.postal_code)
        self.assertEqual(0.0, result.longitude)
        self.assertEqual(0.0, result.latitude)

        result = self._repository.find_location_by_name("Does not exist")

        self.assertIsNone(result)

    def test_find_locations_by_name(self):
        location = WeatherLocation(
            name="Mels", postal_code=8887, longitude=0.0, latitude=0.0
        )

        # Add multiple locations
        for i in range(3):
            location = WeatherLocation(
                name=f"Mels_{i}", postal_code=8887, longitude=0.0, latitude=0.0
            )
            self._repository.add_location(location)

        results = self._repository.find_locations_by_name("Me")
        self.assertEqual(3, len(results))
        self.assertEqual("Mels_0", results[0].name)
        self.assertEqual("Mels_1", results[1].name)
        self.assertEqual("Mels_2", results[2].name)
