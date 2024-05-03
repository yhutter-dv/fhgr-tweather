from shared.date_time_range import DateTimeRange
from analysis_settings.weather_analysis_sample import WeatherAnalysisSample
from analysis_settings.weather_analysis_settings import WeatherAnalysisSettings
from analysis_settings.weather_analysis_settings_subscriber import (
    WeatherAnalysisSettingsSubscriber,
)
from analysis_settings.weather_analysis_type import WeatherAnalysisType
from analysis_settings.weather_location_repository import WeatherLocationRepository
from analysis_settings.weather_metric import WeatherMetric


class WeatherAnalysisSettingsManager:
    def __init__(self, location_repository: WeatherLocationRepository):
        self._settings: WeatherAnalysisSettings | None = None
        self._subscribers: list[WeatherAnalysisSettingsSubscriber] = []
        self._location_repository = location_repository

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
        time_range: DateTimeRange,
    ):
        location_one = self._location_repository.find_location_by_name(
            location_name_one
        )
        location_two = self._location_repository.find_location_by_name(
            location_name_two
        )
        if location_one is None or location_two is None:
            raise Exception(
                f"Could not find locations for provided names {location_name_one} and {location_name_two}"
            )

        sample_one = WeatherAnalysisSample(
            location=location_one, metric=metric, date_time_range=time_range
        )
        sample_two = WeatherAnalysisSample(
            location=location_two, metric=metric, date_time_range=time_range
        )
        new_settings = WeatherAnalysisSettings(
            sample_one=sample_one, sample_two=sample_two, analysis_type=analysis_type
        )
        if self._settings == new_settings:
            return

        self._settings = new_settings
        self._notify_subscribers()
