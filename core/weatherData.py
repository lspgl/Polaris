import requests
import json
import pprint

from datetime import datetime

import sys
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Weather():
    APP_ID = 'bk8Z8O70'
    API_KEY = 'dj0yJmk9c05hSEZFY1VGVVlZJmQ9WVdrOVltczRXamhQTnpBbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTU3'
    with open(__location__ + '/.secret') as f:
        secret_content = f.readlines()
    API_SECRET = secret_content[0].strip()
    API_DARKSKY = secret_content[1].strip()

    YAHOO_WI_MAPPER = {0: 'wi-tornado',
                       1: 'wi-thunderstorm',
                       2: 'wi-hurricane',
                       3: 'wi-thunderstorm',
                       4: 'wi-thunderstorm',
                       5: 'wi-rain-mix',
                       6: 'wi-rain-mix',
                       7: 'wi-sleet',
                       8: 'wi-sleet',
                       9: 'wi-day-sprinke',
                       10: 'wi-sleet',
                       11: 'wi-day-showers',
                       12: 'wi-rain',
                       13: 'wi-snow',
                       14: 'wi-snow',
                       15: 'wi-snow-wind',
                       16: 'wi-snow',
                       17: 'wi-hail',
                       18: 'wi-sleet',
                       19: 'wi-dust',
                       20: 'wi-fog',
                       21: 'wi-day-haze',
                       22: 'wi-smoke',
                       23: 'wi-strong-wind',
                       24: 'wi-windy',
                       25: 'wi-snowflake-cold',
                       26: 'wi-cloudy',
                       27: 'wi-night-alt-cloudy',
                       28: 'wi-day-cloudy',
                       29: 'wi-night-alt-partly-cloudy',
                       30: 'wi-day-sunny-overcast',
                       31: 'wi-night-clear',  # alternatively wi-stars
                       32: 'wi-day-sunny',
                       33: 'wi-night-alt-cloudy-high',
                       34: 'wi-day-cloudy-high',
                       35: 'wi-rain-mix',
                       36: 'wi-hot',
                       37: 'wi-day-storm-showers',
                       38: 'wi-day-storm-showers',
                       39: 'wi-day-showers',
                       40: 'wi-rain',
                       41: 'wi-day-snow',
                       42: 'wi-snow',
                       43: 'wi-night-snow-thunderstorm',
                       44: 'wi-na',
                       45: 'wi-night-alt-showers',
                       46: 'wi-night-alt-snow',
                       47: 'wi-thunderstorm',
                       }
    _DARKSKY_WI_MAPPER_STR = """
    wi-day-sunny: clear-day
    wi-night-clear: clear-night
    wi-rain: rain
    wi-snow: snow
    wi-sleet: sleet
    wi-windy: wind
    wi-fog: fog
    wi-cloudy: cloudy
    wi-day-cloudy: partly-cloudy-day
    wi-night-alt-cloudy: partly-cloudy-night
    wi-hail: hail
    wi-thunderstorm: thunderstorm
    wi-tornado: tornado"""
    DARKSKY_WI_MAPPER = {}
    for entry in _DARKSKY_WI_MAPPER_STR.strip().splitlines():
        mapping = entry.strip().split(':')
        DARKSKY_WI_MAPPER[mapping[1].strip()] = mapping[0].strip()

    LONG, LAT = '47.3769', '8.5414'

    def __init__(self):

        self.req_url = 'https://api.darksky.net/forecast/' + self.API_DARKSKY + '/' + self.LONG + ',' + self.LAT + '?'

        params = {'units': 'si',
                  'exclude': 'minutely'}

        for key, value in params.items():
            self.req_url += str(key) + '=' + str(value) + '&'

    def get_weather(self):
        debug = False
        if debug:
            payload = json.loads("""
                    {"icon": "wi-day-cloudy", "Tnow": 16, "Thigh": 20, "Tlow": 11, "Summary": "Mostly Cloudy", "T24": [15.56, 16.94, 17.69, 18.43, 19.7, 20.47, 20.39, 19.43, 18.04, 16.11, 14.63, 13.62, 12.87, 12.31, 11.58, 10.85, 10.58, 10.96, 11.94, 13.27, 15.03, 17.01, 18.44, 19.53], "P24": [0.05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "Time24": ["13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00"]}
                    """)

            return payload

        # ------------------ DARK SKY IMPLEMENTATION -----------------

        response = requests.get(self.req_url)
        data = json.loads(response.content.decode('utf-8'))
        currently = data['currently']
        hourly = data['hourly']['data']
        daily = data['daily']['data']

        temperature_forecast = []
        precipation_forecast = []
        time_forecast = []
        for d in hourly[:12]:
            time_forecast.append(str(datetime.fromtimestamp(d['time']).hour).zfill(2) + ':00')
            temperature_forecast.append(d['temperature'])
            precipation_forecast.append(d['precipProbability'])

        payload = {
            'icon': self.DARKSKY_WI_MAPPER[currently['icon']],
            'Tnow': round(currently['temperature']),
            'Thigh': round(daily[0]['temperatureHigh']),
            'Tlow': round(daily[0]['temperatureLow']),
            'Summary': currently['summary'],
            'T24': temperature_forecast,
            'P24': precipation_forecast,
            'Time24': time_forecast
        }

        # ----------------------------------------------------

        return payload


if __name__ == '__main__':
    w = Weather()
    get = w.get_weather()
    print(get)
