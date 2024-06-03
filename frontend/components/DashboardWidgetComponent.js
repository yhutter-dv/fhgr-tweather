import { Chart } from "chart.js";

export default class DashboardWidgetComponent extends HTMLElement {
  constructor() {
    super();
    this._shadow = this.attachShadow({ mode: "open" });
    this._shadow.append(this.template.content.cloneNode(true));
    this._container = this._shadow.querySelector("[data-container]");
  }

  connectedCallback() {
    this._initChart();
  }

  _initChart() {
    const root = document.querySelector(":root");
    const foamColor = getComputedStyle(root).getPropertyValue("--light-foam");

    const goldColor = getComputedStyle(root).getPropertyValue("--light-gold");

    const chartContext = this._shadow.getElementById("chart");
    this._chart = new Chart(chartContext, {
      type: "bar",
      data: {
        labels: ["Buchs", "Chur"],
        datasets: [
          {
            borderRadius: 5,
            barPercentage: 0.4,
            categoryPercentage: 1.0,
            data: [10, 15],
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
    });
  }

  get styleTemplate() {
    return `
      section {
          .container-wrapper {
              display: flex;
              flex-direction: column;
              color: var(--light-text);

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
          <div class="container-wrapper">
              <div class="chart-container">
                  <div class="chart-header">
                      <p>30.03.2024</p>
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
              <div class="text-container">
                  <p>At 30.03 Chur is 15°C hoter then Buchs</p>
              </div>
          </div>
      </section>
    `;
    return template;
  }
}

customElements.define("dashboard-widget-component", DashboardWidgetComponent);
