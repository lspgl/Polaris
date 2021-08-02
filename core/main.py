from transportData import SbbProvider
import datetime


def main():
    provider = SbbProvider(n_req=20)
    watchlist = [7, 14]

    watch_data = {}
    station_board = provider.content
    for dep in station_board.departures:
        print(dep)
        if int(dep.number) in watchlist:
            watch_data.setdefault(int(dep.number), []).append(dep)

    for key, value in watch_data.items():
        print(key)
        for dep in value:
            t = dep.departure_time
            print(dep.final_destination)
            print(t)
            dt = t - datetime.datetime.now()
            dt_min, dt_sec = divmod(dt.seconds, 60)
            if dt_min == 1439:
                dt_min = 0

            print(str(dt_min) + 'min ' + str(dt_sec))
            print(str(t.hour) + ':' + str(t.minute))
            print()


if __name__ == '__main__':
    main()
