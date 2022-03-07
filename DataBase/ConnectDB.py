# ！/usr/bin/python3
# coding:utf-8
from __init__ import *

import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm


def root_path():
    current_path = os.path.dirname(os.path.realpath(__file__))
    current_dir = os.path.basename(current_path)
    main_path = f'{current_path.replace(current_dir, "")}'
    return main_path


def sql_engine(db_name, path='db'):
    db_path = os.path.join(root_path(), 'DataBase', path, f'{db_name}.db')
    return create_engine(f'sqlite:///{db_path}', )


def conn_engine(db_name, path='db'):
    engine = sql_engine(db_name, path)
    return engine.connect()

