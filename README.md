# :sun_behind_small_cloud: fhgr-tweather
SAD (Software Architecture and Design) Project @FHGR

## Data
The data for the city locations in Switzerland was retrieved from [here](https://www.swisstopo.admin.ch/de/amtliches-ortschaftenverzeichnis). The data was preprocessed and saved as json file. For this purpose a Script called `preprocess_city_names.py` was written.

It converts LV95 coordinates into their corresponding Longitude and Latitude values.

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

## Tests
In order to run the tests execute the following command:

```bash
python3 -m unittest discover -v
```
