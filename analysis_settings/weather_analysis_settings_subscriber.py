from analysis_settings.weather_analysis_settings import WeatherAnalysisSettings


class WeatherAnalysisSettingsSubscriber:
    def on_settings_changed(self, settings: WeatherAnalysisSettings):
        pass
