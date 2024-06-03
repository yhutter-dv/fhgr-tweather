from datetime import date

from analysis_settings.weather_analysis_config import WeatherAnalysisConfig
from analysis_settings.weather_analysis_settings import WeatherAnalysisSettings
from analysis_settings.weather_analysis_type import WeatherAnalysisType
from analysis_settings.weather_location import WeatherLocation
from analysis_settings.weather_metric import WeatherMetric
from analyze.weather_analyzer import WeatherAnalyzer
from data.weather_api import WeatherApi

if __name__ == "__main__":
    api = WeatherApi()
    analyzer = WeatherAnalyzer(weather_api=api)

    try:
        metric = WeatherMetric.TEMPERATURE
        configs = [
            WeatherAnalysisConfig(
                location=WeatherLocation(
                    name="Buchs SG",
                    postal_code=9470,
                    longitude=9.4709,
                    latitude=47.1655,
                ),
                metric=metric,
                date=date.today(),
            ),
            WeatherAnalysisConfig(
                location=WeatherLocation(
                    name="Chur", postal_code=7000, longitude=9.533, latitude=46.859
                ),
                metric=metric,
                date=date.today(),
            ),
        ]

        settings = WeatherAnalysisSettings(
            configs=configs, analysis_type=WeatherAnalysisType.CHART
        )
        chart_result = analyzer.analyze(settings)
        print(f"Got Anaylze result for Chart {chart_result}")

        settings = WeatherAnalysisSettings(
            configs=configs, analysis_type=WeatherAnalysisType.TEXT
        )
        text_result = analyzer.analyze(settings)
        print(f"Got Analize result for Text {text_result}")
    except Exception as ex:
        print(f"Failed to analyze due to {ex}")
