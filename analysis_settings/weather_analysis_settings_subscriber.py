from abc import abstractmethod
from analysis_settings.weather_analysis_settings import WeatherAnalysisSettings


class WeatherAnalysisSettingsSubscriber:
    @abstractmethod
    def on_settings_changed(self, settings: WeatherAnalysisSettings):
        pass
