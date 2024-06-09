import { Chart } from "chart.js";

export default class DashboardChartWidgetComponent extends HTMLElement {
    /** 
        * @param {DashboardWidgetData} widgetData - The Data for the Widget.
    */
    constructor(widgetData) {
        super()
        this._widgetData = widgetData;
        this._shadow = this.attachShadow({ mode: "open" });
        this._shadow.append(this.template.content.cloneNode(true));

        this._chartDownloadButton = this._shadow.querySelector(".chart-download");
        this._chartDownloadButton.addEventListener("click", () => this._exportChartAsImage());
    }

    /** 
        * Returns the default chart options. See https://www.chartjs.org/docs/latest/general/options.html for further information
    */
    _defaultChartOptions() {
        const root = document.querySelector(":root");
        const foamColor = getComputedStyle(root).getPropertyValue("--light-foam");

        const goldColor = getComputedStyle(root).getPropertyValue("--light-gold");

        const labels = this._widgetData.locations;
        const data = this._widgetData.values;

        // Currently we only support bar charts.
        return {
            type: "bar",
            data: {
                labels: labels,
                datasets: [
                    {
                        borderRadius: 5,
                        barPercentage: 0.4,
                        categoryPercentage: 1.0,
                        data: data,
                        backgroundColor: [foamColor, goldColor],
                        borderWidth: 0,
                    },
                ],
            },
            options: {
                plugins: {
                    legend: false,
                },
                indexAxis: "y",
                responsive: true,
                scales: {
                    y: {
                        grid: {
                            display: false,
                            drawOnChartArea: false,
                            drawTicks: false,
                        },
                    },
                    x: {
                        grid: {
                            display: false,
                            drawOnChartArea: false,
                            drawTicks: false,
                        },
                    },
                },
            },
        }
    }


    /** 
        * Initializes the Chart Context. Note that this method HAS to be called after the Component has mounted (e.g connectedCallback).
        * Otherweise the Canvas Element from which the context is retrieved is not ready yet.
    */
    _initChart() {
        const chartContext = this._shadow.getElementById("chart");
        const chartOptions = this._defaultChartOptions();
        this._chart = new Chart(chartContext, chartOptions);
    }

    /** 
        * Exports the Chart as an Image File 
    */
    _exportChartAsImage() {
        if (this._chart === null) {
            return;
        }
        const linkElement = document.createElement('a');
        linkElement.href = this._chart.toBase64Image();
        linkElement.download = 'TweatherChartExport.png';
        linkElement.click();
        linkElement.remove();
    }

    /** 
        * Callback which automatically gets called once the WebComponent is attached to the DOM. 
    */
    connectedCallback() {
        this._initChart();
    }

    get styleTemplate() {
        return `
          .chart-container {
              background-color: var(--light-surface);
              padding: 2rem;
              margin-bottom: 1rem;
              border-radius: 5px;

              .chart-header {
                  display: flex;
                  justify-content: space-between;
                  color: var(--light-subtle);
                  font-size: 0.75rem;
                  margin-bottom: 1rem;

                  .chart-download {
                      cursor: pointer;
                      padding: 10px;
                      width: 1rem;
                      height: 1rem;
                      border: 1px solid var(--light-foam);
                      border-radius: 8px;
                      color: var(--light-foam);
                      transition: all 0.2s ease-in;

                      &:hover {
                          background-color: var(--light-foam);
                          color: var(--light-surface);
                      }

                      .chart-download-icon {
                          color: inherit !important;
                      }
                  }
              }
          }
        `;
    }

    get template() {
        const template = document.createElement("template");
        template.innerHTML = `
          <style>${this.styleTemplate}</style>
          <section>
              <div class="chart-container">
                  <div class="chart-header">
                      <p>${this._widgetData.date}</p>
                      <div class="chart-download">
                          <svg
                              xmlns="http://www.w3.org/2000/svg"
                              viewBox="0 0 20 20"
                              fill="currentColor"
                              class="chart-download-icon"
                          >
                              <path
                                  d="M10.75 2.75a.75.75 0 0 0-1.5 0v8.614L6.295 8.235a.75.75 0 1 0-1.09 1.03l4.25 4.5a.75.75 0 0 0 1.09 0l4.25-4.5a.75.75 0 0 0-1.09-1.03l-2.955 3.129V2.75Z"
                              />
                              <path
                                  d="M3.5 12.75a.75.75 0 0 0-1.5 0v2.5A2.75 2.75 0 0 0 4.75 18h10.5A2.75 2.75 0 0 0 18 15.25v-2.5a.75.75 0 0 0-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5Z"
                              />
                          </svg>
                      </div>
                  </div>
                  <canvas id="chart"></canvas>
              </div>
          </section>
        `;
        return template;
    }
}

customElements.define("dashboard-chart-widget-component", DashboardChartWidgetComponent);
