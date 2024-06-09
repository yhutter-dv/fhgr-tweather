import { Chart, registerables } from "chart.js";
import DashboardWidgetsComponent from "./DashboardWidgetsComponent";

// Important: These imports here are necessary so that the component gets registered as custom web components.
// Do not remove them furthermore some of them are used in the JsDoc Comments so they need to be imported.

// eslint-disable-next-line no-unused-vars
import SidebarComponent from "./SidebarComponent";
// eslint-disable-next-line no-unused-vars
import HeaderComponent from "./HeaderComponent";
// eslint-disable-next-line no-unused-vars
import SidebarSettings from "../models/SidebarSettings";

import DashboardWidgetData from "../models/DashboardWidgetData";

class DashboardComponent extends HTMLElement {
    constructor() {
        super();

        // Needed in order to use the various Chart Types of ChartJs.
        Chart.register(...registerables);

        this._shadow = this.attachShadow({ mode: "open" });
        this._shadow.append(this.template.content.cloneNode(true));
        this._container = this._shadow.querySelector("[data-container]");

        /** @type {SidebarComponent} */
        this._sidebar = this._shadow.querySelector("sidebar-component");
        this._sidebar.subscribe(this);

        /** @type {SidebarSettings} */
        this._settings = null;

        // Get references to the HTML Elements such as the error dialog etc.
        this._error_dialog = this._shadow.querySelector("#error-dialog");
        this._error_dialog_description = this._shadow.querySelector("[data-error-description]");
        this._error_dialog_close_button = this._shadow.querySelector("#error-dialog-close");
        this._error_dialog_close_button.addEventListener("click", () => this._closeErrorDialog());
    }

    /** 
        * Closes the error dialog.
    */
    _closeErrorDialog() {
        this._error_dialog.close();
    }

    /** 
        * Shows an Error Dialog with a given message.
        * @param {string} message - The message which should be displayed
    */
    _showErrorDialog(message) {
        this._error_dialog_description.innerHTML = message;
        this._error_dialog.show();
    }

    /** 
        * Makes an analyze request with the current settings.
    */
    async _makeAnalyzeRequest() {
        if (this._settings === null) {
            return;
        }
        const API_BASE_URL = import.meta.env.VITE_API_URL;
        const url = `${API_BASE_URL}/weather_analyze`;
        const requestParams = {
            method: "POST",
            body: JSON.stringify({
                locations: this._settings.locations,
                metrics: this._settings.metrics,
                date: this._settings.date,
            }),
            headers: {
                "Content-type": "application/json",
            },
        };
        const response = await fetch(url, requestParams);
        const analysisResults = await response.json();
        return analysisResults;
    }


    /** 
        * Updates the dashboard according to current settings.
    */
    async _updateDashboardWithCurrentSettings() {
        try {
            // Close any open error dialog
            this._closeErrorDialog();

            const analysisResults = await this._makeAnalyzeRequest();

            // Clear out the existing widgets.
            this._container.innerHTML = "";

            // Create the dashboard widgets according to the Analysis Results
            // Only create them if we have no errors. If we do have any error show the error dialog.
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
            // In case something unexpected happens also show the error dialog.
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

    /** 
        * Gets called when the settings in the sidebar components have changed and are valid 
        * @param {SidebarSettings} settings - The changed and valid settings. 
    */
    onSettingsChanged(settings) {
        this._settings = settings;
        this._updateDashboardWithCurrentSettings();
    }
}

customElements.define("dashboard-component", DashboardComponent);
