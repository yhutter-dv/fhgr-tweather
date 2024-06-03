from location.weather_location import WeatherLocation
import json


class WeatherLocationRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._weather_locations: dict[str, WeatherLocation] = {}
        self.init_locations_from_file("location/cities.json")

    def init_locations_from_file(self, file_path: str) -> None:
        with open(file_path, "r", encoding="utf-8") as f:
            cities = json.load(f)

        for city in cities:
            name = city["name"]
            weather_location = WeatherLocation(
                name=name,
                postal_code=city["postal_code"],
                longitude=city["longitude"],
                latitude=city["latitude"],
            )
            self.add_location(weather_location)

    def remove_location(self, location: WeatherLocation) -> None:
        key = location.name
        del self._weather_locations[key]

    def add_location(self, location: WeatherLocation) -> None:
        key = location.name
        self._weather_locations[key] = location

    def get_locations(self) -> list[WeatherLocation]:
        return list(self._weather_locations.values())
    def get_location_names(self) -> list[str]:
        return list(self._weather_locations.keys())

    def clear_locations(self) -> None:
        self._weather_locations = {}

    def find_location_by_name(self, location_name: str) -> WeatherLocation | None:
        return self._weather_locations.get(location_name, None)

    def find_locations_by_name(self, location_name: str) -> list[WeatherLocation]:
        found_results = []
        for key, value in self._weather_locations.items():
            normalized_location_name = location_name.lower().strip()
            normalized_key = key.lower().strip()
            if normalized_location_name in normalized_key:
                found_results.append(value)
        return found_results
