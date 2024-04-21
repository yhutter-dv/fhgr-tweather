# fhgr-tweather
SAD (Software Architecture and Design) Project @FHGR

## Architecture
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
    WeatherAnalysisSettings *-- WeatherAnalysisSample
    WeatherAnalysisSettings *-- WeatherAnalysisType
    WeatherAnalysisSample *-- WeatherMetric
    WeatherAnalysisSample *-- WeatherLocation

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
        - WeatherLocation[] _locations
        + WeatherLocation[] locations()
        + WeatherLocation[] find_locations(String location_name_pattern)
        + WeatherLocation get_location(String location_name)
    }

    note for AnalysisSettingsManager "Root Aggregate"
    class AnalysisSettingsManager {
        - WeatherAnalysisSettings _settings
        - WeatherLocationRepository _weather_location_repository
        - AnalysisSettingsSubscriber[] _subscribers
        + bool update_settings(String location_name_one, String location_name_two, WeatherMetric metric, WeatherAnalysisType analysis_type, DateTime time_range)
        + publish_settings()
        + subscribe(AnalysisSettingsSubscriber subscriber)
        + unsubscribe(AnalysisSettingsSubscriber subscriber)
    }

    class WeatherAnalysisSettings {
        - WeatherAnalysisSample _sample_one
        - WeatherAnalysisSample _sample_two
        - WeatherAnalysisType _analysis_type
        + WeatherAnalysisSample sample_one()
        + WeatherAnalysisSample sample_two()
        + WeatherAnalysisType analysis_type()
    }

    class WeatherAnalysisSample {
        - WeatherLocation _location
        - WeatherMetric _metric
        - DateTime _time_range
        + WeatherLocation location()
        + WeatherMetric metric()
        + DateTime time_range()
    }

    class WeatherLocation {
        - String _location
        - int _postal_code
        - float _longitude
        - float _latitude
        + String location()
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
    WeatherChartAnalysisResult --|> WeatherAnalysisResult
    WeatherTextAnalysisResult --|> WeatherAnalysisResult

    note for WeatherApi "Comes from Data Context (Root Aggregate)"
    class WeatherApi {
        
    }

    note for WeatherAnalyzer "Root Aggregate"
    class WeatherAnalyzer {
        - WeatherApi _weather_api
        + WeatherChartAnalysisResult analyize_as_chart(WeatherAnalysisSettings settings)
        + WeatherTextAnalysisResult analyize_as_text(WeatherAnalysisSettings settings)
    }

    class WeatherAnalysisResult {
        - WeatherDataResponse _data_one
        - WeatherDataResponse _data_two
        + WeatherDataResponse data_one()
        + WeatherDataResponse data_two()
    }

    class WeatherChartAnalysisResult {
        - String _title
        - String _x_axis_label
        - String _y_axis_label
        + String title()
        + String x_axis_label()
        + String y_axis_label()
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
    WeatherDataResponse *-- WeatherData

    note for WeatherApi "Root Aggregate"
    class WeatherApi {
        - WeatherDataRequest _request
        - WeatherDataResponse _response
        + WeatherDataResponse make_request(WeatherDataRequest request) 
    }

    class WeatherDataRequest {
        - WeatherLocation _location
        - DateTime _time_range
        - WeatherMetric _metric
        + WeatherLocation location()
        + DateTime time_range()
        + WeatherMetric metric()
    }

    class WeatherDataResponse {
        - WeatherLocation _location
        - DateTime _time_range
        - WeatherMetric _metric
        - WeatherData _data
        + WeatherLocation location()
        + DateTime time_range()
        + WeatherMetric metric()
        + WeatherData data()
    }

    class WeatherData {
        - float[] _values
        - DateTime[] _dates
        + float[] values()
        + DateTime[] dates
    }
```

```mermaid
---
title: Dashboard Context
---
classDiagram

    WeatherDashboard --|> AnalysisSettingsSubscriber
    WeatherDashboard *-- AnalysisSettingsManager
    WeatherDashboard *-- WeatherTextWidget
    WeatherDashboard *-- WeatherChartWidget

    note for AnalysisSettingsManager "Comes from the AnalysisSettings Context"
    class AnalysisSettingsManager {

    }

    note for AnalysisSettingsSubscriber "Comes from the AnalysisSettings Context"
    class AnalysisSettingsSubscriber {

    }

    note for WeatherDashboard "Root Aggregate"
    class WeatherDashboard {
        - WeatherAnalyzer _weather_analyzer
        - AnalysisSettingsManager _settings_manager
        - WeatherTextWidget _text_widget
        - WeatherChartWidget _chart_widget
        - WeatherAnalysisSettings _settings
        + on_settings_changed(WeatherAnalysisSettings settings)
        + WeatherTextWidget text_widget()
        + WeatherChartWidget chart_widget()
        + String generate_share_link()
        + WeatherDashboard create_from_share_link(String share_link)
    }

    class WeatherTextWidget {
        - String _title
        - WeatherTextAnalysisResult _content
        + String title()
        + WeatherTextAnalysisResult content()
    }


    class WeatherChartWidget {
        - String _title
        - WeatherChartAnalysisResult _content
        + String title()
        + WeatherChartAnalysisResult content()
        + bool save_as_image(String path)
    }
```
