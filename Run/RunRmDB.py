# ！/usr/bin/python3
# coding:utf-8
# sys
from __init__ import *
from datetime import datetime


if __name__ == '__main__':
    log_path = os.path.join(rootPath, 'DataBase', 'db')
    snelheid_path = os.path.join(rootPath, 'DataBase', 'snelheid')
    log_db = os.listdir(log_path)
    snelheid_db = os.listdir(snelheid_path)
    while len(log_db) > 365:
        os.remove(os.path.join(log_path, log_db.sort()[0]))
        log_db = os.listdir(log_path)
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f'{now}\tRemoved log database {log_db[0]}')

    while len(snelheid_db) > 365:

        os.remove(os.path.join(snelheid_path, snelheid_db.sort()[0]))
        snelheid_db = os.listdir(snelheid_path)
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f'{now}\tRemoved snelheid database {log_db[0]}')
