# ！/usr/bin/python3
# coding:utf-8
# sys
from __init__ import *

from Run.core.ConvertData.ReadLogs import read_log, log_to_sql, set_steps_denbdb3c
from Run.core.Integration.DataCalculator import Calculator


def process_db(log_file):
    """
    Process log data to database
    :param log_file: log date
    :return: None
    """
    log_path = os.path.join(rootPath, 'log', log_file)
    wissel_log, date = read_log(log_path)

    try:
        log_to_sql(wissel_log, date)
        set_steps_denbdb3c(date)
        data_exp = Calculator(date)
        data_exp.C_tram_speed()
        data_exp.C_wissel_schakel()
        data_exp.C_storingen()
    except (AttributeError, UnicodeDecodeError, IndexError) as err:
        print(err)

    except KeyboardInterrupt:
        exit()
