from analysis_settings.weather_analysis_settings import WeatherAnalysisSettings
from analysis_settings.weather_analysis_settings_manager import (
    WeatherAnalysisSettingsManager,
)
from analysis_settings.weather_analysis_settings_subscriber import (
    WeatherAnalysisSettingsSubscriber,
)
from analyze.weather_analyzer import WeatherAnalyzer
from analyze.weather_chart_analysis_result import WeatherChartAnalysisResult
from analyze.weather_text_analysis_result import WeatherTextAnalysisResult
from dashboard.weather_chart_widget import WeatherChartWidget
from dashboard.weather_text_widget import WeatherTextWidget


class WeatherDashboard(WeatherAnalysisSettingsSubscriber):
    def __init__(
        self, analysis_settings_manager: WeatherAnalysisSettingsManager
    ) -> None:
        self._weather_analyzer = WeatherAnalyzer()
        self._analysis_settings_manager = analysis_settings_manager
        self._current_settings = None
        self._chart_widget = None
        self._text_widget = None

        self._analysis_settings_manager.subscribe(self)

    def _clear_widgets(self):
        self._chart_widget = None
        self._text_widget = None

    def on_settings_changed(self, settings: WeatherAnalysisSettings):
        self._current_settings = settings

    def reload(self):
        if self._current_settings is None:
            print("Current Settings is not defined, will no refresh settings")
            return

        self._clear_widgets()
        analyse_result = self._weather_analyzer.analyze(self._current_settings)
        if isinstance(analyse_result, WeatherChartAnalysisResult):
            self._chart_widget = WeatherChartWidget(
                chart_analysis_result=analyse_result
            )
        elif isinstance(analyse_result, WeatherTextAnalysisResult):
            self._text_widget = WeatherTextWidget(
                text=analyse_result.text, title=analyse_result.title
            )
        else:
            raise Exception(f"Got unexpected Analysis Type {type(analyse_result)}")

    def __repr__(self) -> str:
        return f"WeatherDashboard(chart_widget: {self._chart_widget}, text_widget: {self._text_widget})"
