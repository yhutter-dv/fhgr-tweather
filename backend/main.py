from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analyze.weather_analysis_result import WeatherAnalysisResult
from analyze.weather_analysis_settings import WeatherAnalysisSettings
from location.weather_location_repository import WeatherLocationRepository
from analyze.weather_analyzer import WeatherAnalyzer

weather_location_repository = WeatherLocationRepository()
weather_analyzer = WeatherAnalyzer()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/weather_analyze")
def weather_analyze(settings: WeatherAnalysisSettings) -> list[WeatherAnalysisResult]:
    return weather_analyzer.analyze(settings=settings)

@app.get("/weather_locations")
def weather_locations() -> list[str]:
    return weather_location_repository.get_location_names()
