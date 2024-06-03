import os
import sys
import json
from datetime import date
from analyze.weather_analysis_settings import WeatherAnalysisSettings
from location.weather_location import WeatherLocation
from location.weather_location_repository import WeatherLocationRepository
from shared.weather_metric import WeatherMetric


if __name__ == "__main__":
    try:
        repository = WeatherLocationRepository()

        # Search for a specific location
        location_name = "Chur"
        location = repository.find_location_by_name("Chur")
        print(f"Found the following Location for {location_name}")
        print(location)
    except Exception as ex:
        print(f"Failed to get location because of {ex}")
