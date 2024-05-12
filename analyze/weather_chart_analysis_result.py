from analyze.weather_analysis_result import WeatherAnalysisResult
from analyze.weather_analysis_sample import WeatherAnalysisSample


class WeatherChartAnalysisResult(WeatherAnalysisResult):
    def __init__(self, samples: list[WeatherAnalysisSample]):
        super().__init__(samples=samples)

    def __repr__(self) -> str:
        return f"WeatherChartAnalysisResult( title: {self.title}, x_axis_label: {self.x_axis_label}, y_axis_label: {self.y_axis_label}, sample_one: {self._sample_one}, sample_two: {self._sample_two}) "
