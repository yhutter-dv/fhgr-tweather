# :sun_behind_small_cloud: FHR Tweather App 
Tweather makes it easy to compare two different locations in Switzerland depending on your defined metrics. Therefore allowing you to pick out the location which fits your needs the most. The name Tweather itself is a pun on Tinder for Weather Locations. This project was done as part of the SAD (Software Architecture and Design) Module @FHGR.


## Prerequisites

> :warning: Please make sure you have the following tools installed on your system

- [Python](https://www.python.org/) >= v.3.11
- [NodeJs](https://nodejs.org/en)


## Data
The data for the city locations in Switzerland was retrieved from [here](https://www.swisstopo.admin.ch/de/amtliches-ortschaftenverzeichnis). The data was preprocessed and saved as json file. For this purpose a Script called `preprocess_city_names.py` was written.
The script can be found under `scripts/preprocess_city_names.py` and does the following things:

- Generate a JSON File called `cities.json`
- Converts LV95 Coordinates into Latitude and Longitude Coordinates
- Extracts city name as well as postal code

## Architecture
The Application is split up into a `frontend` and `backend`. 

### Frontend
The frontend is a simple HTML Appliation which displays the results coming from the backend. The following Technologies were used for the development of the frontend:

- [Vite](https://vitejs.dev/) - Frontend Tool Kit (Webbundler)
- [AlpineJs](https://alpinejs.dev/) - Minimal JavaScript Framework mainly used for Components
- [Tailwind CSS](https://tailwindcss.com/) - CSS Framework for styling

### Backend
The backend itself is written with Python and [FastApi](https://fastapi.tiangolo.com/). For the actual weather metrics themselves [Open Meteo](https://open-meteo.com/) was used.

For more information about the Software Architecture itself see `doc/architecture.md`.

In order to get a feel at how to use the different packages a corresponding `__main__.py` file was created. In order to run it for a corresponding package run the following command:

```bash
python3 -m data # Runs the __main__.py file for the data package
python3 -m analysis_settings # Runs the __main__.py file for the analysis_settings package
python3 -m analyze # Runs the __main__.py file for the analyze package
python3 -m dashboard # Runs the __main__.py file for the dashboard package
```

In order to run the tests execute the following command:

```bash
python3 -m unittest discover -v
```

## Setup
These steps only need to be done one time.

### Backend
First change into the `backend` directory and create a `virtual environment`:

```bash
cd backend
python3 -m venv ./venv
source ./venv/bin/activate # Linux and MacOS
./venv/Scripts/activate # Windows
```

Then install all required packages `see dependencies in pyproject.toml`:

```bash
pip3 install .
```

### Frontend
Change into the `frontend` directory and install all required packages by runnin the following command:

```bash
cd backend
npm i
```

## Running the Application

> :warning: Please make sure that the Backend is started before the Frontend.

### Backend 

> Please note that this step assumes that you have your Python Virtual Environment activated and are inside the `backend` directory.

In order to run the Backend (Fast API) simply execute the following command:

```bash
fastapi dev
```
The OpenAPI Page should now be available under the following [URL](http://localhost:8000/docs)

### Frontend

> Please note that this assumes that you are inside the `frontend` directory.

In order to run the Frontend simply execute the following command:

```bash
npm run dev
```
