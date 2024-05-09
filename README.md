# :sun_behind_small_cloud: fhgr-tweather
SAD (Software Architecture and Design) Project @FHGR

## Data
The data for the city locations in Switzerland was retrieved from [here](https://www.swisstopo.admin.ch/de/amtliches-ortschaftenverzeichnis). The data was preprocessed and saved as json file. For this purpose a Script called `preprocess_city_names.py` was written.
The script can be found under `scripts/preprocess_city_names.py` and does the following things:

- Generate a JSON File called `cities.json`
- Converts LV95 Coordinates into Latitude and Longitude Coordinates
- Extracts city name as well as postal code

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
The Application is split up into multiple packages. The packages are based on the defined Aggregates (see `doc/architecture.md` file). The main package and therefore entry point of the Application is the `dashboard` package.
In order to get a feel at how to use the different packages a corresponding `__main__.py` file was created. In order to run it for a corresponding package run the following command:

```bash
python3 -m data # Runs the __main__.py file for the data package
```

## Tests
In order to run the tests execute the following command:

```bash
python3 -m unittest discover -v
```
