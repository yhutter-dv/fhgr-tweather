from datetime import date
from analysis_settings.weather_analysis_settings_manager import (
    WeatherAnalysisSettingsManager,
)
from analysis_settings.weather_analysis_type import WeatherAnalysisType
from analysis_settings.weather_location import WeatherLocation
from analysis_settings.weather_location_repository import WeatherLocationRepository
from analysis_settings.weather_metric import WeatherMetric
from dashboard.weather_dashboard import WeatherDashboard


if __name__ == "__main__":
    weather_location_repository = WeatherLocationRepository()

    # Add locations to repository (this will come from a file in the main application)
    weather_location_repository.add_location(
        WeatherLocation(
            name="Buchs SG",
            postal_code=9470,
            longitude=9.4709,
            latitude=47.1655,
        )
    )
    weather_location_repository.add_location(
        WeatherLocation(name="Chur", postal_code=7000, longitude=9.533, latitude=46.859)
    )

    settings_manager = WeatherAnalysisSettingsManager(
        location_repository=weather_location_repository
    )
    dashboard = WeatherDashboard(analysis_settings_manager=settings_manager)
    try:
        settings_manager.update_settings(
            "Chur",
            "Buchs SG",
            metric=WeatherMetric.TEMPERATURE,
            analysis_type=WeatherAnalysisType.CHART,
            date=date.today(),
        )
        dashboard.reload()
        print(f"Dashboard is reloaded and now is {dashboard}")
    except Exception as ex:
        print(f"Refreshing Dashboard failed due to {ex}")
