from yahoo_weather.weather import YahooWeather
from yahoo_weather.config.units import Unit

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

    def __init__(self):
        self.data = YahooWeather(APP_ID=self.APP_ID,
                                 api_key=self.API_KEY,
                                 api_secret=self.API_SECRET)
        self.data.get_yahoo_weather_by_city('zuerich', Unit.celsius)

    def get_weather(self):
        today = self.data.condition.__dict__
        next_3 = [f.__dict__ for f in self.data.forecasts[:4]]

        weather_payload = [today] + next_3

        for w in weather_payload:
            w['icon'] = self.YAHOO_WI_MAPPER[w['code']]

        print(weather_payload)

        return [today] + next_3


if __name__ == '__main__':
    w = Weather()
    get = w.get_weather()
    print(get)
