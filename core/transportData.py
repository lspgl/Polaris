import urllib.request
import json
from datetime import datetime, timedelta


class TransportData:
    def __init__(self):
        req = urllib.request.urlopen(
            'http://transport.opendata.ch/v1/stationboard?station=Rotbuchstrasse&limit=20').read()
        j_req = json.loads(req)
        # print(json.dumps(j_req, indent=4))

        # station = j_req['station']
        board = j_req['stationboard']

        for b in board:
            line = b['number']
            if line == '32':
                dest = b['to']
                # delay = b['stop']['delay']
                departure = b['stop']['departure']
                # print(departure.replace('T', ' '))
                departure_time = datetime.strptime(departure, '%Y-%m-%dT%H:%M:%S+0100')
                dt = (departure_time - datetime.now()).total_seconds() / 60
                print()
                print(line + ' ' + dest + ' ' + str(round(dt)) + 'min')


if __name__ == '__main__':
    td = TransportData()
