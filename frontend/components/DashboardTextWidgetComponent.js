export default class DashboardTextWidgetComponent extends HTMLElement {
    constructor(results) {
        super()
        this._locationNameOne = results[0].location.name;
        this._locationNameTwo = results[1].location.name;
        this._valueOne = results[0].value;
        this._valueTwo = results[1].value;
        this._text = `${this._locationNameOne} has a value of ${this._valueOne} whereas ${this._locationNameTwo} has a value of ${this._valueTwo}`;
        this._shadow = this.attachShadow({ mode: "open" });
        this._shadow.append(this.template.content.cloneNode(true));
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
