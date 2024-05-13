from analyze.weather_analysis_sample import WeatherAnalysisSample
from analyze.weather_chart_analysis_result import WeatherChartAnalysisResult
from analyze.weather_text_analysis_result import WeatherTextAnalysisResult
from data.weather_api import WeatherApi
from analysis_settings.weather_analysis_settings import (
    WeatherAnalysisSettings,
    WeatherAnalysisType,
)
from data.weather_data_request import WeatherDataRequest


class WeatherAnalyzer:

    def __init__(self, weather_api: WeatherApi) -> None:
        self._weather_api = weather_api

    def analyze(
        self, settings: WeatherAnalysisSettings
    ) -> WeatherChartAnalysisResult | WeatherTextAnalysisResult:
        num_configs = len(settings.configs)
        # Ensure that we have exactly to configurations, e.g. one per location we want to analyze
        if num_configs != 2:
            raise Exception(
                f"Expected to have exactly two configurations but got {num_configs}"
            )

        # Ensure that they both have the same metric
        if settings.configs[0].metric is not settings.configs[1].metric:
            raise Exception(
                f"Expected to have identical metrics but metrics were {settings.configs[0].metric} and {settings.configs[1].metric}"
            )

        location_one = settings.configs[0].location
        location_two = settings.configs[1].location
        request_for_location_one = WeatherDataRequest(
            location=location_one,
            date=settings.configs[0].date,
            metric=settings.configs[0].metric,
        )
        response_for_location_one = self._weather_api.make_request(
            request=request_for_location_one
        )

        if response_for_location_one.has_error:
            raise Exception(
                f"Response for location {location_one} failed due to {response_for_location_one.error_reason}"
            )

        sample_one = WeatherAnalysisSample(
            location_name=response_for_location_one.location.name,
            date=response_for_location_one.date,
            metric=response_for_location_one.metric,
            value=response_for_location_one.value,
        )

        request_for_location_two = WeatherDataRequest(
            location=location_two,
            date=settings.configs[1].date,
            metric=settings.configs[1].metric,
        )
        response_for_location_two = self._weather_api.make_request(
            request=request_for_location_two
        )
        if response_for_location_two.has_error:
            raise Exception(
                f"Response for location {location_one} failed due to {response_for_location_two.error_reason}"
            )

        sample_two = WeatherAnalysisSample(
            location_name=response_for_location_two.location.name,
            date=response_for_location_two.date,
            metric=response_for_location_two.metric,
            value=response_for_location_two.value,
        )

        match settings.analysis_type:
            case WeatherAnalysisType.CHART:
                return WeatherChartAnalysisResult(samples=[sample_one, sample_two])
            case WeatherAnalysisType.TEXT:
                return WeatherTextAnalysisResult(samples=[sample_one, sample_two])
