from datetime import date, timedelta

import pandas as pd
from openmeteo_requests import Client
from openmeteo_sdk.WeatherApiResponse import VariablesWithTime

from shared.weather_metric_enum import WeatherMetricEnum
from data.weather_data_request import WeatherDataRequest
from data.weather_data_response import WeatherDataResponse


class WeatherApi:
    """The Weather API is responsible for retrieving the raw data from 'Open-Meteo'.

    This class is implemented as a singleton.
    """

    # We could move these values inside a config file
    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
    HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/era5"

    # Technically up to 16 days of forecast are possible
    # See https://open-meteo.com/en/docs
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
        """Helper method to construct DataFrame according to the given metric keys.

        The open-meteo Library makes it somewhat inconvenient to work with Variables.
        This method returns a pandas DataFrame with a date_time column as well as the metric keys as separate columns.
        """

        # Construct the date_time column
        data: dict = {
            "date_time": pd.date_range(
                start=pd.to_datetime(variables.Time(), unit="s"),
                end=pd.to_datetime(variables.TimeEnd(), unit="s"),
                freq=pd.Timedelta(seconds=variables.Interval()),
                inclusive="left",
            ),
        }

        # Extract the values for a given metric
        for index, metric_key in enumerate(metric_keys):
            metric_variable = variables.Variables(index)
            if metric_variable is None:
                raise Exception("Could not get first variable")

            data[metric_key] = (
                metric_variable.ValuesAsNumpy()
                if has_hourly
                else metric_variable.Value()
            )

        # Construct the DataFrame
        df = pd.DataFrame(data)

        # Drop any missing values
        df.dropna(inplace=True)
        return df

    def _get_historical_values(
        self, request: WeatherDataRequest, metric_keys: list[str]
    ) -> list[float]:
        """Gets historical values for the given metric keys."""

        date_str = f"{request.date}"
        params = {
            "latitude": request.location.latitude,
            "longitude": request.location.longitude,
            "start_date": date_str,
            "end_date": date_str,
            "hourly": metric_keys,
        }
        responses = self._client.weather_api(self.FORECAST_URL, params)

        # Get the response and check if we have any hourly data.
        response = responses[0]
        hourly = response.Hourly()
        if hourly is None:
            raise Exception("No hourly data received for Historical Request")

        df = self._create_df_from_variables_with_time(hourly, metric_keys=metric_keys)

        # Filter out the data which matches the request data
        values_for_date = df[df["date_time"].dt.date == request.date]

        if not isinstance(values_for_date, pd.DataFrame):
            raise Exception("Expected to have pd.DataFrame but got something different")

        if values_for_date.empty:
            raise Exception(f"No data found for date '{request.date}'")

        # Only take the latest value
        values = [values_for_date[metric_key].iloc[-1] for metric_key in metric_keys]
        return values

    def _get_forecast_values(
        self, request: WeatherDataRequest, metric_keys: list[str]
    ) -> list[float]:
        """Gets forecast values for the given metric keys."""

        params = {
            "latitude": request.location.latitude,
            "longitude": request.location.longitude,
            "hourly": metric_keys,
            "forecast_days": self.MAX_FORECAST_DAYS,
        }
        responses = self._client.weather_api(self.FORECAST_URL, params)

        # Get the response and check if we have any hourly data.
        response = responses[0]
        hourly = response.Hourly()
        if hourly is None:
            raise Exception("No hourly data received for Forecast request")

        df = self._create_df_from_variables_with_time(hourly, metric_keys=metric_keys)

        # Filter out the data which matches the request date
        values_for_date = df[df["date_time"].dt.date == request.date]

        if not isinstance(values_for_date, pd.DataFrame):
            raise Exception("Expected to have pd.DataFrame but got something different")

        if values_for_date.empty:
            raise Exception(f"No data found for date '{request.date}'")

        # Only take the latest value
        values = [values_for_date[metric_key].iloc[-1] for metric_key in metric_keys]
        return values

    def _get_current_values(
        self, request: WeatherDataRequest, metric_keys: list[str]
    ) -> list[float]:
        """Gets current values for the given metric keys."""
        params = {
            "latitude": request.location.latitude,
            "longitude": request.location.longitude,
            "current": metric_keys,
        }
        responses = self._client.weather_api(self.FORECAST_URL, params)

        # Get the response and check if we have any current data.
        response = responses[0]
        current = response.Current()
        if current is None:
            raise Exception("No current data received for Current Request")

        df = self._create_df_from_variables_with_time(
            current, metric_keys=metric_keys, has_hourly=False
        )

        # Extract the latest values
        values = [df[metric_key].iloc[-1] for metric_key in metric_keys]
        return values

    def _generate_metric_key(
        self, metric: WeatherMetricEnum, altitude_in_meters: int
    ) -> str | None:
        """Generates a metric key given a specific metric.

        This key is used for the open-meteo requests
        For supported metrics see: https://open-meteo.com/en/docs
        """

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
        """Ensures that the forecast date is not beyond the maximum supported forecast date."""

        today = date.today()
        max_forecast_date = today + timedelta(days=self.MAX_FORECAST_DAYS)
        if forecast_date > max_forecast_date:
            raise Exception(
                f"Date '{forecast_date}' is bigger then allowed forecast range, max possible date is '{max_forecast_date}'"
            )

    def make_request(self, request: WeatherDataRequest) -> WeatherDataResponse:
        """Makes a reuqest to the open-meteo API.

        If any errors happen the 'has_error' and 'error_reason' fields are set.
        """
        try:
            # Generate the metric keys which are needed for the Open-Meteo API.
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

            # Construct a valid response
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
            # In case of any error construct an invalid response and set the error reason etc.
            response = WeatherDataResponse(
                location=request.location,
                metrics=request.metrics,
                date=request.date,
                values=[],
                has_error=True,
                error_reason=f"{ex}",
            )
            return response
