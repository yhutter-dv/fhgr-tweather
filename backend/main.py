from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analyze.weather_analysis_result import WeatherAnalysisResult
from analyze.weather_analysis_settings import WeatherAnalysisSettings
from location.weather_location_repository import WeatherLocationRepository
from analyze.weather_analyzer import WeatherAnalyzer
from shared.weather_metric import WeatherMetric
from shared.weather_metric_enum import WeatherMetricEnum

weather_location_repository = WeatherLocationRepository()
weather_analyzer = WeatherAnalyzer()
metrics = [
    WeatherMetric(identifier=WeatherMetricEnum.TEMPERATURE, title="Temperature", description="Temperature in °C"),
    WeatherMetric(identifier=WeatherMetricEnum.RAIN, title="Rain", description="Rain"),
    WeatherMetric(identifier=WeatherMetricEnum.HUMIDTY, title="Humidity", description="Humidity"),
    WeatherMetric(identifier=WeatherMetricEnum.SNOWFALL, title="Snowfall", description="Snowfall"),
]

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

@app.get("/weather_metrics")
def weather_metrics() -> list[WeatherMetric]:
    return metrics
