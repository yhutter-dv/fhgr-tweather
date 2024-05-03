from dataclasses import dataclass

from shared.date_time_range import DateTimeRange
from analysis_settings.weather_location import WeatherLocation
from analysis_settings.weather_metric import WeatherMetric


@dataclass
class WeatherAnalysisSample:
    location: WeatherLocation
    metric: WeatherMetric
    date_time_range: DateTimeRange
