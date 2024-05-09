from dataclasses import dataclass
from datetime import date

from analysis_settings.weather_location import WeatherLocation
from analysis_settings.weather_metric import WeatherMetric


@dataclass
class WeatherDataResponse:
    location: WeatherLocation
    date: date
    metric: WeatherMetric
    value: float | None
    has_error: bool
    error_reason: str
