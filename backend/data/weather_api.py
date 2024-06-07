from datetime import date, timedelta

import pandas as pd
from openmeteo_requests import Client
from openmeteo_sdk.WeatherApiResponse import VariablesWithTime

from shared.weather_metric_enum import WeatherMetricEnum
from data.weather_data_request import WeatherDataRequest
from data.weather_data_response import WeatherDataResponse


class WeatherApi:
    # TODO: Perhaps move these values inside a config file
    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
    HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/era5"

    # Technically up to 16 days of forecast are possible
    MAX_FORECAST_DAYS = 16

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._client = Client()

    def _create_df_from_variables_with_time(
        self, variables: VariablesWithTime, metric_keys: list[str], has_hourly=True
    ) -> pd.DataFrame:
        data: dict = {
            "date_time": pd.date_range(
                start=pd.to_datetime(variables.Time(), unit="s"),
                end=pd.to_datetime(variables.TimeEnd(), unit="s"),
                freq=pd.Timedelta(seconds=variables.Interval()),
                inclusive="left",
            ),
        }

        # Currently we can always assume that we only have one variable because we only support one metric at a time.
        for index, metric_key in enumerate(metric_keys):
            metric_variable = variables.Variables(index)
            if metric_variable is None:
                raise Exception("Could not get first variable")

            data[metric_key] = (
                metric_variable.ValuesAsNumpy()
                if has_hourly
                else metric_variable.Value()
            )

        df = pd.DataFrame(data)
        df.dropna(inplace=True)
        return df

    def _get_historical_values(
        self, request: WeatherDataRequest, metric_keys: list[str]
    ) -> list[float]:
        date_str = f"{request.date}"
        params = {
            "latitude": request.location.latitude,
            "longitude": request.location.longitude,
            "start_date": date_str,
            "end_date": date_str,
            "hourly": metric_keys,
        }
        responses = self._client.weather_api(self.FORECAST_URL, params)

        # Because we could speficy multiple location we need to specify an index for telling which location we want to have.
        response = responses[0]
        hourly = response.Hourly()
        if hourly is None:
            raise Exception(
                "No hourly data received for request make_historical_request"
            )

        df = self._create_df_from_variables_with_time(hourly, metric_keys=metric_keys)

        # Filter out the data which matches the date and return the latest one
        values_for_date = df[df["date_time"].dt.date == request.date]

        if not isinstance(values_for_date, pd.DataFrame):
            raise Exception("Expected to have pd.DataFrame but got something different")

        if values_for_date.empty:
            raise Exception(f"No data found for date '{request.date}'")

        values = [values_for_date[metric_key].iloc[-1] for metric_key in metric_keys]
        return values

    def _get_forecast_values(
        self, request: WeatherDataRequest, metric_keys: list[str]
    ) -> list[float]:
        params = {
            "latitude": request.location.latitude,
            "longitude": request.location.longitude,
            "hourly": metric_keys,
            "forecast_days": self.MAX_FORECAST_DAYS,
        }
        responses = self._client.weather_api(self.FORECAST_URL, params)

        # Because we could speficy multiple location we need to specify an index for telling which location we want to have.
        response = responses[0]
        hourly = response.Hourly()
        if hourly is None:
            raise Exception("No hourly data received for request make_forecast_request")

        df = self._create_df_from_variables_with_time(hourly, metric_keys=metric_keys)

        # Filter out the data which matches the date and return the latest one
        values_for_date = df[df["date_time"].dt.date == request.date]

        if not isinstance(values_for_date, pd.DataFrame):
            raise Exception("Expected to have pd.DataFrame but got something different")

        if values_for_date.empty:
            raise Exception(f"No data found for date '{request.date}'")

        values = [values_for_date[metric_key].iloc[-1] for metric_key in metric_keys]
        return values

    def _get_current_values(
        self, request: WeatherDataRequest, metric_keys: list[str]
    ) -> list[float]:
        params = {
            "latitude": request.location.latitude,
            "longitude": request.location.longitude,
            "current": metric_keys,
        }
        responses = self._client.weather_api(self.FORECAST_URL, params)

        # Because we could speficy multiple location we need to specify an index for telling which location we want to have.
        response = responses[0]
        current = response.Current()
        if current is None:
            raise Exception("No current data received for request make_current_request")

        df = self._create_df_from_variables_with_time(
            current, metric_keys=metric_keys, has_hourly=False
        )

        values = [df[metric_key].iloc[-1] for metric_key in metric_keys]
        return values

    def _generate_metric_key(
        self, metric: WeatherMetricEnum, altitude_in_meters: int
    ) -> str | None:
        # For supported metrics see: https://open-meteo.com/en/docs
        match metric:
            case WeatherMetricEnum.TEMPERATURE:
                return f"{metric}_{altitude_in_meters}m"
            case WeatherMetricEnum.HUMIDTY:
                return f"{metric}_{altitude_in_meters}m"
            case WeatherMetricEnum.RAIN:
                return f"{metric}"
            case WeatherMetricEnum.SNOWFALL:
                return f"{metric}"
            case _:
                return f"{metric}"

    def _ensure_forecast_date(self, forecast_date: date):
        today = date.today()
        max_forecast_date = today + timedelta(days=self.MAX_FORECAST_DAYS)
        if forecast_date > max_forecast_date:
            raise Exception(
                f"Date '{forecast_date}' is bigger then allowed forecast range, max possible date is '{max_forecast_date}'"
            )

    def make_request(self, request: WeatherDataRequest) -> WeatherDataResponse:
        try:
            metric_keys = [
                self._generate_metric_key(key, altitude_in_meters=2)
                for key in request.metrics
            ]

            # Ignore unknown metric keys
            metric_keys = [key for key in metric_keys if key is not None]

            today = date.today()
            values = []

            # Current
            if request.date == today:
                values = self._get_current_values(request, metric_keys=metric_keys)

            # Forecast
            elif request.date > today:
                self._ensure_forecast_date(request.date)
                values = self._get_forecast_values(request, metric_keys=metric_keys)
            # Historical
            else:
                values = self._get_historical_values(request, metric_keys=metric_keys)

            # Convert to float (needed because we get numpy.float type)
            values = [float(value) for value in values]

            response = WeatherDataResponse(
                location=request.location,
                metrics=request.metrics,
                date=request.date,
                values=values,
                has_error=False,
                error_reason="",
            )
            return response
        except Exception as ex:
            response = WeatherDataResponse(
                location=request.location,
                metrics=request.metrics,
                date=request.date,
                values=[],
                has_error=True,
                error_reason=f"{ex}",
            )
            return response
