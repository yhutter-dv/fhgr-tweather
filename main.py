from fastapi import FastAPI

from analysis_settings.weather_location_repository import WeatherLocationRepository

weather_location_repository = WeatherLocationRepository.init_from_file(
    "./scripts/cities.json"
)
app = FastAPI()


@app.get("/weather_locations")
def get_weather_locations() -> list[str]:
    return weather_location_repository.get_location_names()
