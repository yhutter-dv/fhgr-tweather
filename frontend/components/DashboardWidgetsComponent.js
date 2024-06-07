import DashboardChartWidgetComponent from './DashboardChartWidgetComponent';
import DashboardTextWidgetComponent from './DashboardTextWidgetComponent';

export default class DashboardWidgetsComponent extends HTMLElement {
    constructor(widgetData) {
        super();
        this._widgetData = widgetData;
        this._shadow = this.attachShadow({ mode: "open" });
        this._shadow.append(this.template.content.cloneNode(true));
        this._dashboard_widgets_container = this._shadow.querySelector("[data-dashboard-widgets]");

        // Create dedicated widgets, for now we only have a chart and text widget but only if we do not have any errors
        if (this._widgetData.hasError) {
            return;
        }
        this._chartWidget = new DashboardChartWidgetComponent(this._widgetData);
        this._textWidget = new DashboardTextWidgetComponent(this._widgetData);
        this._dashboard_widgets_container.append(this._chartWidget);
        this._dashboard_widgets_container.append(this._textWidget);
    }

    get styleTemplate() {
        return `
          section {
              .container-wrapper {
                  display: flex;
                  flex-direction: column;
                  color: var(--light-text);
              }
          }
        `;
    }

    get template() {
        const template = document.createElement("template");
        template.innerHTML = `
          <style>${this.styleTemplate}</style>
          <section>
              <h1>${this._widgetData.metricFriendlyName}</h1>
              <div data-dashboard-widgets class="container-wrapper"></div>
          </section>
        `;
        return template;
    }
}

customElements.define("dashboard-widget-component", DashboardWidgetsComponent);
