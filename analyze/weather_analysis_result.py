from analyze.weather_analysis_sample import WeatherAnalysisSample


class WeatherAnalysisResult:
    def __init__(self, samples: list[WeatherAnalysisSample]) -> None:
        self._samples = samples
        self._sample_one = samples[0]
        self._sample_two = samples[1]
        # As we only support one metric as of now we can just pick the metric from one of the two sample as they are identical.
        self._metric = self._sample_one.metric
        self._title = self._construct_title()
        self._x_axis_label = "Date"
        self._y_axis_label = self._metric

    def _construct_title(self) -> str:
        return f"Comparing {self._metric} for {self._sample_one.location_name} and {self._sample_two.location_name}"

    @property
    def title(self):
        return self._title

    @property
    def samples(self):
        return self._samples

    @property
    def x_axis_label(self):
        return self._x_axis_label

    @property
    def y_axis_label(self):
        return self._y_axis_label
