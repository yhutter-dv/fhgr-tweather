import os.path
import sys
import csv
from pyproj import Transformer
import json

if __name__ == "__main__":
    INPUT_FILE_PATH = "scripts/city_names.csv"
    OUTPUT_FILE_PATH = "scripts/cities.json"

    CITY_NAME_KEY = "Ortschaftsname"
    PLZ_KEY = "PLZ"
    EAST_COORDINATE_KEY = "E"
    NORTH_COORDINATE_KEY = "N"

    # Needed to convert from Swiss LV95 coordinate system to WGS84 (Longitude, Latitude)
    TRANSFORMER = Transformer.from_crs("EPSG:2056", "EPSG:4326")

    def convert_lv95_to_latlong_coordinates(
        east: float, north: float
    ) -> tuple[float, float]:
        lat, lon = TRANSFORMER.transform(east, north)
        return (lat, lon)

    def validate_csv_keys(row: dict) -> bool:
        keys_to_validate = [
            CITY_NAME_KEY,
            PLZ_KEY,
            EAST_COORDINATE_KEY,
            NORTH_COORDINATE_KEY,
        ]

        valid = True
        for key in keys_to_validate:
            result = row.get(key, None)
            if result is None:
                print(
                    f"Row of CSV File is not valid, expected key '{key}', but was not found"
                )
                # Note that we do not end early here because we wanna print all missing keys
                valid = False
        return valid

    if not os.path.isfile(INPUT_FILE_PATH):
        print(f"Could not find file {INPUT_FILE_PATH}")
        sys.exit(1)

    cities = []
    with open(INPUT_FILE_PATH, "r", encoding="utf-8-sig") as f:
        csv_reader = csv.DictReader(f, delimiter=";")
        for index, row in enumerate(csv_reader):
            # Validate first row only
            if index == 0 and not validate_csv_keys(row):
                print("CSV File does not contain expected keys")
                sys.exit(1)

            city_name = row[CITY_NAME_KEY]
            postal_code = int(row[PLZ_KEY])
            east_coordinate = float(row[EAST_COORDINATE_KEY])
            north_coordinate = float(row[NORTH_COORDINATE_KEY])
            latitude, longitude = convert_lv95_to_latlong_coordinates(
                east_coordinate, north_coordinate
            )

            city = {
                "name": city_name,
                "postal_code": postal_code,
                "latitude": latitude,
                "longitude": longitude,
            }

            cities.append(city)

    with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(cities, f, indent=2)
    print(f"Successfully wrote file {OUTPUT_FILE_PATH}")
