from location.weather_location_repository import WeatherLocationRepository


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
