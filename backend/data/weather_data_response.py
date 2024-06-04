from dataclasses import dataclass
from datetime import date

from location.weather_location import WeatherLocation
from shared.weather_metric_enum import WeatherMetricEnum


@dataclass
class WeatherDataResponse:
    location: WeatherLocation
    date: date
    metric: WeatherMetricEnum
    value: float
    has_error: bool
    error_reason: str
