import urllib.request
from bs4 import BeautifulSoup
import datetime
import json
import sys
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
sys.path.append(__location__)

from stationBoard import StationBoard


# SBB URL Example
# sbb_url = 'http://fahrplan.sbb.ch/bin/stboard.exe/dn?input=8591276&REQTrain_name=&boardType=dep&time=now&productsFilter=1111111111&selectDate=today&maxJourneys=20&start=yes'


class SbbProvider:
    API_BASE = 'http://fahrplan.sbb.ch/bin/stboard.exe/dn'
    BPUIC = {'Milchbuck': '8591276',
             'Rotbuchstrasse': '8591326',
             'ZurichHB': '8503000'}

    def __init__(self, n_req=10, station='Milchbuck'):
        self.station_id = self.BPUIC[station]
        self.n_req = n_req

    @property
    def content(self):
        fetch = self.fetch(self.station_id, nqueries=str(self.n_req))
        soup = BeautifulSoup(fetch, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')

        header = rows[0]
        header = [idx.contents[0] for idx in header.find_all('th')]
        data = []
        for row in rows[1:]:
            cols = row.find_all('td')
            cols = [element.text.strip() for element in cols]
            data.append(cols)
        station_board, specials = self.parse_data(data, header)
        return station_board, specials

    def parse_data(self, data, header):
        specials = []
        station_board = StationBoard(header)
        departure_index = header.index('Ab')
        for row in data:
            if len(row) != len(header):
                specials.append(row)
            else:
                if row[departure_index][2] == ':':
                    dep_time = row[departure_index].split(':')
                    try:
                        int(dep_time[0])
                        int(dep_time[1])
                        station_board.add_departure(row)
                    except ValueError:
                        specials.append(row)

        return station_board, specials

    def fetch(self, station_id, nqueries='20', time='now'):
        url = self.urlmaker(station_id, nqueries)
        print(url)
        resource = urllib.request.urlopen(url)
        content_raw = resource.read().decode(resource.headers.get_content_charset())

        content_open = content_raw.split('<table cellspacing="0" class="hfs_stboard sq_dep_header">', 1)[1]
        content = content_open.split('</table>', 1)[0]
        content = '<table>' + content + '</table>'
        return content

    def urlmaker(self, station_id, nqueries, time='now'):
        params = {'boardType': 'dep',
                  'productsFilter': '1111111111',
                  'start': 'yes',
                  'time': time,
                  'maxJourneys': str(nqueries),
                  'input': str(station_id)}

        param_string = '&'.join([key + '=' + value for key, value in params.items()])
        return self.API_BASE + '?' + param_string


def get_departures(provider):
    departure_data = []
    station_board, specials = provider.content
    for dep in station_board.departures:
        t = dep.departure_time
        t_str = t.strftime("%d-%m %H:%M")
        dt = t - datetime.datetime.now()
        dt_min, dt_sec = divmod(dt.seconds, 60)
        dt_min += 1
        if dt_min > 1000:
            dt_min -= 1440

        if dt_min in [0, -1] and dep.delay == '':
            if dep.mode == 'T':
                img = 'tram'
            else:
                img = 'bus'
            dt_min = '<img src="/static/img/dep_' + img + '_white.png" style="margin-top:10px; margin-right:-10px;"/>'
        else:
            dt_min = str(dt_min) + "'"

        if 'ca.' in dep.delay:
            delay = dep.delay.split('ca.', 1)[-1].strip()
            if ':' in delay:
                dt_min = "<span class='delay-minutes'>" + dep.delay + "</span>"
            else:
                delay_time = int(delay.split('+', 1)[-1].split('Min.')[0].strip())
                dt_min = str(int(dt_min[:-1]) + delay_time) + "' <span class='delay-minutes'>(+" + str(delay_time) + "')</span>"
        elif dep.delay == 'Ausfall':
            dt_min = "<span class='delay-cancelled'>Ausfall</span>"
        elif dep.delay != '' and dep.delay != 'Zusätzliche Fahrt':
            dt_min = dt_min + ' ' + dep.delay

        if 'Zusätzliche Fahrt' in dep.delay:
            dt_min += ' (Zusätzliche Fahrt)'
            dt_min = dt_min.replace(') (', ' ')

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
