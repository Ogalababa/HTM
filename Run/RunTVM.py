# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *
from multiprocessing import Pool
from ReadAndSave.ImportLog import process_log_sql

if __name__ == '__main__':

    remove_list = ['.ipynb_checkpoints']
    while True:
        log_file_list = os.listdir(os.path.join(rootPath, 'log'))
        conver_list = [x for x in log_file_list if x not in remove_list]
        conver_step = [f'{x[:4]}-{x[4:6]}-{x[6:7]}' for x in conver_list]

        log_file_list.sort()
        try:
            if len(conver_list) <= 0:
                exit()

            p = Pool(4)
            p.imap(process_log_sql, conver_list[:4])
            # process_log_sql(conver_list[0])
            p.close()
            p.join()
            for i in conver_list[:4]:
                os.remove(os.path.join(rootPath, 'log', i))
                print(f'Removed {i}')
        except (
                PermissionError,
                IndexError,
                AttributeError,
                UnicodeDecodeError,
        ) as err:
            pass
        except KeyboardInterrupt:
            exit()

        continue
