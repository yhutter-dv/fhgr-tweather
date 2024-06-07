from enum import StrEnum


class WeatherMetricEnum(StrEnum):
    RAIN = "rain"
    TEMPERATURE = "temperature"
    HUMIDTY = "relative_humidity"
    SNOWFALL = "snowfall"

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
