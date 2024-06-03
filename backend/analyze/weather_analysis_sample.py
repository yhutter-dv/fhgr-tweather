from datetime import date
from dataclasses import dataclass
from analysis_settings.weather_metric import WeatherMetric


@dataclass
class WeatherAnalysisSample:
    location_name: str
    date: date
    metric: WeatherMetric
    value: float
