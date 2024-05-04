from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pandas as pd

app = Flask(__name__)

debug = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/button_pressed', methods=['POST'])
def button_pressed():
    button_id = request.json['button_id']
    if button_id == 1: #requestToday
         curr_request = {
            "city": "Chur",  # Choose from Dropdown
            "date": "30-04-2024",  # Choose from Datepicker
            "settings": "temperature_2m,relative_humidity_2m,precipitation,weather_code,surface_pressure,cloud_cover,wind_speed_10m,wind_direction_10m"
        }
    elif button_id == 2: #requestForecast
         curr_request = {
            "city": "Chur",  # Choose from Dropdown
            "date": "02-05-2024",  # Choose from Datepicker
            "settings": "temperature_2m,relative_humidity_2m,precipitation,weather_code,surface_pressure,cloud_cover,wind_speed_10m,wind_direction_10m"
        }
    elif button_id == 3: # requestHistorical
         curr_request = {
            "city": "Chur",  # Choose from Dropdown
            "date": "02-05-2023",  # Choose from Datepicker
            "settings": "temperature_2m,relative_humidity_2m,precipitation,weather_code,surface_pressure,cloud_cover,wind_speed_10m,wind_direction_10m"
        }

    return jsonify(makeRequest(curr_request))

@app.route("/<request>")
def makeRequest(request):
    keys = request.keys()
    if "city" in keys:
        city = request["city"]
        if city == "":
            return "City empty", 400
    else:
        return "No City given", 400

    city_url = "https://geocoding-api.open-meteo.com/v1/search?name={0}&count=1".format(city)

    try:
        city_answer = pd.read_json(city_url)['results'][0]
    except:
        return "City not found", 400


    lat = round(city_answer['latitude'],2)
    lon = round(city_answer['longitude'],2)

    if debug: print(lat, lon)

    if "date" in keys:
        try:
            date = datetime.strptime(request["date"], '%d-%m-%Y').date()
        except:
            return "Invalid date", 400
        if debug: print(date)
    else:
        return "No Date given", 400

    if "settings" in keys:
        settings = request["settings"]
    else:
        return "No settings", 400

    if date == datetime.today().date():
        if debug: print("Heute")
        weather_url = "https://api.open-meteo.com/v1/forecast?latitude={0}&longitude={1}&current={2}".format(lat, lon, settings)
        weather_answer = pd.read_json(weather_url)["current"]
        del weather_answer["interval"]

    elif date > datetime.today().date():
        if debug: print("Forecast")
        weather_url = "https://api.open-meteo.com/v1/forecast?latitude={0}&longitude={1}&hourly={2}".format(lat, lon, settings)
        weather_answer = unpackHourly(pd.read_json(weather_url)["hourly"], date)
    else:
        if debug: print("Historical")
        start, stop = date, date
        weather_url = "https://archive-api.open-meteo.com/v1/era5?latitude={0}&longitude={1}&start_date={2}&end_date={3}&hourly={4}".format(lat, lon, start, stop, settings)
        weather_answer = unpackHourly(pd.read_json(weather_url)["hourly"], date)

    result = weather_answer.to_json(orient="columns")
    return result, 200


def unpackHourly(data, date):
    mytime = datetime.strptime('1200', '%H%M').time()
    fulldate = datetime.combine(date, mytime).strftime('%Y-%m-%dT%H:%M')

    index = data['time'].index(fulldate)
    for key in data.keys():
        data[key] = data[key][index]

    return data

# example URL == "/get-data/chur?time="





if __name__ == "__main__":
    app.run(debug=True)