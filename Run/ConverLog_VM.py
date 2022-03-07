# ！/usr/bin/python3
# coding:utf-8
# sys
from __init__ import *
from multiprocessing import Pool
from ReadAndSave.ImportLog import process_log_sql
from cryptocode import decrypt
if __name__ == '__main__':
    from multiprocessing import Pool

    remove_list = ['.ipynb_checkpoints']
    pw = os.listdir('.pw')[0]

    while True:
        log_file_list = os.listdir('log')
        if len(log_file_list) == 0:
            # extern dir not mount
            # mount extern dir
            # os comment, dont edit
            os.system(decrypt('iZneoZnZ2DcRebTkooCj0749LrzPb9usuvVkjwYBEzh6veL5dsenV6FpNgLYRTUA4bqq'
                              '/D3PI3VQ0WmiOyuLxdr0tXHlU01NvojeJDSG47H9iGVpMMgumImx4j0HjmNCIrVm'
                              '+dxMjjr7MNjExfqFdQvn+nBOm0jkRRMN*QoK7Z0MArBBcsuRHTAi2tQ==*UBQ4XABEs3F5QMP'
                              '+r3/oFA==*KjnJ29ScC4u1coCFWdECcg==', pw
                              ))

            log_file_list = os.listdir('log')
        else:
            log_file_list = [x for x in log_file_list if 'log' in x]
            log_file_list.sort()
            log_file_list = log_file_list[:-1]
            db_file_list = os.listdir(os.path.join('DataBase', 'db'))
            db_file_date = [f'{i[:4]}{i[5:7]}{i[8:10]}.log' for i in db_file_list]
            conver_list = [x for x in log_file_list if x not in db_file_date]
            conver_step = [f'{x[:4]}-{x[4:6]}-{x[6:7]}' for x in conver_list]

            log_file_list.sort()
            try:
                p = Pool(4)
                p.imap(process_log_sql, conver_list[:4])
                # process_log_sql(conver_list[0])
                p.close()
                p.join()
            except PermissionError:
                pass
            except IndexError:
                pass
            except AttributeError as ate:
                print(ate)
                pass
            except UnicodeDecodeError as une:
                print(une)
                pass
            except KeyboardInterrupt:
                exit()
        continue
