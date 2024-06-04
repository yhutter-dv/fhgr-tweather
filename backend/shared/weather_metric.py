from dataclasses import dataclass
from shared.weather_metric_enum import WeatherMetricEnum

@dataclass
class WeatherMetric:
    identifier: WeatherMetricEnum
    title: str
    description: str
