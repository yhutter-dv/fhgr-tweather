from dataclasses import dataclass
from datetime import date

@dataclass
class WeatherAnalysisSettings:
    locations: list[str]
    metrics: list[str]
    date: date
