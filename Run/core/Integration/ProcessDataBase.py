# ！/usr/bin/python3
# coding:utf-8
# sys
from __init__ import *
from datetime import datetime
from Run.core.ConvertData.ReadLogs import read_log, log_to_sql, set_steps_denbdb3c
from Run.core.Integration.DataCalculator import Calculator


def process_db(log_file):
    """
    Process log data to database
    :param log_file: log date
    :return: None
    """
    start_time = datetime.now()
    log_path = os.path.join(rootPath, 'log', log_file)
    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Downloading {log_file}')
    wissel_log, date = read_log(log_path)

    try:
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Start update {log_file}')
        log_to_sql(wissel_log, date)
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Read log done')
        set_steps_denbdb3c(date)
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Set steps done')
        data_exp = Calculator(date)
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Calculation done')
        data_exp.C_tram_speed()
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Tram speed done')
        data_exp.C_wissel_schakel()
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Wissel schakel done')
        data_exp.C_storingen()
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Storingen done')
        end_time = datetime.now()
        delta = end_time - start_time
        print(f'Total process time: {round(delta.total_seconds(),2)} seconds')
        print('-'*30)
    except (AttributeError, UnicodeDecodeError, IndexError) as err:
        # print(err)
        pass

    except KeyboardInterrupt:
        exit()
