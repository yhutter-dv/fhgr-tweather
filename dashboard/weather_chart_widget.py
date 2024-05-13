from analyze.weather_chart_analysis_result import WeatherChartAnalysisResult
from dashboard.weather_chart_data import WeatherChartData


class WeatherChartWidget:
    def __init__(self, chart_analysis_result: WeatherChartAnalysisResult) -> None:
        self._data = self._create_data_from_analysis_result(
            chart_analysis_result=chart_analysis_result
        )
        self._title = chart_analysis_result.title

    def __repr__(self) -> str:
        return f"WeatherChartWidget(title: {self._title}, data: {self._data})"

    def _create_data_from_analysis_result(
        self, chart_analysis_result: WeatherChartAnalysisResult
    ) -> WeatherChartData:
        return WeatherChartData(
            [(x.date, x.value) for x in chart_analysis_result.samples]
        )

    @property
    def title(self):
        return self._title

    @property
    def data(self):
        return self._data

    def save_as_image(file_path: str) -> bool:
        # TODO: We need to discuss if we want to save the image from the client side rather then on the server.
        # Depending on the Chart Library we use we would not need to implement this ourselves.
        return True
