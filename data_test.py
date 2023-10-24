import h5py
from datetime import datetime


def date_in_datatime(dataset_names):
    times = [datetime.strptime(name, '%Y-%m-%d %H:%M:%S.%f') for name in dataset_names]

    # Уберем миллисекунды, так как они отсутствуют в примере times
    times = [time.replace(microsecond=0) for time in times]

    return times
def data_time(path):
    try:
        with h5py.File(path, 'r') as file:
            if 'data' in file:
                data_group = file['data']  # Доступ к группе 'data'

                # Получаем список всех имён объектов в группе 'data'
                dataset_names = list(data_group.keys())
                #print(dataset_names)
            else:
                print("Группа 'data' не существует в файле.")
            return dataset_names
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
