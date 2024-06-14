import unittest
from datetime import date, timedelta
from data.weather_api import WeatherApi
from data.weather_data_request import WeatherDataRequest
from location.weather_location import WeatherLocation
from shared.weather_metric_enum import WeatherMetricEnum


class TestWeatherApi(unittest.TestCase):
    def setUp(self) -> None:
        self.api = WeatherApi()

    def test_weather_api_valid_request(self):
        request_location = WeatherLocation(
            name="Buchs SG",
            postal_code=9470,
            latitude=47.16516222572188,
            longitude=9.475764283520503,
        )
        request_date = date.today()

        request_metrics = [WeatherMetricEnum(WeatherMetricEnum.RAIN)]

        request = WeatherDataRequest(
            location=request_location, date=request_date, metrics=request_metrics
        )
        response = self.api.make_request(request)
        self.assertIsNotNone(response)
        self.assertFalse(response.has_error)
        self.assertEqual("", response.error_reason)
        self.assertTrue(len(response.values) > 0)
        self.assertIsNotNone(response.values[0])

    def test_weather_api_invalid_request_date_in_past(self):
        request_location = WeatherLocation(
            name="Buchs SG",
            postal_code=9470,
            latitude=47.16516222572188,
            longitude=9.475764283520503,
        )

        # Request should be invalid because the date is to far in the past.
        request_date = date.today() - timedelta(days=365)

        request_metrics = [WeatherMetricEnum(WeatherMetricEnum.RAIN)]

        request = WeatherDataRequest(
            location=request_location, date=request_date, metrics=request_metrics
        )
        response = self.api.make_request(request)
        self.assertIsNotNone(response)
        self.assertTrue(response.has_error)
        self.assertNotEqual("", response.error_reason)
        self.assertTrue(len(response.values) == 0)

    def test_weather_api_invalid_request_date_in_future(self):
        request_location = WeatherLocation(
            name="Buchs SG",
            postal_code=9470,
            latitude=47.16516222572188,
            longitude=9.475764283520503,
        )

        # Request should be invalid because the date is to far in the future.
        request_date = date.today() + timedelta(days=365)

        request_metrics = [WeatherMetricEnum(WeatherMetricEnum.RAIN)]

        request = WeatherDataRequest(
            location=request_location, date=request_date, metrics=request_metrics
        )
        response = self.api.make_request(request)
        self.assertIsNotNone(response)
        self.assertTrue(response.has_error)
        self.assertNotEqual("", response.error_reason)
        self.assertTrue(len(response.values) == 0)
