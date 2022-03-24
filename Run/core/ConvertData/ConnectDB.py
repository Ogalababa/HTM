# ！/usr/bin/python3
# coding:utf-8
# sys
from __init__ import *
from sqlalchemy import create_engine


def sql_engine(db_name, path='db'):
    """Create a sql engine, connecting to wissel status database
    default path： Database/db"""
    db_path = os.path.join(rootPath, 'DataBase', path, f'{db_name}.db')
    return create_engine(f'sqlite:///{db_path}', )


def conn_engine(db_name, path='db'):
    """Connect engine to wissel status database"""
    engine = sql_engine(db_name, path)
    return engine.connect()
