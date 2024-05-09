from datetime import date, timedelta

from analysis_settings.weather_location import WeatherLocation
from analysis_settings.weather_metric import WeatherMetric
from data.weather_api import WeatherApi
from data.weather_data_request import WeatherDataRequest

if __name__ == "__main__":
    api = WeatherApi()
    location = WeatherLocation(
        name="Chur", latitude=46.8590, longitude=9.533, postal_code=7000
    )
    print(f"Making API Request for location {location}")

    # Comment out to try different dates:
    request_date = date.today() - timedelta(days=4)
    # request_date = date.today() + timedelta(days=9)
    # request_date = date.today()

    request = WeatherDataRequest(
        location=location, date=request_date, metric=WeatherMetric.TEMPERATURE
    )
    respone = api.make_request(request)
    print(f"Got Response for API Request: {respone}")
