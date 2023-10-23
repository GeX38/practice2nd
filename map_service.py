import datetime
from export_mod import retrieve_data, plot_map, _UTC
from data_test import date_in_datatime
def generate_plot(path,polz_vvod):
        file_path = path
        print(file_path)
        times = date_in_datatime(polz_vvod)
        # times = [
        #     # datetime.datetime(2023, 2, 6, 1, 17),
        #     # datetime.datetime(2023, 2, 6, 1, 32),
        #     # datetime.datetime(2023, 2, 6, 1, 37)
        #     datetime.datetime(2023, 2, 6, 10, 20),
        #     datetime.datetime(2023, 2, 6, 10, 35),
        #     datetime.datetime(2023, 2, 6, 10, 40)
        # ]
        times = [t.replace(tzinfo=t.tzinfo or _UTC) for t in times]
        print(times)
        data = retrieve_data(file_path, "ROTI", times)
        _data = {"ROTI": data}
        plot_map(
            plot_times=times,
            data=_data,
            type_d="ROTI",
            ncols=3,
            lon_limits=(25, 50),
            lat_limits=(25, 50)
        )