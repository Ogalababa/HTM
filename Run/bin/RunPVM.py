# ！/usr/bin/python3
# coding:utf-8
# sys

from __init__ import *

from Run.core.Integration.ProcessDataBase import process_db
from Run.core.LogFilter.MountDir import mount_log

# Re-analyze all log files
# 重新分析所有log文件
def recover_db():
    """Recover all database from wissel log files"""
    # log_file_list = [i for i in os.listdir(os.path.join(rootPath, 'log')) if '.log' in i]
    log_file_list = ['20220725.log']
    log_file_list.sort()
    
    if len(log_file_list) == 0:
        mount_log()  # mount extern dir
        log_file_list = [i for i in os.listdir(os.path.join(rootPath, 'log')) if '.log' in i]
        log_file_list.sort()
    for i in log_file_list:
        process_db(i)


if __name__ == '__main__':
    recover_db()
