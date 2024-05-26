from analyze.weather_analysis_result import WeatherAnalysisResult
from analyze.weather_analysis_sample import WeatherAnalysisSample
from math import fabs


class WeatherTextAnalysisResult(WeatherAnalysisResult):
    def __init__(self, samples: list[WeatherAnalysisSample]) -> None:
        super().__init__(samples=samples)
        self._text = self._construct_text()

    def __repr__(self) -> str:
        return f"WeatherTextAnalysisResult( text: {self.text}, sample_one: {self._sample_one}, sample_two: {self._sample_two}) "

    @property
    def text(self):
        return self._text

    def _construct_text(self) -> str:
        difference = fabs(self._sample_one.value - self._sample_two.value)
        return f"{self._sample_one.location_name} has a {self._metric} of {self._sample_one.value} whereas {self._sample_two.location_name} has a {self._metric} of {self._sample_two.value}. The difference between them is {difference}"
