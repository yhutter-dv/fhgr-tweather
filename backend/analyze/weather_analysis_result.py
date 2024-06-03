
from dataclasses import dataclass
from datetime import date
from location.weather_location import WeatherLocation
from shared.weather_metric import WeatherMetric
from data.weather_data_response import WeatherDataResponse

@dataclass
class WeatherAnalysisResult:
    metric: WeatherMetric
    # TODO: Question if the same class should be used here or we should use another class
    result: list[WeatherDataResponse]
