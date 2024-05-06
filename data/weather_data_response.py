from dataclasses import dataclass
from datetime import datetime

from analysis_settings.weather_location import WeatherLocation
from analysis_settings.weather_metric import WeatherMetric


@dataclass
class WeatherDataResponse:
    location: WeatherLocation
    date: datetime
    metric: WeatherMetric
    value: float
