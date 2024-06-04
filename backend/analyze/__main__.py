from datetime import date

from analyze.weather_analysis_settings import WeatherAnalysisSettings
from location.weather_location import WeatherLocation
from shared.weather_metric_enum import WeatherMetricEnum
from analyze.weather_analyzer import WeatherAnalyzer
from data.weather_api import WeatherApi

if __name__ == "__main__":
    try:
        analyzer = WeatherAnalyzer()
        analysis_settings = WeatherAnalysisSettings(
            locations=["Chur", "Buchs SG"],
            metrics=[WeatherMetricEnum.TEMPERATURE, WeatherMetricEnum.RAIN],
            date=date.today())
        result = analyzer.analyze(analysis_settings)
        print(f"Got the following result {result}")
    except Exception as ex:
        print(f"Failed to analyze due to {ex}")
