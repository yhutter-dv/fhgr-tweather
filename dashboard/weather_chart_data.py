from dataclasses import dataclass
from datetime import date


@dataclass
class WeatherChartData:
    data: list[tuple[date, float]]
