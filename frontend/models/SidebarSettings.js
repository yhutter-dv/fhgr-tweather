export default class SidebarSettings {
  constructor(locations, metrics, date) {
    this._locations = locations;
    this._metrics = metrics;
    this._date = date;
  }

  get locations() {
    return this._locations;
  }

  get metrics() {
    return this._metrics;
  }

  get date() {
    return this._date;
  }
}
