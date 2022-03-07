# ！/usr/bin/python3
# coding utf-8

from __init__ import *
from sqlalchemy import create_engine


def root_path():
    curpath = os.path.dirname(os.path.realpath(__file__))
    return curpath.replace(os.path.basename(curpath), '')


def to_sqlite(dataframe, sqlite_table):
    """

    :type sqlite_table: object
    :type dataframe: Dataframe
    """
    # connect database
    root_dir = root_path()
    db_path = os.path.join(root_dir, 'DataBase', 'db', 'all_wissel_data.db')
    engine = create_engine(f'sqlite:///{db_path}', )
    sqlite_connection = engine.connect()
    # Write database
    dataframe.to_sql(sqlite_table, sqlite_connection, if_exists='replace')
    # Close database
    sqlite_connection.close()
