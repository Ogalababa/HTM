# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *
from multiprocessing import Pool
from Run.core.Integration.ProcessDataBase import process_db
from Run.core.LogFilter.MountDir import mount_log


def recover_db():
    """Recover all database from wissel log files"""
    while True:
        log_file_list = os.listdir(os.path.join(rootPath, 'log'))
        if len(log_file_list) == 0:
            # extern dir not mount
            # mount extern dir
            # os comment, dont edit
            mount_log()
            log_file_list = os.listdir(os.path.join(rootPath, 'log'))

        if len(log_file_list) >= 1:
            log_file_list = [x for x in log_file_list if 'log' in x]
            log_file_list.sort()
            log_file_list = log_file_list[:-1]
            db_file_list = os.listdir(os.path.join(rootPath, 'DataBase', 'db'))
            db_file_date = [f'{i[:4]}{i[5:7]}{i[8:10]}.log' for i in db_file_list]
            conver_list = [x for x in log_file_list if x not in db_file_date]
            if len(conver_list) <= 0:
                print('All data up to date')
                os._exit(0)

            conver_list.sort()
            try:
                p = Pool(20)
                p.imap(process_db, conver_list[:20])
                # process_log_sql(conver_list[0])
                p.close()
                p.join()
            except (
                    PermissionError,
                    IndexError,
                    AttributeError,
                    UnicodeDecodeError
            ) as err:
                pass
            except KeyboardInterrupt:
                exit()
        continue


if __name__ == '__main__':
    recover_db()
