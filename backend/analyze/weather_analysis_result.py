
from dataclasses import dataclass
from datetime import date
from location.weather_location import WeatherLocation
from shared.weather_metric_enum import WeatherMetricEnum
from data.weather_data_response import WeatherDataResponse

@dataclass
class WeatherAnalysisResult:
    metric: WeatherMetricEnum
    # TODO: Question if the same class should be used here or we should use another class
    result: list[WeatherDataResponse]
