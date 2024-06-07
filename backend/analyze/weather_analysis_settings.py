from dataclasses import dataclass
from datetime import date

from shared.weather_metric_enum import WeatherMetricEnum


@dataclass
class WeatherAnalysisSettings:
    locations: list[str]
    metrics: list[WeatherMetricEnum]
    date: date
