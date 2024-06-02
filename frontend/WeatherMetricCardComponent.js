class WeatherMetricCardComponent extends HTMLElement {
  constructor(metric, metricTitle, metricDescription) {
    super();
    this._metric = metric;
    this._metricTitle = metricTitle;
    this._metricDescription = metricDescription;

    this._shadow = this.attachShadow({ mode: "open" });
    this._shadow.append(this.template.content.cloneNode(true));

    this._container = this._shadow.querySelector("[data-container]");
  }

  toggle() {
    this._container.classList.toggle("weather-metric-card-selected");
  }

  get metric() {
    return this._metric;
  }

  get styleTemplate() {
    return `
      .weather-metric-card {
          padding: 1rem;
          background-color: var(--light-surface);
          border-radius: 5px;
          cursor: pointer;
          margin-bottom: 1.5rem;

          .title {
              font-weight: 600;
          }

          .description {
              font-size: 14px;
              font-weight: normal;
              color: var(--light-subtle);
          }
      }

      .weather-metric-card-selected {
          background-color: var(--light-foam);
          color: var(--light-base);

          .description{
              color: var(--light-base);
          }
      }
    `;
  }

  get template() {
    const template = document.createElement("template");
    template.innerHTML = `
      <style>${this.styleTemplate}</style>
      <div data-container class="weather-metric-card">
        <p class="title">${this._metricTitle}</p>
        <p class="description">${this._metricDescription}</p>
      </div>`;
    return template;
  }
}

customElements.define("weather-metric-card", WeatherMetricCardComponent);
