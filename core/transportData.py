import urllib.request
from bs4 import BeautifulSoup
import datetime
import json
import sys
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
sys.path.append(__location__)

# from stationBoard import StationBoard
from stationBoardv2 import StationBoard


# SBB URL Example
# sbb_url = 'http://fahrplan.sbb.ch/bin/stboard.exe/dn?input=8591276&REQTrain_name=&boardType=dep&time=now&productsFilter=1111111111&selectDate=today&maxJourneys=20&start=yes'


class SbbProvider:
    API_BASE = 'http://fahrplan.sbb.ch/bin/stboard.exe/dn'
    API_BASE = 'https://transport.opendata.ch/v1/stationboard'
    BPUIC = {'Milchbuck': '8591276',
             'Rotbuchstrasse': '8591326',
             'ZurichHB': '8503000'}

    def __init__(self, n_req=10, station='Milchbuck'):
        self.station_id = self.BPUIC[station]
        self.n_req = n_req

    @property
    def content(self):
        station, board = self.fetch(self.station_id, nqueries=str(self.n_req))
        stationboard = StationBoard(board)
        return stationboard

    def fetch(self, station_id, nqueries='20'):
        url = self.urlmaker(station_id, nqueries)
        print(url)
        resource = urllib.request.urlopen(url)
        content = json.loads(resource.read())
        station = content['station']
        board = content['stationboard']
        return station, board

    def urlmaker(self, station_id, nqueries, time='now'):
        params = {'boardType': 'dep',
                  'productsFilter': '1111111111',
                  'start': 'yes',
                  'time': time,
                  'maxJourneys': str(nqueries),
                  'input': str(station_id)}

        params = {'id': station_id,
                  'limit': nqueries}

        param_string = '&'.join([key + '=' + value for key, value in params.items()])
        return self.API_BASE + '?' + param_string


def get_departures(provider):
    departure_data = []
    station_board = provider.content
    for dep in station_board.departures:
        t = dep.departure_time
        t_str = t.strftime("%d-%m %H:%M")
        dt = t - datetime.datetime.now()
        dt_min, dt_sec = divmod(dt.seconds, 60)
        dt_min += 1
        if dt_min > 1000:
            dt_min -= 1440

        if dt_min in [0, -1] and dep.delay is None:
            if dep.mode == 'T':
                img = 'tram'
            else:
                img = 'bus'
            dt_min = '<img src="/static/img/dep_' + img + '_white.png" style="margin-top:10px; margin-right:-10px;"/>'
        else:
            dt_min = str(dt_min) + "'"

        if dep.delay is not None:
            dt_min += "<span class='delay-minutes'>" + dep.delay + "</span>"

        dest = dep.final_destination.split('Zürich,', 1)[-1].strip()

        departure_data.append({'line': dep.line,
                               'mode': dep.mode,
                               'number': dep.number,
                               'dep': t_str,
                               'final': dest,
                               'dt_m': dt_min,
                               'dt_s': dt_sec,
                               'delay': dep.delay,
                               'foreground': dep.foreground,
                               'background': dep.background})
    return departure_data


if __name__ == '__main__':
    sbb = SbbProvider(n_req=20)
    pkg = get_departures(sbb)
    print(pkg)
