import datetime
from pprint import pprint

COLORS = {'T 14': ['#009ee3', '#fff'],
          'T 7': ['#000', '#fff'],
          'T 9': ['#4a3a90', '#fff'],
          'T 10': ['#e82d89', '#fff'],
          'B 69': ['#fff', '#000'],
          'B 72': ['#daaea0', '#000']
          }


class Departure:
    def __init__(self, departure):
        self.dep = departure
        self.dep.pop('passList', None)
        self.departure_time = datetime.datetime.strptime(self.dep['stop']['departure'].split('+')[0],
                                                         '%Y-%m-%dT%H:%M:%S')
        self.delay = self.dep['stop']['delay']
        self.final_destination = self.dep['to']
        self.number = self.dep['number']
        self.mode = self.dep['category']

        self.line = f'{self.mode} {self.number}'
        try:
            self.background, self.foreground = COLORS[self.line]
        except KeyError:
            self.background, self.foreground = ['#fff', '#000']
        pprint(self.dep)


class StationBoard:
    def __init__(self, data):
        self.data = data
        self.departures = [Departure(d) for d in data]
