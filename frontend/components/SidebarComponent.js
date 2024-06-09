import WeatherMetricCardComponent from "./WeatherMetricCardComponent";
import WeatherLocationCardComponent from "./WeatherLocationCardComponent";
import SidebarSettings from "../models/SidebarSettings";

export default class SidebarComponent extends HTMLElement {
    constructor() {
        super();
        this._subscribers = [];

        /** @type {string[]} */
        this._selectedWeatherLocations = [];

        /** @type {string[]} */
        this._selectedWeatherMetrics = [];

        /** @type {Date} */
        this._selectedDate = null;

        this._shadow = this.attachShadow({ mode: "open" });
        this._shadow.append(this.template.content.cloneNode(true));

        this._initElements();
        this._validateWeatherMetrics();
        this._validateWeatherLocations();
        this._validateWeatherDate();

        this._fetchWeatherLocations();
        this._fetchWeatherMetrics();
    }

    /** 
        * Checks if the current settings are valid.
        * @returns {boolean}
    */
    get _settingsValid() {
        return (
            this._selectedWeatherMetrics.length >= 1 &&
            this._selectedWeatherLocations.length == 2 &&
            this._selectedDate != null
        );
    }

    /** 
        * Fetches all Weather Locations from the backend.
    */
    async _fetchWeatherLocations() {
        const API_BASE_URL = import.meta.env.VITE_API_URL;
        const url = `${API_BASE_URL}/weather_locations`;
        const response = await fetch(url);
        const locations = await response.json();
        this._availableWeatherLocations = locations;
        this._weatherLocationCards = this._availableWeatherLocations.map(
            (x) => new WeatherLocationCardComponent(x),
        );
        this._weatherLocationCards.forEach((x) => {
            x.addEventListener("click", () => this._onWeatherLocationCardClicked(x));
            this._weatherLocationCardsContainer.appendChild(x);
        });
    }

    /** 
        * Fetches all Weather Metrics from the backend.
    */
    async _fetchWeatherMetrics() {
        const API_BASE_URL = import.meta.env.VITE_API_URL;
        const url = `${API_BASE_URL}/weather_metrics`;
        const response = await fetch(url);
        const metrics = await response.json();
        this._availableWeatherMetrics = metrics;

        this._weatherMetricCards = this._availableWeatherMetrics.map(
            (x) => new WeatherMetricCardComponent(x),
        );

        this._weatherMetricCards.forEach((x) => {
            x.addEventListener("click", () => this._onWeatherMetricCardClicked(x));
            this._weatherMetricCardsContainer.appendChild(x);
        });
    }

    /** 
        * Updates the disabled/enabled state of the Analyze Button.
    */
    _updateAnalyzeButtonState() {
        if (!this._settingsValid) {
            this._analyzeButton.classList.add("analyze-button-invalid");
        } else {
            this._analyzeButton.classList.remove("analyze-button-invalid");
        }
    }

    /** 
        * Gets called when the user has clicked on the Search Button for searching a specific location. 
    */
    _onWeatherLocationSearchButtonClicked() {
        // Remove any whitespace characters.
        const search = this._weatherLocationSearch.value.trim();

        // Show or hide depending if the name includes the searched text
        this._weatherLocationCards.forEach((x) => {
            // Ignore casing
            if (x.name.toLowerCase().includes(search.toLowerCase())) {
                x.show();
            } else {
                x.hide();
            }
        });
    }

    /** 
        * Gets all needed references to HTML Elements etc. 
    */
    _initElements() {
        this._weatherLocationSearch = this._shadow.querySelector("[data-search]");
        this._weatherLocationSearchButton = this._shadow.querySelector(
            "#weather-location-search-button",
        );

        this._weatherLocationCardsContainer = this._shadow.querySelector(
            "#weather-location-cards-container",
        );

        this._weatherMetricCardsContainer = this._shadow.querySelector(
            "#weather-metric-cards-container",
        );

        this._weatherLocationInfo = this._shadow.querySelector(
            "#weather-location-info",
        );

        this._weatherMetricInfo = this._shadow.querySelector(
            "#weather-metric-info",
        );

        this._weatherDateInfo = this._shadow.querySelector("#weather-date-info");

        this._weatherDate = this._shadow.querySelector("#weather-date");

        this._weatherLocationSearchButton.addEventListener("click", () =>
            this._onWeatherLocationSearchButtonClicked(),
        );


        this._weatherDate.addEventListener("change", () =>
            this._onWeatherDateChanged(),
        );

        this._analyzeButton = this._shadow.querySelector("#analyze-button");
        this._analyzeButton.addEventListener("click", () =>
            this._onAnalyzeButtonClicked(),
        );
    }

    /** 
        * Gets called when the user has selected a date. 
    */
    _onWeatherDateChanged() {
        this._selectedDate = this._weatherDate.value;
        this._validateWeatherDate();
    }

    /** 
        * Gets called when the user has clicked the analyze button. 
    */
    _onAnalyzeButtonClicked() {
        this._notifySettingsChanged();
    }

    /** 
        * Notify any subscribers about changed settings. Only notify if settings are actually valid. 
    */
    _notifySettingsChanged() {
        if (!this._settingsValid) {
            return;
        }
        const settings = new SidebarSettings(
            this._selectedWeatherLocations,
            this._selectedWeatherMetrics,
            this._selectedDate,
        );
        this._subscribers.forEach((s) => s.onSettingsChanged(settings));
    }

    /** 
        * Gets called when the user has clicked on a Weather Location Card (e.g Chur etc.). 
    */
    _onWeatherLocationCardClicked(card) {
        card.toggle();
        const index = this._selectedWeatherLocations.indexOf(card.name);
        const alreadySelected =
            index >= 0 && this._selectedWeatherLocations.length !== 0;
        if (alreadySelected) {
            this._selectedWeatherLocations.splice(index, 1);
        } else {
            this._selectedWeatherLocations.push(card.name);
        }
        this._validateWeatherLocations();
    }

    /** 
        * Gets called when the user has clicked on a Weather Metric Card (e.g Temperature). 
    */
    _onWeatherMetricCardClicked(card) {
        card.toggle();
        const index = this._selectedWeatherMetrics.indexOf(card.metric);
        const alreadySelected =
            index >= 0 && this._selectedWeatherMetrics.length !== 0;
        if (alreadySelected) {
            this._selectedWeatherMetrics.splice(index, 1);
        } else {
            this._selectedWeatherMetrics.push(card.metric);
        }
        this._validateWeatherMetrics();
    }

    /** 
        * Validates the Selected Weather Locations and updates the info message if needed. 
    */
    _validateWeatherLocations() {
        this._updateAnalyzeButtonState();
        const numberOfSelectedWeatherLocations =
            this._selectedWeatherLocations.length;
        if (numberOfSelectedWeatherLocations == 2) {
            this._weatherLocationInfo.classList.remove("error-text");
        } else {
            this._weatherLocationInfo.classList.add("error-text");
        }
    }

    /** 
        * Validates the Selected Weather Metrics and updates the info message if needed. 
    */
    _validateWeatherMetrics() {
        this._updateAnalyzeButtonState();
        const numberOfSelectedWeatherMetrics = this._selectedWeatherMetrics.length;
        if (numberOfSelectedWeatherMetrics < 1) {
            this._weatherMetricInfo.classList.add("error-text");
        } else {
            this._weatherMetricInfo.classList.remove("error-text");
        }
    }

    /** 
        * Validates the Selected Weather Date and updates the info message if needed. 
    */
    _validateWeatherDate() {
        this._updateAnalyzeButtonState();
        if (this._selectedDate == null) {
            this._weatherDateInfo.classList.add("error-text");
        } else {
            this._weatherDateInfo.classList.remove("error-text");
        }
    }

    get styleTemplate() {
        return `
      aside {
          margin-top: calc(var(--header-height) + 2 * 1rem);
          padding: 1rem;
          /* TODO: We probably wanna remove this hardcoded width... */
          max-width: var(--sidebar-width);
          border-right: 1px solid var(--light-highlight-high);
          height: 100%;
          position: absolute;

          section {
              margin-bottom: 1.5rem;

              .title {
                  margin-bottom: 0.5rem;
                  font-weight: 600;
                  font-size: 1rem;
              }

              .subtitle {
                  color: var(--light-subtle);
                  font-weight: 600;
                  font-size: 0.75rem;
              }
          }

          .weather-location-search-container {
                display: flex;
                flex-direction: row;
                justify-content: center;
                align-items: center;
                .weather-location-search {
                    background-color: var(--light-surface);
                    border: 1px solid var(--light-highlight-high);
                    padding: 0.5rem;
                    width: calc(100% - 1rem);
                    font-size: 0.75rem;
                    color: var(--light-muted);
                    border-radius: 5px;

                    &:focus {
                        outline: none !important;
                        border: 1px solid var(--light-foam);
                    }
                }

                #weather-location-search-button {
                    background-color: var(--light-surface);
                    margin-left: 1.5rem;
                    padding: 0.75rem;
                    border: 1px solid var(--light-highlight-high);
                    border-radius: 8px;
                    color: var(--light-text);
                    cursor: pointer;
                }
          }

          .error-text {
              color: var(--light-love) !important;
          }

          #weather-location-cards-container {
              margin-top: 1.5rem;
              display: grid;
              grid-template-columns: 1fr 1fr;
              gap: 1rem;
              max-height: 20rem;
              overflow-y: scroll;
          }

          #weather-metric-cards-container {
              margin-top: 1.5rem;
          }

          #weather-date {
              background-color: var(--light-surface);
              border: 1px solid var(--light-highlight-high);
              padding: 0.5rem;
              width: calc(100% - 1rem);
              color: var(--light-muted);
              border-radius: 5px;

              &:focus {
                  outline: none !important;
                  border: 1px solid var(--light-foam);
              }
          }

          .button-container {
              padding: 1.5rem 0;

              #analyze-button {
                  background-color: var(--light-gold);
                  margin-right: 0.75rem;
                  padding: 0.75rem;
                  border: none;
                  border-radius: 8px;
                  color: var(--light-base);
                  cursor: pointer;

                  &.analyze-button-invalid {
                    background-color: var(--light-love);
                  }
              }

              #reset-button {
                  background-color: var(--light-base);
                  margin-right: 0.75rem;
                  padding: 0.75rem;
                  border: 1px solid var(--light-text);
                  border-radius: 8px;
                  color: var(--light-text);
                  cursor: pointer;
              }
          }
      }
    `;
    }

    get template() {
        const template = document.createElement("template");
        template.innerHTML = `
      <style>${this.styleTemplate}</style>
      <aside>
          <section>
              <h2 class="title">Select Location</h2>
              <p id="weather-location-info" class="subtitle">Please choose exactly two Locations</p>
              <div class="weather-location-search-container">
                <input
                    data-search
                    class="weather-location-search"
                    type="text"
                    placeholder="Search for a location..."/>
                <button id="weather-location-search-button">
                   Search
                </button>
              </div>
              <div id="weather-location-cards-container"></div>
          </section>
          <section>
              <h2 class="title">Select Weather Metrics</h2>
              <p id="weather-metric-info" class="subtitle">Please choose at least one Metric</p>
              <div id="weather-metric-cards-container"></div>
          </section>
          <section>
              <h2 class="title">Pick a Date</h2>
              <p id="weather-date-info" class="subtitle">Please choose a Date for the Comparison</p>
              <input id="weather-date" type="date" />
          </section>
          <section>
              <div class="button-container">
                  <button id="analyze-button">
                      Analyze
                  </button>
                  <button id="reset-button">
                      Reset
                  </button>
              </div>
          </section>
      </aside>
    `;
        return template;
    }

    /*
        * Adds a subscriber to the list
    */
    subscribe(subscriber) {
        const index = this._subscribers.indexOf(subscriber);
        if (index > 0) {
            return;
        }
        this._subscribers.push(subscriber);
    }
}

customElements.define("sidebar-component", SidebarComponent);
