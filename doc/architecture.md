# Architecture
The architecture is split into different parts. First the differente Context (building blocks) of the Application are explained. Afterwards it is described how these builidng blocks interact with each other.

## Context
The whole applications is split up into `different context`. Each context serves a specific puprose. Communication between contexts is done via the `Aggregate Root` Object. Below you can find a short explanation for each context and its purpose

|Context|Description|
|--|----|
|Analysis Settings Context|This context holds all objects related to settings needed for an Analysis|
|Analyze Context|This context holds all objects responsible for actually doing the analysis|
|Data Context|This context holds all objects responsible for retrieving and caching the actual data|
|Dashboard Context|This context holds all objects responsible for displaying the actual dashboard|

```mermaid
---
title: Analysis Settings Context
---
classDiagram

    AnalysisSettingsManager *-- WeatherAnalysisSettings
    AnalysisSettingsManager *-- WeatherLocationRepository
    AnalysisSettingsManager .. AnalysisSettingsSubscriber
    WeatherAnalysisSettings *-- WeatherAnalysisType
    WeatherAnalysisSettings *-- WeatherAnalysisConfig
    WeatherAnalysisConfig *-- WeatherMetric
    WeatherAnalysisConfig *-- WeatherLocation

    class AnalysisSettingsSubscriber {
        <<interface>>
        + on_settings_changed(WeatherAnalysisSettings settings)
    }

    class WeatherMetric {
        <<enumeration>>
        RAIN,
        TEMPERATURE,
        HUMIDTY
    }

    class WeatherAnalysisType {
        <<enumeration>>
        TEXT,
        CHART
    }

    class WeatherLocationRepository {
        - WeatherLocation[] _weather_locations
        + remove_location(WeatherLocation location)
        + add_location(WeatherLocation location)
        + clear_locations()
        + WeatherLocation[] find_locations_by_name(String location_name)
        + WeatherLocation find_location_by_name(String location_name)
    }

    note for AnalysisSettingsManager "Root Aggregate"
    class AnalysisSettingsManager {
        - WeatherAnalysisSettings _settings
        - AnalysisSettingsSubscriber[] _subscribers
        - WeatherLocationRepository _weather_location_repository
        - notify_subscribers()
        + subscribe(AnalysisSettingsSubscriber subscriber)
        + unsubscribe(AnalysisSettingsSubscriber subscriber)
        + update_settings(String location_name_one, String location_name_two, WeatherMetric metric, WeatherAnalysisType analysis_type, Date date)
    }

    class WeatherAnalysisSettings {
        - WeatherAnalysisConfig[] _configs
        - WeatherAnalysisType _analysis_type
        + WeatherAnalysisConfig[] configs
        + WeatherAnalysisType analysis_type()
    }

    class WeatherAnalysisConfig {
        - WeatherLocation _location
        - WeatherMetric _metric
        - Date _date
        + WeatherLocation location()
        + WeatherMetric metric()
        + Date date()
    }

    class WeatherLocation {
        - String _name
        - int _postal_code
        - float _longitude
        - float _latitude
        + String name()
        + int postal_code()
        + float longitude()
        + float latitude()
    }
```

```mermaid
---
title: Analyze Context
---
classDiagram

    WeatherAnalyzer *-- WeatherApi
    WeatherAnalyzer *-- WeatherAnalysisResult
    WeatherAnalysisResult *-- WeatherAnalysisSample
    WeatherChartAnalysisResult --|> WeatherAnalysisResult
    WeatherTextAnalysisResult --|> WeatherAnalysisResult

    note for WeatherApi "Comes from Data Context (Root Aggregate)"
    class WeatherApi {
        
    }

    note for WeatherAnalyzer "Root Aggregate"
    class WeatherAnalyzer {
        - WeatherApi _weather_api
        + WeatherAnalysisResult analyze(WeatherAnalysisSettings settings)
    }

    class WeatherAnalysisResult {
        - WeatherAnalysisSample[] _samples
        - WeatherMetric _metric
        - String _title
        - String _x_axis_label
        - String _y_axis_label
        - String _construct_title()
        + String title()
        + WeatherAnalysisSample[] samples
        + String x_axis_label()
        + String y_axis_label()
    }

    class WeatherAnalysisSample {
        - String _location_name
        - Date _date
        - WeatherMetric _metric
        - float _value
        + String location_name()
        + Date date()
        + float value()
    }

    class WeatherChartAnalysisResult {
        
    }

    class WeatherTextAnalysisResult {
        - String _text
        + String text()
    }

```

```mermaid
---
title: Data Context
---
classDiagram

    WeatherApi *-- WeatherDataRequest
    WeatherApi *-- WeatherDataResponse

    note for WeatherApi "Root Aggregate"
    class WeatherApi {
        - float _get_historical_value(WeatherDataRequest request)
        - float _get_current_value(WeatherDataRequest request)
        - float _get_forecast_value(WeatherDataRequest request)
        + WeatherDataResponse make_request(WeatherDataRequest request) 
    }

    class WeatherDataRequest {
        - WeatherLocation _location
        - Date _date
        - WeatherMetric _metric
        + WeatherLocation location()
        + Date date()
        + WeatherMetric metric()
    }

    class WeatherDataResponse {
        - WeatherLocation _location
        - Date _date
        - float _value
        - WeatherMetric _metric
        - bool _has_error
        - String _error_reason
        + WeatherLocation location()
        + Date date()
        + WeatherMetric metric()
        + float value()
        + bool has_error()
        + String error_reason()
    }
```

```mermaid
---
title: Dashboard Context
---
classDiagram

    WeatherDashboard --|> WeatherAnalysisSettingsSubscriber
    WeatherDashboard *-- WeatherAnalysisSettingsManager
    WeatherDashboard *-- WeatherTextWidget
    WeatherDashboard *-- WeatherChartWidget
    WeatherChartWidget *-- WeatherChartData

    note for WeatherAnalysisSettingsManager "Comes from the AnalysisSettings Context"
    class WeatherAnalysisSettingsManager {

    }

    note for WeatherAnalysisSettingsSubscriber "Comes from the AnalysisSettings Context"
    class WeatherAnalysisSettingsSubscriber {

    }

    note for WeatherDashboard "Root Aggregate"
    class WeatherDashboard {
        - WeatherAnalyzer _weather_analyzer
        - WeatherAnalysisSettingsManager _settings_manager
        - WeatherAnalysisSettings _current_settings
        - WeatherTextWidget _text_widget
        - WeatherChartWidget _chart_widget
        - WeatherAnalysisSettings _settings
        - clear_widgets()
        + on_settings_changed(WeatherAnalysisSettings settings)
        + reload()
        + String generate_share_link()
    }

    class WeatherTextWidget {
        - String _title
        - String _text
        + String title()
        + String text()
    }


    class WeatherChartWidget {
        - String _title
        - WeatherChartData _data
        + String title()
        + WeatherChartData data()
        + bool save_as_image(String path)
    }

    class WeatherChartData {
        - Tuple<Date, float>[] _data
        + Tuple<Date, float>[] data()
    }
```

## Context Mapping

```mermaid
---
title: Context Mapping
---
flowchart BT
    AnalyzeContext --> DataContext
    DashboardContext --> AnalyzeContext
    DashboardContext --> AnalysisSettingsContext
```

