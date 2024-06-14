from datetime import date, timedelta

from location.weather_location import WeatherLocation
from shared.weather_metric_enum import WeatherMetricEnum
from data.weather_api import WeatherApi
from data.weather_data_request import WeatherDataRequest

if __name__ == "__main__":
    try:
        api = WeatherApi()

        # Location is set to Chur
        location = WeatherLocation(
            name="Chur", latitude=46.8590, longitude=9.533, postal_code=7000
        )
        print(f"Making API Request for location {location}")

        # Comment out to try different dates:
        request_date = date.today() - timedelta(days=4)
        # request_date = date.today() + timedelta(days=9)
        # request_date = date.today()

        # Make a request for temperature, rain and snowfall.
        request = WeatherDataRequest(
            location=location,
            date=request_date,
            metrics=[
                WeatherMetricEnum(WeatherMetricEnum.TEMPERATURE),
                WeatherMetricEnum(WeatherMetricEnum.RAIN),
                WeatherMetricEnum(WeatherMetricEnum.SNOWFALL),
            ],
        )
        respone = api.make_request(request)
        print(f"Got Response for API Request: {respone}")
    except Exception as ex:
        print(f"Failed to make API Request because of {ex}")
