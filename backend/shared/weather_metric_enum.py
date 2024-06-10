from enum import StrEnum


class WeatherMetricEnum(StrEnum):
    RAIN = "rain"
    TEMPERATURE = "temperature"
    HUMIDTY = "relative_humidity"
    SNOWFALL = "snowfall"

    def identifier(self) -> str:
        match self:
            case WeatherMetricEnum.TEMPERATURE:
                return "temperature"
            case WeatherMetricEnum.RAIN:
                return "rain"
            case WeatherMetricEnum.HUMIDTY:
                return "relative_humidity"
            case WeatherMetricEnum.SNOWFALL:
                return "snowfall"
            case _:
                return "unknown"

    def title(self) -> str:
        match self:
            case WeatherMetricEnum.TEMPERATURE:
                return "Temperature"
            case WeatherMetricEnum.RAIN:
                return "Rain"
            case WeatherMetricEnum.HUMIDTY:
                return "Humidity"
            case WeatherMetricEnum.SNOWFALL:
                return "Snowfall"
            case _:
                return "Unknown"

    def description(self) -> str:
        match self:
            case WeatherMetricEnum.TEMPERATURE:
                return "Temperature in °C"
            case WeatherMetricEnum.RAIN:
                return "Rain"
            case WeatherMetricEnum.HUMIDTY:
                return "Humidity"
            case WeatherMetricEnum.SNOWFALL:
                return "Snowfall"
            case _:
                return "Unknown"

    def friendly_name(self) -> str:
        match self:
            case WeatherMetricEnum.TEMPERATURE:
                return "Temperature"
            case WeatherMetricEnum.RAIN:
                return "Rain"
            case WeatherMetricEnum.HUMIDTY:
                return "Humidity"
            case WeatherMetricEnum.SNOWFALL:
                return "Snowfall"
            case _:
                return "Unknown"
