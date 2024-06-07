from datetime import date
from dataclasses import dataclass
from analyze.weather_analysis_data import WeatherAnalysisData
from shared.weather_metric_enum import WeatherMetricEnum


@dataclass
class WeatherAnalysisResult:
    metric: WeatherMetricEnum
    metric_friendly_name: str
    date: date
    results: list[WeatherAnalysisData]
