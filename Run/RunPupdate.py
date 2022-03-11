# ！/usr/bin/python3
# coding:utf-8
# sys
from __init__ import *
from ReadAndSave.ImportLog import process_log_sql
from ReadAndSave.MountDir import mount_log, umount_log

if __name__ == '__main__':

    log_file_list = os.listdir(os.path.join(rootPath, 'log'))
    if len(log_file_list) == 0:
        mount_log()  # mount extern dir
        log_file_list = os.listdir(os.path.join(rootPath, 'log'))

    else:
        log_file_list = [x for x in log_file_list if 'log' in x]
        log_file_list.sort()
        log_file = log_file_list = log_file_list[:-1]
        try:
            process_log_sql(log_file)
            umount_log()
        except (
                PermissionError,
                IndexError,
                AttributeError,
                UnicodeDecodeError
        ) as err:
            pass
        except KeyboardInterrupt:
            exit()
