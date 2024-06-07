export default class DashboardWidgetData {
    constructor(analysisResult) {
        this._metricFriendlyName = analysisResult["metric_friendly_name"];
        this._date = new Date(analysisResult["date"]);
        this._locations = analysisResult.results.map(r => r["location_name"]);
        this._hasError = analysisResult.results.some(r => r["has_error"]);
        this._errorReason = analysisResult.results.map(r => r["error_reason"]).join();
        this._values = analysisResult.results.map(r => r["value"]);
    }

    get metricFriendlyName() {
        return this._metricFriendlyName;
    }

    get date() {
        return this._date;
    }

    get hasError() {
        return this._hasError;
    }

    get errorReason() {
        return this._errorReason;
    }

    get locations() {
        return this._locations;
    }

    get values() {
        return this._values;
    }

}
