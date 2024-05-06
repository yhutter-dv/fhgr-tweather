from datetime import datetime
from analysis_settings.weather_location import WeatherLocation
from analysis_settings.weather_metric import WeatherMetric
from data.weather_api import WeatherApi
from data.weather_data_request import WeatherDataRequest


if __name__ == "__main__":
    api = WeatherApi()
    location = WeatherLocation(
        name="Chur", longitude=0.0, latitude=0.0, postal_code=7000
    )
    date = datetime.now()
    metric = WeatherMetric.RAIN
    request = WeatherDataRequest(location=location, date=date, metric=metric)
    try:
        result = api.make_request(request)
        print(result)
    except Exception as ex:
        print(f"An error occurred in make the request: {ex}")

