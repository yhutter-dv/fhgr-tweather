from dataclasses import dataclass
from datetime import date

from analysis_settings.weather_location import WeatherLocation
from analysis_settings.weather_metric import WeatherMetric


@dataclass
class WeatherAnalysisSample:
    location: WeatherLocation
    metric: WeatherMetric
    date: date
