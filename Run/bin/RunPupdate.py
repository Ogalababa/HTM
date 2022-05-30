# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *
from Run.core.Integration.ProcessDataBase import process_db
from Run.core.LogFilter.MountDir import mount_log
from datetime import datetime


def update_db():
    """Update database from last log file"""
    # Check log files
    # 检测log文件
    log_file_list = os.listdir(os.path.join(rootPath, 'log'))
    
    if len(log_file_list) == 0:
        mount_log()  # mount extern dir
        log_file_list = os.listdir(os.path.join(rootPath, 'log'))

    if len(log_file_list) > 1:
        log_file_list = [x for x in log_file_list if 'log' in x]
        log_file = max(log_file_list)
        try:
            # Analyze log files
            # 分析log文件
            process_db(log_file)
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # write update record
            # 写入更新记录
            with open(os.path.join(
                    usrPath, 'crontab_log', 'database_update.log'), 'a') as u_log:
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
            
            
def rebuild_db(log_file_2: str):
    """Update database from last log file"""
    # Check log files
    # 检测log文件
    log_file_list = os.listdir(os.path.join(rootPath, 'log'))
    
    if len(log_file_list) == 0:
        mount_log()  # mount extern dir
        log_file_list = os.listdir(os.path.join(rootPath, 'log'))

    if len(log_file_list) > 1:
        log_file_list = [x for x in log_file_list if 'log' in x]
        log_file = max(log_file_list)
        try:
            # Analyze log files
            # 分析log文件
            process_db(log_file_2)
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # write update record
            # 写入更新记录
            with open(os.path.join(
                    usrPath, 'crontab_log', 'database_update.log'), 'a') as u_log:
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
