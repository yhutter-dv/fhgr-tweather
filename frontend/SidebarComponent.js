class SidebarComponent extends HTMLElement {
  constructor() {
    super();
    // TODO: Fetch fia requests...
    this._availableWeatherLocations = [
      "Chur",
      "Buchs",
      "Mels",
      "St. Gallen",
      "Zürich",
    ];
    this._availableWeatherMetrics = [
      {
        metric: "temperature",
        title: "Temperature",
        description: "Make a comparison based on Temperature in °C",
      },
      {
        metric: "rain",
        title: "Rain",
        description: "Amount of rain",
      },
    ];
    this._selectedWeatherLocations = [];
    this._selectedWeatherMetrics = [];

    this._shadow = this.attachShadow({ mode: "open" });
    this._shadow.append(this.template.content.cloneNode(true));

    // Get necessary references to HTML Elements
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

    this._weatherLocationCards = this._availableWeatherLocations.map(
      (x) => new WeatherLocationCardComponent(x),
    );

    this._weatherLocationCards.forEach((x) => {
      x.addEventListener("click", () => this._onWeatherLocationCardClicked(x));
      this._weatherLocationCardsContainer.appendChild(x);
    });

    this._weatherMetricCards = this._availableWeatherMetrics.map(
      (x) => new WeatherMetricCardComponent(x.metric, x.title, x.description),
    );

    this._weatherMetricCards.forEach((x) => {
      x.addEventListener("click", () => this._onWeatherMetricCardClicked(x));
      this._weatherMetricCardsContainer.appendChild(x);
    });
  }

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

  _validateWeatherLocations() {
    const numberOfSelectedWeatherLocations =
      this._selectedWeatherLocations.length;
    if (numberOfSelectedWeatherLocations > 2) {
      this._weatherLocationInfo.classList.add("error-text");
      this._weatherLocationInfo.innerHTML = `You have choosen ${numberOfSelectedWeatherLocations} Locations but you have to choose exactly two`;
    } else {
      this._weatherLocationInfo.classList.remove("error-text");
      this._weatherLocationInfo.innerHTML = `Please choose exactly two Locations`;
    }
  }

  _validateWeatherMetrics() {
    const numberOfSelectedWeatherMetrics = this._selectedWeatherMetrics.length;

    if (numberOfSelectedWeatherMetrics < 1) {
      this._weatherMetricInfo.classList.add("error-text");
      this._weatherMetricInfo.innerHTML = `You have to choose at least one Weather Metric`;
    } else {
      this._weatherMetricInfo.classList.remove("error-text");
      this._weatherMetricInfo.innerHTML = `Choose your Weather Metrics`;
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

          .weather-locations-search {
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

          .error-text {
              color: var(--light-love) !important;
          }

          #weather-location-cards-container {
              margin-top: 1.5rem;
              display: grid;
              grid-template-columns: 1fr 1fr;
              gap: 1rem;
              /* TODO: Define Max Height */
              /* max-height: 15rem; */
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

              .primary-button {
                  background-color: var(--light-gold);
                  margin-right: 0.75rem;
                  padding: 0.75rem;
                  border: none;
                  border-radius: 8px;
                  color: var(--light-base);
                  cursor: pointer;
              }

              .secondary-button {
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
              <p id="weather-location-info" class="subtitle"></p>
              <input
                  class="weather-locations-search"
                  type="text"
                  placeholder="Search for a location..."
              />
              <div id="weather-location-cards-container"></div>
          </section>
          <section>
              <h2 class="title">Select Weather Metrics</h2>
              <p id="weather-metric-info" class="subtitle"></p>
              <div id="weather-metric-cards-container"></div>
          </section>
          <section>
              <h2 class="title">Pick a Date</h2>
              <p class="subtitle">Please choose a Date for the Comparison</p>
              <input id="weather-date" type="date" />
          </section>
          <section>
              <div class="button-container">
                  <button id="analyze-button" class="primary-button">
                      Analyze
                  </button>
                  <button id="reset-button" class="secondary-button">
                      Reset
                  </button>
              </div>
          </section>
      </aside>
    `;
    return template;
  }
}

customElements.define("sidebar-component", SidebarComponent);
