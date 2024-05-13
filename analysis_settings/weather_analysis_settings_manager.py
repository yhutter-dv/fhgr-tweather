from datetime import date

from analysis_settings.weather_analysis_config import WeatherAnalysisConfig
from analysis_settings.weather_analysis_settings import WeatherAnalysisSettings
from analysis_settings.weather_analysis_settings_subscriber import (
    WeatherAnalysisSettingsSubscriber,
)
from analysis_settings.weather_analysis_type import WeatherAnalysisType
from analysis_settings.weather_location_repository import WeatherLocationRepository
from analysis_settings.weather_metric import WeatherMetric


class WeatherAnalysisSettingsManager:
    def __init__(self, location_repository: WeatherLocationRepository | None = None):
        self._settings: WeatherAnalysisSettings | None = None
        self._subscribers: list[WeatherAnalysisSettingsSubscriber] = []
        self._location_repository = (
            location_repository
            if location_repository is not None
            else WeatherLocationRepository()
        )

    def _notify_subscribers(self):
        if self._settings is None:
            return
        for subscriber in self._subscribers:
            subscriber.on_settings_changed(self._settings)

    def subscribe(self, subscriber: WeatherAnalysisSettingsSubscriber):
        if subscriber in self._subscribers:
            return
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber: WeatherAnalysisSettingsSubscriber):
        if subscriber not in self._subscribers:
            return
        self._subscribers.remove(subscriber)

    def update_settings(
        self,
        location_name_one: str,
        location_name_two: str,
        metric: WeatherMetric,
        analysis_type: WeatherAnalysisType,
        date: date,
    ):
        location_one = self._location_repository.find_location_by_name(
            location_name_one
        )
        location_two = self._location_repository.find_location_by_name(
            location_name_two
        )
        if location_one is None:
            raise Exception(f"Could not find location with name '{location_name_one}'")

        if location_two is None:
            raise Exception(f"Could not find location with name '{location_name_two}'")

        configs = [
            WeatherAnalysisConfig(location=location_one, metric=metric, date=date),
            WeatherAnalysisConfig(location=location_two, metric=metric, date=date),
        ]
        new_settings = WeatherAnalysisSettings(
            configs=configs, analysis_type=analysis_type
        )
        if self._settings == new_settings:
            return

        self._settings = new_settings
        self._notify_subscribers()
