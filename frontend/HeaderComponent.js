class HeaderComponent extends HTMLElement {
  constructor() {
    super();
    this.shadow = this.attachShadow({ mode: "open" });
    this.shadow.append(this.template.content.cloneNode(true));
  }

  get styleTemplate() {
    return `
      header {
          display: flex;
          padding: 1rem 2rem;
          align-items: center;
          border-bottom: 1px solid var(--light-highlight-high);
          position: fixed;
          height: var(--header-height);
          top: 0;
          width: 100%;
          backdrop-filter: blur(10px);
          background-color: var(--light-base-transparent);
          z-index: 2;

          .header-logo {
              height: 2rem;
              margin-right: 1rem;
              fill: var(--light-foam);
          }

          .header-text {
              font-weight: bold;
              font-size: 1.5rem;
          }
      }
    `;
  }

  get template() {
    const template = document.createElement("template");
    template.innerHTML = `
      <style>${this.styleTemplate}</style>
      <header>
          <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              class="header-logo"
          >
              <path
                  fill-rule="evenodd"
                  d="M4.5 9.75a6 6 0 0 1 11.573-2.226 3.75 3.75 0 0 1 4.133 4.303A4.5 4.5 0 0 1 18 20.25H6.75a5.25 5.25 0 0 1-2.23-10.004 6.072 6.072 0 0 1-.02-.496Z"
                  clip-rule="evenodd"
              />
          </svg>
          <h1 class="header-text">Tweather</h1>
      </header>
    `;
    return template;
  }
}

customElements.define("header-component", HeaderComponent);
