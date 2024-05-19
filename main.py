from fastapi import FastAPI
from analysis_settings.weather_location import WeatherLocation
import json


def init_weather_location_repostitory_from_file(
    file_path: str,
) -> list[WeatherLocation]:

    weather_locations = []

    with open(file_path, "r", encoding="utf-8") as f:
        cities = json.load(f)

    for city in cities:
        weather_location = WeatherLocation(
            name=city["name"],
            postal_code=city["postal_code"],
            longitude=city["longitude"],
            latitude=city["latitude"],
        )
        weather_locations.append(weather_location)
    return weather_locations

app = FastAPI()
weather_locations = init_weather_location_repostitory_from_file("./cities.json")

@app.get("/weather_locations")
def get_weather_locations() -> list[WeatherLocation]:
    return weather_locations[0:10]

@app.get("/hello_world")
def get_hello_world(number_of_repeats: int) -> str:
    return "hello world"*number_of_repeats
