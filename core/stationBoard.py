import datetime


class StationBoard:
    def __init__(self, header):
        self.header = header
        self.departures = []

    def add_departure(self, row):
        row = dict(zip(self.header, row))
        self.departures.append(Departure(row))


class Departure:
    def __init__(self, row):
        self.line = row['Fahrt']

        for i, char in enumerate(self.line):
            if char.isdigit():
                break

        # TODO: Nightbusses (NB N6) cannot be distinguised uniquely with this logic (vs. T 6, both result in number 6)
        self.mode = self.line[:i].strip()
        self.number = self.line[i:].strip()

        self.departure_time = self._time_string_to_datetime(row['Ab'])
        self.delay = row['Prognose']
        exclusion_chars = ['•', '', '-']
        _destinations_raw = [r for r in row['Nach'].split('\n') if r not in exclusion_chars]

        self.final_destination = _destinations_raw[0]

        self.stops = [[s[:-7], self._time_string_to_datetime(s[-5:])] for s in _destinations_raw[1:]]

    @staticmethod
    def _time_string_to_datetime(tstring):
        hour, minute = tstring.split(':')
        now = datetime.datetime.combine(datetime.date.today(), datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute))
        departure = datetime.datetime.combine(datetime.date.today(), datetime.time(int(hour), int(minute)))

        if departure < now:
            departure += datetime.timedelta(days=1)
        return departure

    def __str__(self):
        retstr = '-' * 50 + '\n'
        retstr += self.mode + ' ' + self.number + ' nach ' + self.final_destination + ': ' + str(self.departure_time) + '(Delay: ' + self.delay + ')' + '\n'
        for stop in self.stops:
            retstr += ' ' * 4 + stop[0] + ': ' + str(stop[1]) + '\n'

        return retstr
