from dataclasses import dataclass

from analysis_settings.weather_analysis_sample import WeatherAnalysisSample
from analysis_settings.weather_analysis_type import WeatherAnalysisType


@dataclass
class WeatherAnalysisSettings:
    sample_one: WeatherAnalysisSample
    sample_two: WeatherAnalysisSample
    analysis_type: WeatherAnalysisType
