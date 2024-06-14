# Architecture
The architecture is split into different parts. First the differente Context (building blocks) of the Application are explained. Afterwards it is described how these builidng blocks interact with each other.

## Context
The whole applications is split up into `different context`. Each context serves a specific puprose. Communication between contexts is done via the `Aggregate Root` Object. Below you can find a short explanation for each context and its purpose

|Context|Description|
|--|----|
|Shared Context|This context only holds Models which are shared between Contexts.|
|Location Context|This context holds all objects related to Weather Locations|
|Data Context|This context holds all objects responsible for retrieving the actual data|
|Analyze Context|This context holds all objects responsible for actually doing the analysis|

```mermaid
---
title: Shared Context
---
classDiagram

    class WeatherMetricEnum {
        <<enumeration>>
        RAIN,
        TEMPERATURE,
        HUMIDTY,
        SNOWFALL
    }

    class WeatherMetric {
        + WeatherMetricEnum identifier
        + String title
        + String description
    }
```

```mermaid
---
title: Location Context
---
classDiagram

    WeatherLocationRepository *-- WeatherLocation

    note for WeatherLocationRepository "Root Aggregate"
    class WeatherLocationRepository {
        - WeatherLocationRepository _instance
        - WeatherLocation[] _weather_locations
        - _init_locations_from_file()
        + add_location(WeatherLocation location)
        + WeatherLocation[] get_locations()
        + String[] get_location_names()
        + WeatherLocation[] find_locations_by_name(String location_name)
        + WeatherLocation find_location_by_name(String location_name)
    }

    class WeatherLocation {
        + String name
        + int postal_code
        + float longitude
        + float latitude
    }

```

```mermaid
---
title: Analyze Context
---
classDiagram

    WeatherAnalyzer *-- WeatherApi
    WeatherAnalyzer *-- WeatherLocationRepository
    WeatherAnalyzer *-- WeatherAnalysisResult
    WeatherAnalyzer *-- WeatherAnalysisSettings
    WeatherAnalysisResult *-- WeatherAnalysisData
    WeatherAnalysisResult *-- WeatherMetricEnum
 
    note for WeatherApi "Comes from Data Context (Root Aggregate)"
    class WeatherApi {
        
    }

    note for WeatherLocationRepository "Comes from Location Context (Root Aggregate)"
    class WeatherLocationRepository {
        
    }

    note for WeatherMetricEnum "Comes from Shared Context"
    class WeatherMetricEnum {
        
    }

    note for WeatherAnalyzer "Root Aggregate"
    class WeatherAnalyzer {
        - WeatherApi _weather_api
        - WeatherLocationRepository _repository
        - _validate_settings(WeatherAnalysisSettings settings)
        + WeatherAnalysisResult[] analyze(WeatherAnalysisSettings settings)
    }

    class WeatherAnalysisSettings {
        + String[] locations
        + WeatherMetricEnum[] metrics
        + Date date
    }


    class WeatherAnalysisResult {
        + WeatherMetricEnum metric
        + String metric_friendly_name
        + Date date
        + WeatherAnalysisData[] results
    }

    class WeatherAnalysisData {
        + String location_name
        + float? value
        + bool has_error
        + String error_reason
    }
```

```mermaid
---
title: Data Context
---
classDiagram

    WeatherApi *-- WeatherDataRequest
    WeatherApi *-- WeatherDataResponse
    WeatherDataRequest *-- WeatherMetricEnum
    WeatherDataResponse *-- WeatherMetricEnum

    note for WeatherMetricEnum "Comes from Shared Context"
    class WeatherMetricEnum {
        
    }

    note for WeatherApi "Root Aggregate"
    class WeatherApi {
        - WeatherApi _instance
        - pd.DataFrame  _create_df_from_variables_with_time(VariablesWithTime variables, String[] metric_keys, bool has_hourly)
        - float[] _get_historical_values(WeatherDataRequest request, String[] metric_keys)
        - float[] _get_current_values(WeatherDataRequest request, String[] metric_keys)
        - float[] _get_forecast_values(WeatherDataRequest request, String[] metric_keys)
        - String _generate_metric_key(WeatherMetricEnum metric, int altitude_in_meters)
        - void _ensure_forecast_date(Date forecast_date)
        + WeatherDataResponse make_request(WeatherDataRequest request) 
    }

    class WeatherDataRequest {
        + WeatherLocation location
        + Date date
        + WeatherMetric[] metrics
    }

    class WeatherDataResponse {
        + WeatherLocation location
        + Date date
        + WeatherMetricEnum metrics
        + float[] values
        + bool has_error
        + String error_reason
    }
```

## Context Mapping

```mermaid
---
title: Context Mapping
---
flowchart BT
    AnalyzeContext --> DataContext
    AnalyzeContext --> LocationContext
    AnalyzeContext --> SharedContext
    DataContext --> SharedContext
```

