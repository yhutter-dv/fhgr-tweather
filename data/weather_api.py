from data.weather_data_request import WeatherDataRequest
import pandas as pd
from datetime import datetime


class WeatherApi:
    def __init__(self):
        pass

    def make_request(self, request: WeatherDataRequest) -> dict | None:
        city = request.location.name

        # TODO use longitude and latitude from location
        city_url = (
            "https://geocoding-api.open-meteo.com/v1/search?name={0}&count=1".format(
                city
            )
        )

        try:
            city_answer = pd.read_json(city_url)["results"][0]
        except Exception as ex:
            print(f"No city found with name {city}: Error {ex}")
            return None

        lat = round(city_answer["latitude"], 2)
        lon = round(city_answer["longitude"], 2)

        date = request.date

        metric = request.metric

        # Today
        if date == datetime.today().date():
            weather_url = "https://api.open-meteo.com/v1/forecast?latitude={0}&longitude={1}&current={2}".format(
                lat, lon, metric
            )
            weather_answer = pd.read_json(weather_url)["current"]
            del weather_answer["interval"]

        # Future
        elif date > datetime.today().date():
            weather_url = "https://api.open-meteo.com/v1/forecast?latitude={0}&longitude={1}&hourly={2}".format(
                lat, lon, metric
            )
            weather_answer = self.unpackHourly(
                pd.read_json(weather_url)["hourly"], date
            )
        # Historical
        else:
            start, stop = date, date
            weather_url = "https://archive-api.open-meteo.com/v1/era5?latitude={0}&longitude={1}&start_date={2}&end_date={3}&hourly={4}".format(
                lat, lon, start, stop, metric
            )
            weather_answer = unpackHourly(pd.read_json(weather_url)["hourly"], date)

        result = weather_answer.to_json(orient="columns")
        return result

    def unpackHourly(self, df_hours: pd.DataFrame, date: datetime) -> pd.DataFrame:
        mytime = datetime.strptime("1200", "%H%M").time()
        fulldate = datetime.combine(date, mytime).strftime("%Y-%m-%dT%H:%M")

        index = df_hours["time"].index(fulldate)
        for key in df_hours.keys():
            df_hours[key] = df_hours[key][index]

        return df_hours
