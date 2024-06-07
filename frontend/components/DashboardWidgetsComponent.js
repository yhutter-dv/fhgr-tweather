import DashboardChartWidgetComponent from './DashboardChartWidgetComponent';
import DashboardTextWidgetComponent from './DashboardTextWidgetComponent';

export default class DashboardWidgetsComponent extends HTMLElement {
    constructor(metric, results) {
        super();
        this._metric = metric;
        this._date = new Date(results[0].date);
        this._shadow = this.attachShadow({ mode: "open" });
        this._shadow.append(this.template.content.cloneNode(true));
        this._dashboard_widgets_container = this._shadow.querySelector("[data-dashboard-widgets]");

        // Create dedicated widgets, for now we only have a chart and text widget
        this._chartWidget = new DashboardChartWidgetComponent(results);
        this._textWidget = new DashboardTextWidgetComponent(results);
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
              <h1>Temperature</h1>
              <div data-dashboard-widgets class="container-wrapper"></div>
          </section>
        `;
        return template;
    }
}

customElements.define("dashboard-widget-component", DashboardWidgetsComponent);
