from analyze.weather_analysis_result import WeatherAnalysisResult
from data.weather_api import WeatherApi
from analyze.weather_analysis_settings import (
    WeatherAnalysisSettings,
)
from data.weather_data_request import WeatherDataRequest
from location.weather_location import WeatherLocation
from location.weather_location_repository import WeatherLocationRepository


class WeatherAnalyzer:
    def __init__(self) -> None:
        self._weather_api = WeatherApi()
        self._repository = WeatherLocationRepository()

    def _validate_settings(self, settings: WeatherAnalysisSettings) -> None:
        num_locations = len(settings.locations)
        num_metrics = len(settings.metrics)

        if settings.date is None:
            raise Exception(f"Expected to have a valid date but got '{settings.date}'")

        if num_locations != 2:
            raise Exception(
                f"Expected to have exactly two locations but got {num_locations}"
            )

        if num_metrics < 1:
            raise Exception(f"Expected to have at least one metric but got none")

    def analyze(
        self, settings: WeatherAnalysisSettings
    ) -> list[WeatherAnalysisResult]:
        self._validate_settings(settings)

        location_name_one = settings.locations[0]
        location_name_two = settings.locations[1]
        location_one = self._repository.find_location_by_name(location_name_one)
        location_two = self._repository.find_location_by_name(location_name_two)

        if location_one is None:
            raise Exception(f"Could not find a location with the name '{location_name_one}'")
        elif location_two is None:
            raise Exception(f"Could not find a location with the name '{location_name_two}'")

        analysis_results = []

        for metric in settings.metrics:
            # TODO: Optimize this so that we can pass a list of metrics instead of iterating over it...
            request_location_one = WeatherDataRequest(location=location_one, date=settings.date, metric=metric)
            request_location_two = WeatherDataRequest(location=location_two, date=settings.date, metric=metric)
            response_location_one = self._weather_api.make_request(request_location_one)
            response_location_two = self._weather_api.make_request(request_location_two)
            analysis_result = WeatherAnalysisResult(metric=metric, result=[response_location_one, response_location_two])
            analysis_results.append(analysis_result)

        return analysis_results
