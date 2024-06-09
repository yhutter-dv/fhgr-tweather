export default class SidebarSettings {
    /** 
        * @param {string[]} locations - The selected locations  (e.g 'Buchs', 'Chur')
        * @param {string[]} metrics - The selected meetrics (e.g 'temperature', 'rain' etc.). 
        * @param {Date} date - The selected date. 
    */
    constructor(locations, metrics, date) {
        this._locations = locations;
        this._metrics = metrics;
        this._date = date;
    }

    /** 
        * Returns the locations.
        * @returns {string[]}
    */
    get locations() {
        return this._locations;
    }

    /** 
        * Returns the metrics.
        * @returns {string[]}
    */
    get metrics() {
        return this._metrics;
    }

    /** 
        * Returns the date.
        * @returns {Date}
    */
    get date() {
        return this._date;
    }
}
