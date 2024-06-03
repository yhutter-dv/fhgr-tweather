from dataclasses import dataclass
from datetime import date

from location.weather_location import WeatherLocation
from shared.weather_metric import WeatherMetric


@dataclass
class WeatherDataResponse:
    location: WeatherLocation
    date: date
    metric: WeatherMetric
    value: float
    has_error: bool
    error_reason: str
