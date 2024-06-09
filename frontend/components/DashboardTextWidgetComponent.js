
// eslint-disable-next-line no-unused-vars
import DashboardWidgetData from "../models/DashboardWidgetData";

export default class DashboardTextWidgetComponent extends HTMLElement {
    /** 
        * @param {DashboardWidgetData} widgetData - The Data for the Widget.
    */
    constructor(widgetData) {
        super()
        this._widgetData = widgetData;
        this._text = this._createText();
        this._shadow = this.attachShadow({ mode: "open" });
        this._shadow.append(this.template.content.cloneNode(true));
    }

    /** 
        * Creates a text message from the current data.
        * @returns {string}
    */
    _createText() {
        const locationOne = this._widgetData.locations[0];
        const locationTwo = this._widgetData.locations[1];
        const valueOne = this._widgetData.values[0].toFixed(2);
        const valueTwo = this._widgetData.values[1].toFixed(2);
        const difference = Math.abs(valueOne - valueTwo).toFixed(2);
        return `${locationOne} has a value of ${valueOne} whereas ${locationTwo} has a value of ${valueTwo}. The difference is ${difference}`;
    }

    get styleTemplate() {
        return `
            .text-container {
              padding: 2rem;
              display: flex;
              justify-content: center;
              align-items: center;
              font-weight: 600;
              font-size: 0.75rem;
              border-radius: 5px;
              background-color: var(--light-surface);
            }
        `;
    }

    get template() {
        const template = document.createElement("template");
        template.innerHTML = `
          <style>${this.styleTemplate}</style>
          <div class="text-container">
              <p>${this._text}</p>
          </div>
        `;
        return template;
    }
}

customElements.define("dashboard-text-widget-component", DashboardTextWidgetComponent);
