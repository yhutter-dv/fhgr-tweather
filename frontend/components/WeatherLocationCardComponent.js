export default class WeatherLocationCardComponent extends HTMLElement {
  constructor(locationName) {
    super();
    this._locationName = locationName;
    this._shadow = this.attachShadow({ mode: "open" });
    this._shadow.append(this.template.content.cloneNode(true));

    this._container = this._shadow.querySelector("[data-container]");
  }

  toggle() {
    this._container.classList.toggle("weather-location-card-selected");
  }

  hide() {
    this.style.display = "none";
  }

  show() {
    this.style.display = "block";
  }

  get name() {
    return this._locationName;
  }

  get styleTemplate() {
    return `
      .weather-location-card {
          display: flex;
          padding: 1.5rem;
          justify-content: center;
          align-items: center;
          background-color: var(--light-surface);
          border-radius: 5px;
          cursor: pointer;

          p {
              margin: 0;
          }
      }

      .weather-location-card-selected {
          background-color: var(--light-foam);
          color: var(--light-base);
      }
    `;
  }

  get template() {
    const template = document.createElement("template");
    template.innerHTML = `
      <style>${this.styleTemplate}</style>
      <div data-container class="weather-location-card">
        <p>${this._locationName}</p>
      </div>`;
    return template;
  }
}

customElements.define("weather-location-card", WeatherLocationCardComponent);
