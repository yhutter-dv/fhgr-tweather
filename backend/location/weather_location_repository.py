from location.weather_location import WeatherLocation
import json


class WeatherLocationRepository:
    """This class is responsible for searching and retrieving Weather Locations.

    This class is implemented as a Singleton.
    The Open-Meteo API works with longitude and latitude values.
    This class allows searching for locations with a name such as 'Chur' and receive a matching Object with the appropriate longitude and latitude values.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._weather_locations: dict[str, WeatherLocation] = {}
        # Load the locations from file
        self._init_locations_from_file()

    def _init_locations_from_file(self) -> None:
        """Initializes all locations from a predefined JSON file."""

        file_path = "location/cities.json"

        with open(file_path, "r", encoding="utf-8") as f:
            cities = json.load(f)

        # Iterate through the entries and construct a WeatherLocation object.
        for city in cities:
            name = city["name"]
            weather_location = WeatherLocation(
                name=name,
                postal_code=city["postal_code"],
                longitude=city["longitude"],
                latitude=city["latitude"],
            )
            self.add_location(weather_location)

    def add_location(self, location: WeatherLocation) -> None:
        key = location.name
        self._weather_locations[key] = location

    def get_locations(self) -> list[WeatherLocation]:
        """Returns all Weather Locations."""
        return list(self._weather_locations.values())

    def get_location_names(self) -> list[str]:
        """Returns all Location Names."""
        return list(self._weather_locations.keys())

    def find_location_by_name(self, location_name: str) -> WeatherLocation | None:
        """Returns a Location exactly matching a given Location Name (e.g 'Buchs SG')"""

        return self._weather_locations.get(location_name, None)

    def find_locations_by_name(self, location_name: str) -> list[WeatherLocation]:
        """Returns all locations containing part of a Location Name (e.g 'Chu')"""
        found_results = []
        for key, value in self._weather_locations.items():
            normalized_location_name = location_name.lower().strip()
            normalized_key = key.lower().strip()
            if normalized_location_name in normalized_key:
                found_results.append(value)
        return found_results
