from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from analyze.weather_analysis_result import WeatherAnalysisResult
from analyze.weather_analysis_settings import WeatherAnalysisSettings
from location.weather_location_repository import WeatherLocationRepository
from analyze.weather_analyzer import WeatherAnalyzer
from shared.weather_metric import WeatherMetric
from shared.weather_metric_enum import WeatherMetricEnum

# Create instances of needed classes
weather_location_repository = WeatherLocationRepository()
weather_analyzer = WeatherAnalyzer()
metric_enums = [
    WeatherMetricEnum(WeatherMetricEnum.TEMPERATURE),
    WeatherMetricEnum(WeatherMetricEnum.HUMIDTY),
    WeatherMetricEnum(WeatherMetricEnum.SNOWFALL),
    WeatherMetricEnum(WeatherMetricEnum.RAIN),
]
metrics = [
    WeatherMetric(
        identifier=metric,
        title=metric.title(),
        description=metric.description(),
    )
    for metric in metric_enums
]

app = FastAPI()


@app.post("/weather_analyze")
def weather_analyze(settings: WeatherAnalysisSettings) -> list[WeatherAnalysisResult]:
    """Returns a list of Analysis Results according ot the Settings.

    One AnalysisResult per Metric is returned.
    """
    try:
        return weather_analyzer.analyze(settings=settings)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")


@app.get("/weather_locations")
def weather_locations() -> list[str]:
    """Returns a list of supported Locations.

    Please note that currently only locations in Switzerland are supported.
    """
    return weather_location_repository.get_location_names()


@app.get("/weather_metrics")
def weather_metrics() -> list[WeatherMetric]:
    """Returns a list of supported Weather Metrics"""
    return metrics


# Enable CORS
# It is important that this is done AFTER defining the endpoints.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
