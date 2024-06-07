from dataclasses import dataclass


@dataclass
class WeatherAnalysisData:
    location_name: str
    value: float
    has_error: bool
    error_reason: str
