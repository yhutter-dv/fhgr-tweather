from dataclasses import dataclass
import datetime
from location.weather_location import WeatherLocation
from shared.weather_metric import WeatherMetric


@dataclass
class WeatherDataRequest:
    location: WeatherLocation
    date: datetime.date
    metric: WeatherMetric
