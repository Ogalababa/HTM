# ！/usr/bin/python3
# coding:utf-8
# sys
from __init__ import *
from multiprocessing import Pool
from Run.core.ConvertData.ReadLogs import process_log_sql
from Run.core.LogFilter.MountDir import mount_log, umount_log


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

        else:
            log_file_list = [x for x in log_file_list if 'log' in x]
            log_file_list.sort()
            log_file_list = log_file_list[:-1]
            db_file_list = os.listdir(os.path.join(rootPath, 'DataBase', 'db'))
            db_file_date = [f'{i[:4]}{i[5:7]}{i[8:10]}.log' for i in db_file_list]
            conver_list = [x for x in log_file_list if x not in db_file_date]

            if len(conver_list) <= 0:
                print('All data up to date')
                umount_log()
                exit()

            conver_list.sort()
            try:
                p = Pool(10)
                p.imap(process_log_sql, conver_list[:10])
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