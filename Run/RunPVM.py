# ！/usr/bin/python3
# coding:utf-8
# sys
from __init__ import *
from multiprocessing import Pool
from ReadAndSave.ImportLog import process_log_sql
from cryptocode import decrypt

if __name__ == '__main__':

    pw = os.listdir('.pw')[0]
    with open(os.path.join(rootPath, '.pw', pw), 'r') as readfile:
        comm = readfile.readline()
        mount = comm[0][:-1]
        umount = comm[1][:-1]

    while True:
        log_file_list = os.listdir(os.path.join(rootPath, 'log'))
        if len(log_file_list) == 0:
            # extern dir not mount
            # mount extern dir
            # os comment, dont edit
            os.system(decrypt(mount, pw))

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
                os.system(decrypt(umount, pw))
                exit()

            conver_list.sort()
            try:
                p = Pool(4)
                p.imap(process_log_sql, conver_list[:4])
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
