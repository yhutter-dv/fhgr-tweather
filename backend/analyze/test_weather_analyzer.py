import unittest
from datetime import date, timedelta

from analyze.weather_analysis_settings import WeatherAnalysisSettings
from analyze.weather_analyzer import WeatherAnalyzer
from shared.weather_metric_enum import WeatherMetricEnum


class TestWeatherAnalyzer(unittest.TestCase):
    def setUp(self) -> None:
        self.analyzer = WeatherAnalyzer()

    def test_analyzer_invalid_location(self):
        # Only locations in Switzerland should be supported.
        analysis_settings = WeatherAnalysisSettings(
            locations=["Does totally not exist", "Buchs SG"],
            metrics=[
                WeatherMetricEnum(WeatherMetricEnum.TEMPERATURE),
                WeatherMetricEnum(WeatherMetricEnum.RAIN),
            ],
            date=date.today(),
        )
        analysis_result = self.analyzer.analyze(analysis_settings)

        # We expect two results (one per Weather Metric, e.g one for Temperature and one for Rain)
        self.assertTrue(2, len(analysis_result))

        # For each metric we expect only one location (the Location which is valid which should be Buchs SG)

        # First Metric (e.g Temperature)
        self.assertTrue(1, len(analysis_result[0].results))
        self.assertEqual("Buchs SG", analysis_result[0].results[0].location_name)

        # Second Metric (e.g Rain)
        self.assertTrue(1, len(analysis_result[1].results))
        self.assertEqual("Buchs SG", analysis_result[1].results[0].location_name)

    def test_analyzer_invalid_date(self):
        # Set date to a year in the past which is not valid
        analysis_settings = WeatherAnalysisSettings(
            locations=["Chur", "Buchs SG"],
            metrics=[
                WeatherMetricEnum(WeatherMetricEnum.TEMPERATURE),
                WeatherMetricEnum(WeatherMetricEnum.RAIN),
            ],
            date=date.today() - timedelta(days=365),
        )
        analysis_result = self.analyzer.analyze(analysis_settings)

        # We expect two results (one per Weather Metric, e.g one for Temperature and one for Rain)
        self.assertTrue(2, len(analysis_result))

        # First Metric, e.g. Temperature
        # Both results (one per Location) should have an error reason set (that the date is to far in the past)
        self.assertEqual("Chur", analysis_result[0].results[0].location_name)
        self.assertTrue(analysis_result[0].results[0].has_error)
        self.assertIsNotNone(analysis_result[0].results[0].error_reason)

        self.assertEqual("Buchs SG", analysis_result[0].results[1].location_name)
        self.assertTrue(analysis_result[0].results[1].has_error)
        self.assertIsNotNone(analysis_result[0].results[1].error_reason)

        # Second Metric, e.g. Rain
        # Both results (one per Location) should have an error reason set (that the date is to far in the past)
        self.assertEqual("Chur", analysis_result[1].results[0].location_name)
        self.assertTrue(analysis_result[1].results[0].has_error)
        self.assertIsNotNone(analysis_result[1].results[0].error_reason)

        self.assertEqual("Buchs SG", analysis_result[1].results[1].location_name)
        self.assertTrue(analysis_result[1].results[1].has_error)
        self.assertIsNotNone(analysis_result[1].results[1].error_reason)

    def test_analyzer_valid(self):
        analysis_settings = WeatherAnalysisSettings(
            locations=["Chur", "Buchs SG"],
            metrics=[
                WeatherMetricEnum(WeatherMetricEnum.TEMPERATURE),
                WeatherMetricEnum(WeatherMetricEnum.RAIN),
            ],
            date=date.today(),
        )
        analysis_result = self.analyzer.analyze(analysis_settings)

        # We expect two results (one per Weather Metric, e.g one for Temperature and one for Rain)
        self.assertTrue(2, len(analysis_result))

        # Validate Temperature
        self.assertEqual(WeatherMetricEnum.TEMPERATURE, analysis_result[0].metric)

        # We expect two results (one per Location, e.g. Chur and Buchs)
        self.assertTrue(2, len(analysis_result[0].results))

        # Validate location names
        self.assertTrue("Chur", analysis_result[0].results[0].location_name)
        self.assertTrue("Buchs SG", analysis_result[0].results[1].location_name)

        # Validate value
        self.assertIsNotNone(analysis_result[0].results[0].value)

        # Validate Rain
        self.assertEqual(WeatherMetricEnum.RAIN, analysis_result[1].metric)

        # We expect two results (one per Location, e.g. Chur and Buchs)
        self.assertTrue(2, len(analysis_result[1].results))

        # Validate location names
        self.assertTrue("Chur", analysis_result[1].results[0].location_name)
        self.assertTrue("Buchs SG", analysis_result[1].results[1].location_name)

        # Validate value
        self.assertIsNotNone(analysis_result[1].results[0].value)
        self.assertIsNotNone(analysis_result[1].results[1].value)
