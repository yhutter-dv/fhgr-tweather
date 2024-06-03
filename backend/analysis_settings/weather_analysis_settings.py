from dataclasses import dataclass

from analysis_settings.weather_analysis_config import WeatherAnalysisConfig
from analysis_settings.weather_analysis_type import WeatherAnalysisType


@dataclass
class WeatherAnalysisSettings:
    configs: list[WeatherAnalysisConfig]
    analysis_type: WeatherAnalysisType
