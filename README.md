# :sun_behind_small_cloud: fhgr-tweather
SAD (Software Architecture and Design) Project @FHGR

## Data
The data for the city locations in Switzerland was retrieved from [here](https://www.swisstopo.admin.ch/de/amtliches-ortschaftenverzeichnis). The data was preprocessed and saved as json file. For this purpose a Script called `preprocess_city_names.py` was written.
The script can be found under `scripts/preprocess_city_names.py` and does the following things:

- Generate a JSON File called `cities.json`
- Converts LV95 Coordinates into Latitude and Longitude Coordinates
- Extracts city name as well as postal code

## Architecture
The Application is split up into multiple packages:

|Context|Description|
|--|----|
|Analysis Settings Context|This context holds all objects related to settings needed for an Analysis|
|Analyze Context|This context holds all objects responsible for actually doing the analysis|
|Data Context|This context holds all objects responsible for retrieving and caching the actual data|
|Dashboard Context|This context holds all objects responsible for displaying the actual dashboard|

For more information see the `doc/architecture.md`. The main Context and therefore entry point of the Application is the `Dashboard Context`.

## Setup
First of all create a `virtual environment`:

```bash
python3 -m venv ./venv
source ./venv/bin/activate # Linux and MacOS
./venv/Scripts/activate # Windows
```

Then install all required packages `see dependencies in pyproject.toml`:

```bash
pip3 install .
```

## Packages

In order to get a feel at how to use the different packages a corresponding `__main__.py` file was created. In order to run it for a corresponding package run the following command:

```bash
python3 -m data # Runs the __main__.py file for the data package
python3 -m analysis_settings # Runs the __main__.py file for the analysis_settings package
python3 -m analyze # Runs the __main__.py file for the analyze package
python3 -m dashboard # Runs the __main__.py file for the dashboard package
```

## Tests
In order to run the tests execute the following command:

```bash
python3 -m unittest discover -v
```
