# ！/usr/bin/python3
# coding:utf-8
# sys
from __init__ import *
from Run.core.ConvertData.ReadLogs import process_log_sql
from Run.core.LogFilter.MountDir import mount_log, umount_log
from datetime import datetime


def update_db():
    """Update database from last log file"""
    log_file_list = os.listdir(os.path.join(rootPath, 'log'))
    if len(log_file_list) == 0:
        mount_log()  # mount extern dir
        log_file_list = os.listdir(os.path.join(rootPath, 'log'))

    if len(log_file_list) > 1:
        log_file_list = [x for x in log_file_list if 'log' in x]

        log_file = max(log_file_list)
        try:
            process_log_sql(log_file)
            umount_log()
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            with open(os.path.join(
                    rootPath, 'database_update.log'), 'a') as u_log:
                u_log.write(f'{now}\t Database {log_file} updated\n')

        except (
                PermissionError,
                IndexError,
                AttributeError,
                UnicodeDecodeError
        ) as err:
            pass
        except KeyboardInterrupt:
            exit()


if __name__ == '__main__':
    update_db()

