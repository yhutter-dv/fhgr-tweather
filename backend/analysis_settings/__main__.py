import os
import sys
import json
from datetime import date
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


def init_weather_location_repostitory_from_file(
    file_path: str,
) -> WeatherLocationRepository:
    repository = WeatherLocationRepository()

    with open(file_path, "r", encoding="utf-8") as f:
        cities = json.load(f)

    for city in cities:
        weather_location = WeatherLocation(
            name=city["name"],
            postal_code=city["postal_code"],
            longitude=city["longitude"],
            latitude=city["latitude"],
        )
        repository.add_location(weather_location)
    return repository


# Example class which subscribes to setting changes. Note that this will be done in the Dashboard Aggregate but for demo purpose a class is created here.
class SettingsSubscriber(WeatherAnalysisSettingsSubscriber):

    def on_settings_changed(self, settings: WeatherAnalysisSettings):
        print(f"Settings have changed and are now {settings}")


if __name__ == "__main__":
    CITIES_FILE_PATH = "analysis_settings/cities.json"
    if not os.path.isfile(CITIES_FILE_PATH):
        print(f"Could not locate file '{CITIES_FILE_PATH}'")
        sys.exit(1)

    repository = init_weather_location_repostitory_from_file(CITIES_FILE_PATH)
    weather_analysis_settings_manager = WeatherAnalysisSettingsManager(repository)
    subscriber = SettingsSubscriber()
    weather_analysis_settings_manager.subscribe(subscriber)

    # Simulate Settings change
    weather_analysis_settings_manager.update_settings(
        location_name_one="Chur",
        location_name_two="Buchs SG",
        metric=WeatherMetric.TEMPERATURE,
        analysis_type=WeatherAnalysisType.CHART,
        date=date.today(),
    )
