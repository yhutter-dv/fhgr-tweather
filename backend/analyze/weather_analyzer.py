from analyze.weather_analysis_data import WeatherAnalysisData
from analyze.weather_analysis_result import WeatherAnalysisResult
from data.weather_api import WeatherApi
from analyze.weather_analysis_settings import (
    WeatherAnalysisSettings,
)
from data.weather_data_request import WeatherDataRequest
from location.weather_location_repository import WeatherLocationRepository


class WeatherAnalyzer:
    """This class returns an analysis result depending no the passed settings"""

    def __init__(self) -> None:
        self._weather_api = WeatherApi()
        self._repository = WeatherLocationRepository()

        # We could move this hardcoded value into a configuration file.
        self._num_supported_locations = 2

    def _validate_settings(self, settings: WeatherAnalysisSettings) -> None:
        """Validates if the given settings are correct.

        This method makes sure that the settings are valid.
        If they are not an exception with an appropriate description is thrown.
        """
        num_locations = len(settings.locations)
        num_metrics = len(settings.metrics)

        if settings.date is None:
            raise Exception(f"Expected to have a valid date but got '{settings.date}'")

        if num_locations != self._num_supported_locations:
            raise Exception(
                f"Expected to have exactly {self._num_supported_locations} locations but got {num_locations}"
            )

        if num_metrics < 1:
            raise Exception("Expected to have at least one metric but got none")

    def analyze(self, settings: WeatherAnalysisSettings) -> list[WeatherAnalysisResult]:
        """Makes an analysis depending on the given settings.

        This method makes an analyis depending on the given settings.
        If anything goes wrong the 'has_error' field as well as the 'error_message' are set.
        """
        self._validate_settings(settings)
        locations = settings.locations[: self._num_supported_locations]
        locations = [
            self._repository.find_location_by_name(location) for location in locations
        ]
        # Filter out locations which are None so we only have valid ones
        locations = [location for location in locations if location is not None]

        date = settings.date

        analysis_results = []

        # This is  a lookup dictionary in order to associated a given metrics with a list of received WeatherAnalysisData
        # Essentially it makes a structure like the following:
        #   { 'temperature' : [temperature_data_one, temperature_data_two], 'rain': ...}
        # This makes it easy to get the data associated with a specific metric, e.g. temperature, rain etc.
        data_for_metrics: dict[str, list[WeatherAnalysisData]] = dict()

        # Make a request per location and pass the metrics as a list
        for location in locations:
            request = WeatherDataRequest(
                location=location, date=date, metrics=settings.metrics
            )
            response = self._weather_api.make_request(request)
            for index, metric in enumerate(response.metrics):
                value = response.values[index] if not response.has_error else None
                data = WeatherAnalysisData(
                    location_name=location.name,
                    value=value,
                    has_error=response.has_error,
                    error_reason=response.error_reason,
                )
                # Initialize list if key does not exist
                if data_for_metrics.get(metric) is None:
                    data_for_metrics[metric] = []

                data_for_metrics[metric].append(data)

        # Iterate over the metrics and construct an analysis result for the given metric
        for metric in settings.metrics:
            results = data_for_metrics[metric]
            analysis_result = WeatherAnalysisResult(
                metric=metric,
                metric_friendly_name=metric.friendly_name(),
                date=date,
                results=results,
            )
            analysis_results.append(analysis_result)

        return analysis_results
