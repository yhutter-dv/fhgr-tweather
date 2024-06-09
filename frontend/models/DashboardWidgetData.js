export default class DashboardWidgetData {
    /** 
        * @param {any} analysisResult - An analysis Result response from the backend for a specific metric (e.g Temperature)
    */
    constructor(analysisResult) {
        this._metricFriendlyName = analysisResult["metric_friendly_name"];
        this._date = new Date(analysisResult["date"]);
        this._locations = analysisResult.results.map(r => r["location_name"]);

        // We have an error if any for the results have an error.
        this._hasError = analysisResult.results.some(r => r["has_error"]);

        // Remove any duplicated error reasons and join them together
        this._errorReason = [...new Set(analysisResult.results.map(r => r["error_reason"]))].join();

        this._values = analysisResult.results.map(r => r["value"]);
    }

    /** 
        * Returns the friendly name for the metric metric (e.g 'Temperature' for 'temperature').
        * @returns {string}
    */
    get metricFriendlyName() {
        return this._metricFriendlyName;
    }

    /** 
        * Returns the date .
        * @returns {Date}
    */
    get date() {
        return this._date;
    }

    /** 
        * Indicates if the Data has any error.
        * @returns {boolean}
    */
    get hasError() {
        return this._hasError;
    }

    /** 
        * Returns the error Reason.
        * @returns {string}
    */
    get errorReason() {
        return this._errorReason;
    }

    /** 
        * Returns the locations.
        * @returns {string[]}
    */
    get locations() {
        return this._locations;
    }

    /** 
        * Returns the values.
        * @returns {number[]}
    */
    get values() {
        return this._values;
    }

}
