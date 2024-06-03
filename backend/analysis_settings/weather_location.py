from dataclasses import dataclass



@dataclass
class WeatherLocation:
    name: str
    postal_code: int
    longitude: float
    latitude: float
