import pandas as pd
from datetime import datetime

#url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
#url = "https://geocoding-api.open-meteo.com/v1/search?name=Berlin"
'''
notes
Es wäre noch möglich einen Zeitaspekt einzubauen
Ich habe es jetzt aber immer auf 12:00 gesetzt falls nötig

Bei den Settings habe ich eine Liste erstellt, von allen Settings, 
welche sowohl für die Current, historical als auch den Forecast möglich sind

'''


requestToday = {
    "city" : "Chur",       #Choose from Dropdown
    "date" : "30-04-2024", #Choose from Datepicker
    "settings" : "temperature_2m,relative_humidity_2m,precipitation,weather_code,surface_pressure,cloud_cover,wind_speed_10m,wind_direction_10m"
}

requestForecast = {
    "city" : "Chur",       #Choose from Dropdown
    "date" : "02-05-2024", #Choose from Datepicker
    "settings" : "temperature_2m,relative_humidity_2m,precipitation,weather_code,surface_pressure,cloud_cover,wind_speed_10m,wind_direction_10m"
}

requestHistorical = {
    "city" : "Chur",       #Choose from Dropdown
    "date" : "02-05-2023", #Choose from Datepicker
    "settings" : "temperature_2m,relative_humidity_2m,precipitation,weather_code,surface_pressure,cloud_cover,wind_speed_10m,wind_direction_10m"
}

debug = False

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
    return result


def unpackHourly(data, date):
    mytime = datetime.strptime('1200', '%H%M').time()
    fulldate = datetime.combine(date, mytime).strftime('%Y-%m-%dT%H:%M')

    index = data['time'].index(fulldate)
    for key in data.keys():
        data[key] = data[key][index]

    return data

'''
requestToday
requestForecast
requestHistorical
'''

print(makeRequest(requestToday))
#{"time":"2024-04-30T12:00","temperature_2m":21.6,"relative_humidity_2m":41,"precipitation":0.0,"weather_code":1,"surface_pressure":948.7,"cloud_cover":41,"wind_speed_10m":14.6,"wind_direction_10m":200}

print("")
print(makeRequest(requestForecast))
#{"time":"2024-05-02T12:00","temperature_2m":17.6,"relative_humidity_2m":49,"precipitation":0.0,"weather_code":2,"surface_pressure":933.0,"cloud_cover":64,"wind_speed_10m":11.3,"wind_direction_10m":202}

print("")
print(makeRequest(requestHistorical))
#{"time":"2023-05-02T12:00","temperature_2m":12.4,"relative_humidity_2m":72,"precipitation":0.4,"weather_code":51,"surface_pressure":951.7,"cloud_cover":69,"wind_speed_10m":7.8,"wind_direction_10m":22}







'''
#Historical
curl "https://archive-api.open-meteo.com/v1/era5
      ?latitude=52.52
      &longitude=13.41
      &start_date=2021-01-01
      &end_date=2021-12-31
      &hourly=temperature_2m"
'''

'''
curl "https://api.open-meteo.com/v1/forecast
     ?latitude=52.52
     &longitude=13.41
     &current=
        temperature_2m,
        wind_speed_10m
     &hourly=
        temperature_2m,
        relative_humidity_2m,
        wind_speed_10m"
'''

'''
Possible Settings
Hourly:
    temperature_2m,
    relative_humidity_2m,
    precipitation,
    weather_code,
    surface_pressure,
    cloud_cover,
    wind_speed_10m,
    wind_direction_10m

Current:
    temperature_2m,
    relative_humidity_2m,
    apparent_temperature,
    precipitation,
    weather_code,
    surface_pressure,
    cloud_cover,
    wind_speed_10m,
    wind_direction_10m
'''