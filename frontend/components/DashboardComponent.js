import { Chart, registerables } from "chart.js";
import DashboardWidgetsComponent from "./DashboardWidgetsComponent";

// Important: These imports here are necessary so that the component gets registered as custom web components.
// Do not remove them
import SidebarComponent from "./SidebarComponent";
import HeaderComponent from "./HeaderComponent";
import DashboardWidgetData from "../models/DashboardWidgetData";

class DashboardComponent extends HTMLElement {
    constructor() {
        super();

        // Needed in order to use the various Chart Types of Chartjs.
        Chart.register(...registerables);

        this._shadow = this.attachShadow({ mode: "open" });
        this._shadow.append(this.template.content.cloneNode(true));
        this._container = this._shadow.querySelector("[data-container]");

        this._sidebar = this._shadow.querySelector("sidebar-component");
        this._sidebar.subscribe(this);

        this._error_dialog = this._shadow.querySelector("#error-dialog");
        this._error_dialog_description = this._shadow.querySelector("[data-error-description]");
        this._error_dialog_close_button = this._shadow.querySelector("#error-dialog-close");
        this._error_dialog_close_button.addEventListener("click", () => this._closeErrorDialog());
    }

    _closeErrorDialog() {
        this._error_dialog.close();
    }

    _showErrorDialog(message) {
        this._error_dialog_description.innerHTML = message;
        this._error_dialog.show();
    }

    async _updateDashboard(settings) {
        const API_BASE_URL = import.meta.env.VITE_API_URL;
        const url = `${API_BASE_URL}/weather_analyze`;
        const requestParams = {
            method: "POST",
            body: JSON.stringify({
                locations: settings.locations,
                metrics: settings.metrics,
                date: settings.date,
            }),
            headers: {
                "Content-type": "application/json",
            },
        };

        try {
            // Close any open error dialog
            this._closeErrorDialog();

            const response = await fetch(url, requestParams);
            const analysisResults = await response.json();
            this._container.innerHTML = "";

            for (let i = 0; i < analysisResults.length; i++) {
                const analysisResult = analysisResults[i];
                const widgetData = new DashboardWidgetData(analysisResult);
                if (widgetData.hasError) {
                    this._showErrorDialog(widgetData.errorReason);
                    break;
                }
                this._container.appendChild(
                    new DashboardWidgetsComponent(widgetData),
                );
            }
        } catch (e) {
            this._showErrorDialog(e.stack);
        }

    }

    get styleTemplate() {
        return `
          #error-dialog {
              position: absolute;
              max-width: 25vw;
              top: 50vh;
              border-radius: 0.5rem;
              padding: 2rem;
              border: 1px solid var(--light-text);
              color: var(--light-text);
              background-color: var(--light-surface);

              #error-dialog-close {
                margin-top: 1.5rem;
                padding: 0.75rem;
                border: 1px solid var(--light-highlight-high);
                border-radius: 8px;
                color: var(--light-text);
                cursor: pointer;
              }
          }
          main {
              position: absolute;
              left: calc(var(--sidebar-width) + 2 * 1rem);
              top: 6rem;
              width: calc(100% - calc(var(--sidebar-width) + 2rem + 4rem));
              display: grid;
              padding: 1rem 2rem;
              grid-template-columns: 1fr 1fr;
              gap: 1rem;
          }
        `;
    }

    get template() {
        const template = document.createElement("template");
        template.innerHTML = `
          <style>${this.styleTemplate}</style>
          <header-component></header-component>
          <sidebar-component></sidebar-component>
          <main data-container></main>
          <dialog id="error-dialog">
            <h2>Oops something went wrong</h2>
            <br />
            <p data-error-description></p>
            <button id="error-dialog-close">Close</button>
          </dialog>
        `;
        return template;
    }

    onSettingsChanged(settings) {
        this._updateDashboard(settings);
    }
}

customElements.define("dashboard-component", DashboardComponent);
