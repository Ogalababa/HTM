# ！/usr/bin/python3
# coding:utf-8
from __init__ import *
from sqlalchemy import create_engine


def sql_engine(db_name, path='db'):
    db_path = os.path.join(rootPath, 'DataBase', path, f'{db_name}.db')
    return create_engine(f'sqlite:///{db_path}', )


def conn_engine(db_name, path='db'):
    engine = sql_engine(db_name, path)
    return engine.connect()

