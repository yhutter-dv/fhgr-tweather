# :sun_behind_small_cloud: FHR Tweather App
Tweather makes it easy to compare two different locations in Switzerland, depending on your defined metrics. Therefore, it allows you to pick out the location that fits your needs the most. The name Tweather itself is a pun on Tinder for Weather Locations (find your suitable location depending on your preferences) This project was done as part of the SAD (Software Architecture and Design) Module at the University of Applied Sciences of the Grisons.

## Screenhots
Here's what the Web Application Looks like (Kudos for the Colors go to [Rosé Pine](https://rosepinetheme.com/)): 
![Screenshot 01](./images/tweather_screenshot_01.png)

## Prerequisites
> :warning: The installation of the following software is a prerequisite for the installation and starting up of the application.
- [Python (>= 3.11)](https://wiki.python.org/moin/BeginnersGuide/Download)
- [Node.js (incl. npm; v21.0)](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- [Chrome Browser (v >= 67)](https://www.google.com/chrome/)

## Preprocessing
The API we use to retrieve the Weather Information is called [Open Meteo](https://open-meteo.com/en/docs). The API works by passing in the Longitude and Latitude values of the location, which are the weather metrics you want to know. As the purpose of this process was to support locations based in Switzerland, we used the following [CSV](https://www.swisstopo.admin.ch/de/amtliches-ortschaftenverzeichnis) file as a base. However, the entries in that CSV File are do not contain Longitude and Latitude values. To get around this, a small Python Script was written that takes each location, calculates the correct Latitude and Longitude values, and saves the result back as a JSON File. The script can be found under `scripts/preprocess_city_names.py` and does the following things:

- Generate a JSON File called `cities.json`
- Converts LV95 Coordinates into Latitude and Longitude Coordinates
- Extracts the city name as well as the postal code

# Setup
These steps only need to be done once.

## Installation and start-up of backend
The backend of the application is programmed with Python and uses the [FastAPI](https://fastapi.tiangolo.com/) Framework.

### Virtual environment
It is recommended to use a [virtual environment](https://docs.python.org/3/library/venv.html) (venv) to avoid potential conflicts with already-installed Python libraries. To create a virtual environment for the backend, go to the `backend` directory and run the following command: 
```bash
python -m venv ./venv
```
The Virtual Environment can then be activated. In a *nix environment, the virtual environment is activated with the following command:
```bash
source ./venv/bin/activate
```
In a Windows environment, the virtual environment is activated with the following command:
```bash
source .\venv\Scripts\activate.bat 
```

### Installation backend
To install the backend, switch to the `backend` directory and run the following command to install the required program libraries:
```bash
pip3 install .
```
### Start backend
Switch to the `backend` directory and execute the following command line to start the FastAPI server:
```bash
fastapi dev
```
If the FastAPI server could be started successfully, a message would appear with the address under which the server can be reached (by default, http://127.0.0.1:8000):

```bash
 ╭────────── FastAPI CLI - Development mode ────────╮
 │                                                  │
 │  Serving at: http://127.0.0.1:8000               │
 │                                                  │
 │  API docs: http://127.0.0.1:8000/docs            │
 │                                                  │
 │  Running in development mode, for production use:│
 │                                                  │
 │  fastapi run                                     │
 │                                                  │
 ╰──────────────────────────────────────────────────╯
```

## Installation and start-up of frontend
The frontend was implemented with HTML, CSS and JS. [Vite](https://vitejs.dev/) was used as a build tool to "compile" the components.

### Installation frontend
Change into the `frontend` directory and install all required packages by running the following command:
```bash
npm i
```
### Start frontend
For the frontend to be functional, the backend must be started first. In addition, it must be ensured that the value of `VITE_API_URL` in the file `frontend/.env` corresponds to the server address of the FastAPI server:
```
VITE_API_URL=http://127.0.0.1:8000
```
To start a local server for the frontend, go to the `frontend` directory and execute the following command:
```bash
npm run dev
```
If the server could be started successfully, a corresponding message would appear with the address under which the server can be reached (by default, http://localhost:5173):
```bash
  VITE v5.2.11  ready in 242 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

# Architecture
The application is split up into a `frontend` and `backend` part.

## Frontend
The frontend is a simple HTML5 application that displays the results coming from the backend. The following technologies were used for the development of the frontend:

- [Vite](https://vitejs.dev/) - Frontend Tool Kit (Web bundler)
- [Rose Pine](https://rosepinetheme.com/palette/) - Used Color Scheme
- [ChartJS](https://www.chartjs.org/) - Chart Library

## Backend
The backend itself is written in Python and [FastAPI](https://fastapi.tiangolo.com/). For the actual weather metrics themselves, [Open Meteo](https://open-meteo.com/) was used. For more information about the Software architecture, also see `doc/architecture.md`.

## Main Packages
> Please note that in order for this to work you have to have your Virtual Environment activated.

The backend is split up into three different packages. The main application entrypoint is the `analyze` package.

To get a feel for how to use the different packages, a corresponding `__main__.py` file was created. To run it for a corresponding package, run the following command (depending on your Operating System)

### *nix systems
```bash
cd backend
python3 -m data # Runs the __main__.py file for the data package
python3 -m location # Runs the __main__.py file for the location
python3 -m analyze # Runs the __main__.py file for the analyze package
```
### Windows
```bash
cd backend
python -m data # Runs the __main__.py file for the data package
python -m location # Runs the __main__.py file for the location
python -m analyze # Runs the __main__.py file for the analyze package
```
## Unit Tests
For the different packages, some Unit Tests were also implemented. To run them, simply execute the following command (depending on your Operating System):

### *nix systems
```bash
cd backend
python3 -m unittest discover -v 
```
### Windows 
```bash
cd backend
python -m unittest discover -v 
```
