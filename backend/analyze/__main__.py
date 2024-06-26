from datetime import date

from analyze.weather_analysis_settings import WeatherAnalysisSettings
from shared.weather_metric_enum import WeatherMetricEnum
from analyze.weather_analyzer import WeatherAnalyzer

if __name__ == "__main__":
    try:
        # Create an instance of the Weather Analyzer and make a request for Chur and Buchs.
        # We want to compare todays temperature and amount of rain.
        analyzer = WeatherAnalyzer()
        analysis_settings = WeatherAnalysisSettings(
            locations=["Chur", "Buchs SG"],
            metrics=[
                WeatherMetricEnum(WeatherMetricEnum.TEMPERATURE),
                WeatherMetricEnum(WeatherMetricEnum.RAIN),
            ],
            date=date.today(),
        )
        result = analyzer.analyze(analysis_settings)
        print(f"Got the following result {result}")
    except Exception as ex:
        print(f"Failed to analyze due to {ex}")
