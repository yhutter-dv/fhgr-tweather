import datetime
import unittest

from analysis_settings.weather_analysis_settings import WeatherAnalysisSettings
from analysis_settings.weather_analysis_settings_manager import (
    WeatherAnalysisSettingsManager,
)
from analysis_settings.weather_analysis_settings_subscriber import (
    WeatherAnalysisSettingsSubscriber,
)
from analysis_settings.weather_analysis_type import WeatherAnalysisType
from analysis_settings.weather_location import WeatherLocation
from analysis_settings.weather_location_repository import WeatherLocationRepository
from analysis_settings.weather_metric import WeatherMetric


class TestWeatherAnalysisSettingsManager(
    unittest.TestCase, WeatherAnalysisSettingsSubscriber
):
    def setUp(self):
        self._repository = WeatherLocationRepository()
        location = WeatherLocation(
            name="Chur", postal_code=7000, longitude=0.0, latitude=0.0
        )
        self._repository.add_location(location)

        self._settings_manager = WeatherAnalysisSettingsManager(
            location_repository=self._repository
        )
        self._settings: WeatherAnalysisSettings | None = None
        self._settings_manager.subscribe(self)

    def tearDown(self):
        self._settings_manager.unsubscribe(self)

    def on_settings_changed(self, settings: WeatherAnalysisSettings):
        self._settings = settings

    def test_subscribe_unsubscribe(self):
        location_name_one = "Chur"
        location_name_two = "Chur"
        metric = WeatherMetric.RAIN
        analysis_type = WeatherAnalysisType.TEXT
        now = datetime.datetime.now()

        self._settings_manager.update_settings(
            location_name_one=location_name_one,
            location_name_two=location_name_two,
            metric=metric,
            analysis_type=analysis_type,
            date=now,
        )

        self.assertIsNotNone(self._settings)

        # This is sadly needed as the linter does not seem to understand that at this point settings is defined
        if self._settings is None:
            self.fail("Expected settings to be defined")

        self._settings_manager.unsubscribe(self)

        self._settings_manager.update_settings(
            location_name_one=location_name_one,
            location_name_two=location_name_two,
            metric=metric,
            analysis_type=WeatherAnalysisType.CHART,
            date=now,
        )

        if self._settings is None:
            self.fail("Expected settings to be defined")

        self.assertNotEqual(WeatherAnalysisType.CHART, self._settings.analysis_type)

    def test_update_settings(self):
        location_name_one = "Chur"
        location_name_two = "Chur"
        metric = WeatherMetric.RAIN
        analysis_type = WeatherAnalysisType.TEXT
        now = datetime.datetime.now()

        self._settings_manager.update_settings(
            location_name_one=location_name_one,
            location_name_two=location_name_two,
            metric=metric,
            analysis_type=analysis_type,
            date=now,
        )

        self.assertIsNotNone(self._settings)

        # This is sadly needed as the linter does not seem to understand that at this point settings is defined
        if self._settings is None:
            self.fail("Expected settings to be defined")

        config_one = self._settings.configs[0]
        config_two = self._settings.configs[1]
        self.assertEqual("Chur", config_one.location.name)
        self.assertEqual(WeatherMetric.RAIN, config_one.metric)
        self.assertEqual("Chur", config_two.location.name)
        self.assertEqual(WeatherMetric.RAIN, config_two.metric)
        self.assertEqual(WeatherAnalysisType.TEXT, self._settings.analysis_type)


if __name__ == "__main__":
    unittest.main(verbosity=2)
