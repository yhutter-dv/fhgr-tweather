import { Chart, registerables } from "chart.js";
import DashboardWidgetComponent from "./DashboardWidgetComponent";

// Important: These imports here are necessary so that the component gets registered as custom web components.
// Do not remove them
import SidebarComponent from "./SidebarComponent";
import HeaderComponent from "./HeaderComponent";

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

    this._container.appendChild(new DashboardWidgetComponent());
  }

  get styleTemplate() {
    return `
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
    `;
    return template;
  }

  onSettingsChanged(settings) {
    console.log("Settings have changed ", settings);
  }
}

customElements.define("dashboard-component", DashboardComponent);
