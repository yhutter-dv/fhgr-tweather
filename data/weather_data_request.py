from dataclasses import dataclass
import datetime
from analysis_settings.weather_location import WeatherLocation
from analysis_settings.weather_metric import WeatherMetric


@dataclass
class WeatherDataRequest:
    location: WeatherLocation
    date: datetime.datetime
    metric: WeatherMetric
