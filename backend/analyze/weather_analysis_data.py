from dataclasses import dataclass


@dataclass
class WeatherAnalysisData:
    location_name: str
    value: float | None
    has_error: bool
    error_reason: str
